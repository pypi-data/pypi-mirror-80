from sqlalchemy import and_, or_, inspect
from sqlalchemy.schema import UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.sql import sqltypes
from sqlalchemy.ext.declarative.api import DeclarativeMeta

from .utils.adapter_base import AdapterBase
from .utils.column_type import ColumnType
from .utils.relation_type import RelationType


class SqlalchemyAdapter(AdapterBase):
    """An adapter for working with SqlAlchemy library.

    The `adapter_settings` for this class is a simple Python dictionary that
    must contain next values:

        - *session* is an SqlAlchemy session object that will be used to query
          a database.
        - *ModelBase* is a declarative base class for ORM models.
    """

    def __init__(self, adapter_settings):
        super().__init__(adapter_settings)
        self.session = adapter_settings["session"]
        self.ModelBase = adapter_settings["ModelBase"]

    # --- general methods ------------------------------------------------------

    @classmethod
    def is_usable(cls, model_cls):
        return issubclass(type(model_cls), DeclarativeMeta)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    @classmethod
    def iter_fields(cls, model_cls):
        for field in inspect(model_cls).attrs:
            if hasattr(field, "target"):
                continue  # a relation

            column = list(field.columns)[0]
            if column.foreign_keys:
                continue  # foreign key

            column_type = type(column.type)
            yield_type = ColumnType.OTHER

            for sql_type, cur_yield_type in (
                (sqltypes._Binary, ColumnType.BINARY),
                # Text is derived from String class, so checking it firsts
                (sqltypes.Text, ColumnType.TEXT),
                (sqltypes.String, ColumnType.STRING),
                (sqltypes.Integer, ColumnType.INTEGER),
                (sqltypes.Numeric, ColumnType.FLOAT),  # can be cecimal
                (sqltypes.Date, ColumnType.DATE),
                (sqltypes.Time, ColumnType.TIME),
                (sqltypes.DateTime, ColumnType.DATETIME),
                (sqltypes.Boolean, ColumnType.BOOLEAN),
            ):
                if issubclass(column_type, sql_type):
                    if cur_yield_type is ColumnType.FLOAT and column.type.asdecimal:
                        cur_yield_type = ColumnType.DECIMAL
                    yield_type = cur_yield_type
                    break

            yield field.key, yield_type

    @classmethod
    def iter_relations(cls, model_cls):
        registry = model_cls._decl_class_registry

        for field in inspect(model_cls).attrs:
            if not hasattr(field, "target"):
                continue  # not a relation

            # getting referenced model
            other_model_cls = None
            for value_from_registry in registry.values():
                if (
                    hasattr(value_from_registry, "__table__")
                    and value_from_registry.__table__ is field.target
                ):
                    other_model_cls = value_from_registry
                    break

            # getting relation type
            direction_name = field.direction.name

            if direction_name == "MANYTOMANY":
                direction = RelationType.MANY_TO_MANY

            elif direction_name == "MANYTOONE":
                direction = RelationType.MANY_TO_ONE
                other_field = field.back_populates or field.backref
                if other_field is not None:
                    other_attr = getattr(other_model_cls, other_field)
                    if not other_attr.property.uselist:
                        direction = RelationType.ONE_TO_ONE

            elif direction_name == "ONETOMANY":
                if not field.uselist:
                    direction = RelationType.ONE_TO_ONE
                else:
                    direction = RelationType.ONE_TO_MANY

            # getting reverse key
            reverse_key = None
            if field.back_populates:
                reverse_key = field.back_populates
            elif field.backref:
                reverse_key = field.backref[0]

            yield (field.key, other_model_cls, direction, reverse_key)

    @staticmethod
    def __iter_fields_columns(model_cls):
        """Returns an iterator of lists of type:

            [field_name, column_names]

        Where:
            - *field_name* is a name of a field of the `model_cls`.
            - *column_names* is a set of column names that the field uses
              (for example, in case of composite foreign key there will be
              one field that uses many columns to reference another model)

        :param model_cls: ORM model class for which relations are going to be
            iterated.
        :returns: A generator of field names and their columns.
        """

        for field in inspect(model_cls).attrs:

            if hasattr(field, "columns") and list(field.columns)[0].foreign_keys:
                continue  # foreign key (not a relation)

            if hasattr(field, "target"):  # a relation
                # assume that composite key has columns only from one table
                if not list(field.local_columns)[0].foreign_keys:
                    # no columns for the foreign key on this side
                    continue

                columns = field.local_columns
            else:
                columns = field.columns

            yield [field.key, {column.name for column in columns}]

    @classmethod
    def iter_required_fields(cls, model_cls):
        # --- collecting not null column names ---
        ignore_primary_key = False
        if len(model_cls.__table__.primary_key.columns) == 1:
            primary_column = list(model_cls.__table__.primary_key.columns)[0]
            if isinstance(primary_column.type, sqltypes.Integer):
                # single primary key of integer type have their default sequence
                # generated
                ignore_primary_key = True

        required_column_names = set()
        for column_name, column in model_cls.__table__.columns.items():
            if hasattr(column.default, "arg"):
                continue  # has a default value
            if not column.nullable:
                if not column.primary_key or not ignore_primary_key:
                    required_column_names.add(column_name)
                    continue

        # --- yielding field names ---
        for field_name, column_names in cls.__iter_fields_columns(model_cls):
            if required_column_names.intersection(column_names):
                yield field_name

    @classmethod
    def iter_unique_field_combinations(cls, model_cls):
        yielded_one_to_one = set()
        # --- one to one is also unique ---
        registry = model_cls._decl_class_registry

        for field in inspect(model_cls).attrs:
            if not hasattr(field, "target"):
                continue  # not a relation

            direction_name = field.direction.name

            # getting referenced model
            other_model_cls = None
            for value_from_registry in registry.values():
                if (
                    hasattr(value_from_registry, "__table__")
                    and value_from_registry.__table__ is field.target
                ):
                    other_model_cls = value_from_registry
                    break

            if direction_name == "MANYTOONE":
                other_field = field.back_populates or field.backref
                if other_field is not None:
                    other_attr = getattr(other_model_cls, other_field)
                    if not other_attr.property.uselist:  # one to one
                        yielded_one_to_one.add(field.key)
                        yield {field.key}

            elif direction_name == "ONETOMANY":
                if not field.uselist:  # one-to-one
                    yielded_one_to_one.add(field.key)
                    yield {field.key}

        # --- collecting unique constraints (for columns) ---
        unique_column_combinations = []
        for constraint in model_cls.__table__.constraints:
            if not isinstance(constraint, (UniqueConstraint, PrimaryKeyConstraint)):
                continue
            column_names = set()
            for column in constraint.columns:
                column_names.add(column.name)

            unique_column_combinations.append(column_names)

        # --- yielding unique field name combinations ---
        for unique_column_combination in unique_column_combinations:
            unique_fields = set()

            for field_name, column_names in cls.__iter_fields_columns(model_cls):
                if not (column_names - unique_column_combination):
                    unique_fields.add(field_name)
            if unique_fields:
                if len(unique_fields) == 1 and not (unique_fields - yielded_one_to_one):
                    continue  # was already yielded

                yield unique_fields

    @classmethod
    def get_table_fullname(cls, model_cls):
        return model_cls.__table__.fullname

    def get_model_cls_by_table_fullname(self, name):
        for value_from_registry in self.ModelBase._decl_class_registry.values():
            if not hasattr(value_from_registry, "__table__"):
                continue
            if name == self.get_table_fullname(value_from_registry):
                return value_from_registry

    def iter_all_models(self):
        for value_from_registry in self.ModelBase._decl_class_registry.values():
            if hasattr(value_from_registry, "__table__"):
                yield value_from_registry

    # --- methods for working with items ---------------------------------------

    @staticmethod
    def __none_on_the_other_side(model_field, related_model):
        # if it is the other model that has reference to
        # this model with foreign key equals `None`, then we
        # know that other model is not usable as filter
        for column in model_field.property.remote_side:
            if getattr(related_model, column.name) is None:
                return True
        return False

    def get(self, items_and_fkeys):
        if not items_and_fkeys:
            return []

        # initializing variables -----------------------------------------------
        item_cls = items_and_fkeys[0][0]
        model_cls = item_cls.model_cls
        session = self.session

        # --- getting item models from database --------------------------------
        all_items_filters = []
        query_object = session.query(model_cls)
        getters = items_and_fkeys[0][0].getters

        for item, fkeys in items_and_fkeys:
            one_item_filters = []
            for group in getters:
                group_filters = []
                # in case related item was not in database
                skip_group_filters = False
                for field_name in group:
                    if field_name not in item:
                        skip_group_filters = True
                        break

                    model_field = getattr(item.model_cls, field_name)
                    if field_name in item.fields:
                        field_value = item[field_name]
                        group_filters.append(model_field == field_value)
                    elif field_name in item.relations:
                        related_models = fkeys.get(field_name)
                        if not related_models:
                            # failed to get or created related model before
                            skip_group_filters = True
                            break

                        relation = item.relations[field_name]
                        if relation["relation_type"].is_x_to_one():
                            if related_models[0] is not None:
                                if self.__none_on_the_other_side(
                                    model_field, related_models[0]
                                ):
                                    skip_group_filters = True
                                    break

                            group_filters.append(model_field == related_models[0])
                        else:
                            contains_any = []
                            relation_type = item.relations[field_name]["relation_type"]
                            is_x_to_x = relation_type is RelationType.MANY_TO_MANY
                            for related_model in related_models:
                                if is_x_to_x or not self.__none_on_the_other_side(
                                    model_field, related_model
                                ):
                                    contains_any.append(
                                        model_field.contains(related_model)
                                    )
                            if contains_any:
                                group_filters.append(or_(*contains_any))
                            else:
                                skip_group_filters = True
                                break

                if not skip_group_filters and group_filters:
                    one_item_filters.append(and_(*group_filters))

            if one_item_filters:
                all_items_filters.append(or_(*one_item_filters))

        if not all_items_filters:
            return []  # nothing to get from DB

        query_object = query_object.filter(or_(*all_items_filters))
        models = query_object.all()

        #         print('+'*40)
        #         print(str(query_object.statement.compile(
        #             compile_kwargs={"literal_binds": True})), flush=True)

        return models

    def delete(self, model):
        self.session.delete(model)

    def create_blank_model(self, model_cls):
        model = model_cls()
        self.session.add(model)
        return model

    def add_related_models(self, model, fkey, related_models):
        related_list = getattr(model, fkey)
        for model in related_models:
            if model not in related_list:
                related_list.append(model)

    def clear_related_models(self, model, fkey):
        getattr(model, fkey).clear()

    def related_x_to_many_exists(self, model, fkey):
        model_cls = type(model)
        exists_query = (
            self.session.query(model_cls)
            .filter(
                getattr(model_cls, fkey).any(),
                *[
                    getattr(model_cls, pk) == getattr(model, pk)
                    for pk in self.get_primary_key_names(model_cls)
                ]
            )
            .exists()
        )
        return self.session.query(exists_query).scalar()

    def related_x_to_many_contains(self, model, fkey, child_models):
        if not child_models:
            return []

        def model_filters(models):
            model_cls = type(models[0])
            filters = []
            for model in models:
                filters.append(
                    and_(
                        *[
                            getattr(model_cls, pk) == getattr(model, pk)
                            for pk in self.get_primary_key_names(model_cls)
                        ]
                    )
                )
            return or_(*filters)

        model_cls = type(model)
        child_model_cls = type(child_models[0])
        filter_value = and_(model_filters([model]), model_filters(child_models))

        query_object = (
            self.session.query(child_model_cls)
            .join(getattr(model_cls, fkey))
            .filter(filter_value)
        )

        return query_object.all()

    @classmethod
    def get_primary_key_names(cls, model_cls):
        return tuple(pk.name for pk in inspect(model_cls).primary_key)

    def save_model(self, model):
        self.session.add(model)
        self.session.flush()

    @classmethod
    def __get_select_and_keep_fielter(cls, model_cls, selectors, keepers):
        select_filter_sets = []
        for selectors_entry in selectors:
            select_filter_set = []
            for field_name, value in selectors_entry.items():
                select_filter_set.append(getattr(model_cls, field_name) == value)
            select_filter_sets.append(and_(*select_filter_set))
        total_select_filter = or_(*select_filter_sets)

        keep_fielter_sets = []
        for keepers_entry in keepers:
            keep_fielter_set = []
            for field_name, value in keepers_entry.items():
                keep_fielter_set.append(getattr(model_cls, field_name) != value)
            keep_fielter_sets.append(or_(*keep_fielter_set))
        total_keep_filter = and_(*keep_fielter_sets)

        if select_filter_sets or keep_fielter_sets:
            return and_(total_select_filter, total_keep_filter)
        return None

    def execute_delete(self, model_cls, selectors, keepers):
        filters = self.__get_select_and_keep_fielter(model_cls, selectors, keepers)
        if filters is not None:
            self.session.query(model_cls).filter(filters).delete()

    def execute_unref(self, parent, fkey, selectors, keepers):
        parent_cls = type(parent)
        registry = parent_cls._decl_class_registry
        target_property = getattr(parent_cls, fkey).property.target

        # getting referenced model class
        for value_from_registry in registry.values():
            if (
                hasattr(value_from_registry, "__table__")
                and value_from_registry.__table__ is target_property
            ):
                target_cls = value_from_registry
                break

        target_filters = self.__get_select_and_keep_fielter(
            target_cls, selectors, keepers
        )
        if target_filters is None:
            return

        pk_list = self.get_primary_key_names(parent_cls)

        query = (
            self.session.query(target_cls)
            .join(getattr(parent_cls, fkey))
            .filter(
                *[getattr(parent_cls, key) == getattr(parent, key) for key in pk_list],
                target_filters
            )
        )

        related_list = getattr(parent, fkey)
        for child in query:
            related_list.remove(child)

    # --- methods for tests ----------------------------------------------------

    def get_all_models(self, model_cls, sort_key=None):
        models = list(self.session.query(model_cls).all())
        if sort_key:
            models.sort(key=sort_key)
        return models

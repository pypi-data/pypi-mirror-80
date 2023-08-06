import re
import copy
from datetime import date, datetime, time
from decimal import Decimal
from itertools import chain
from pprint import pprint

from save_to_db.adapters.utils.column_type import ColumnType

from .item_base import ItemBase
from .item_contructor import complete_item_structure
from .item_metaclass import ItemMetaclass

from .bulk_item import BulkItem
from save_to_db.exceptions import (
    MultipleModelsMatch,
    WrongAlias,
    ItemProcessError,
    ItemRevertError,
)


#: regex for preparing strings to be converted into numeric values
_number_regex = re.compile(r"[^0-9\.]")


class Item(ItemBase, metaclass=ItemMetaclass, no_setup=True):
    """This class is used to collect data for a single item in order to create
    or update corresponding row or rows in a database.

    .. note::
        If you want to create an item class that will be used as a base for
        other item classed, you ca use `no_setup` argument:

            .. code:: Python

                class CustomItemBase(Item, no_setup=True):
                    pass  # shared staff goes here

                class ItemA(CustomItemBase):
                    pass

                class ItemB(CustomItemBase):
                    pass

    **To configure an item class use next class variables:**

    :cvar model_cls: Reference to an ORM model class of one of the supported
        ORM libraries.

        .. note::
            You can use :py:func:`~save_to_db.info.print_info` function from
            :py:mod:`save_to_db.info` module to print to console all supported
            ORM library names and their configurations for use with this
            library.

    :cvar batch_size: Maximum number of models that can be pulled from database
        with one query.
        Default: `None` (defined by used ORM library itself).

            .. seealso::
                `BATCH_SIZE` class constant of
                :py:class:`~save_to_db.adapters.utils.adapter_base.AdapterBase`
                class.

    :cvar defaults: Dictionary with default values, where value can be
        either raw value or a callable that accepts an item as an argument
        and returns a field value.

        .. note::
            Defaults order is based on the number of '__' that keys contain,
            shorter keys are prioritized. This is due to the fact that default
            values can be another items.

        .. warning::
            When using other item instances as default values, do not forget
            about possible item scoping (see :py:class:`~.scope.Scope` class),
            make sure that related items assigned by default are from the same
            scope. You can use the fact that items are automatically created
            when accessed:

            .. code-block:: Python

                defaults = {
                    # to make default values compatible with scoping,
                    # use this:
                    'item_1': lambda item: item['some_key'](field='value')
                    # instead of this:
                    'item_2': lambda item: OtherItem(field='value')
                    # or this:
                    'item_3': OtherItem(field='value')
                }

    :cvar creators: List of groups of fields (sets) of an item. When values for
        all fields of a group are present in an item, a new record can be
        created in a database using that group.

    :cvar autoinject_creators: If `True` (default) and `creators_autoconfig` is
        also set to `True`, then not null model fields will be added to each
        group in *creators* list.
        Default: `True`.

    :cvar creators_autoconfig: Sets auto configuration for `creators` fields,
        possible values:

            - `True` - auto configuration is on (adds to `creators` if they were
              manually configured);
            - `False` - auto configuration is off;
            - `None` - auto configuration is on if `creators` was not
              configured manually, off otherwise (Default).

    :cvar getters: List of groups of fields (sets) of an item. When values for
        all fields of a group are present in an item, then the group can be
        used to look for a record in a database.

        .. note::
            If `allow_merge_items` is `True`, `getters` considered to contain
            all the unique keys during merging.

    :cvar getters_autoconfig: Same as `creators_autoconfig` but for `getters`
        fields.

    :cvar nullables: Set of field names for which value must be set to null or
        to an empty list (in case of x-to-many relationship) when saving, if
        value is not present in the item.

        .. note::
            You can set this value to `True`, then all fields will be listed
            automatically.

    :cvar remove_null_fields: Set of field names which, in case they have `None`
        value (or an empty list in case of x-to-many relationship), must be removed
        from an item upon processing.

        .. warning::
            If a field name is listed in `nullables`, then it will not be
            deleted.

    :cvar remove_null_fields_autoconfig: Sets auto configuration for
        `remove_null_fields` fields, possible values:

            - `True` - auto configuration is on (adds to `remove_null_fields`
              if it was manually configured);
            - `False` - auto configuration is off;
            - `None` - auto configuration is on if `remove_nulls` was not
              configured manually, off otherwise (Default).

        .. note::
            Only not null fields are automatically added to to `remove_null_fields`.

    :cvar relations:  dictionary describing foreign keys (relations),
        example:

            .. code-block:: Python

                relations = {
                    'one': {
                        'item_cls': ItemClassOne,
                        'replace_x_to_many': False,  # default value
                    }
                    'two': ItemClassTwo,  # if we only interested in item class
                }

        Keys are the fields that reference other items (foreign key columns
        in database) and values are dictionaries with next keys and values:

            - 'item_cls' - item class used to create related item;
            - 'replace_x_to_many' - Only applicable to x-to-many
              relationships. If `True` then when saving an item to a
              database, remove old values for the field from database.
              Default: `False`.

    :cvar aliases: A `dict` with field aliases. Dictionary keys are used as
        aliases, and values are used as actual item field names. Aliases and
        field names can contain double underscores ("__").

    :cvar conversions: A dictionary that describes how string values must be
        converted to proper data types. Default `conversions` value:

        .. code-block:: Python

            conversions = {
                'decimal_separator': '.',
                'boolean_true_strings': ('true', 'yes', 'on', '1', '+',),
                'boolean_false_strings': ('false', 'no', 'off', '0', '-',),
                # Format values for dates and times used as arguments for
                # `datetime.datetime` function
                'date_formats': ('%Y-%m-%d',),  # can be multiple formats
                'time_formats': ('%H:%M:%S',),
                'datetime_formats': ('%Y-%m-%d %H:%M:%S',),
                # Functions conversions work only on values that are not of
                # string type and not already of required type.
                # They have priority over date and time formats.
                # If they return string, it'll be processed using date and
                # time formats
                'date_func': __some_conversion_function__,
                'time_func': __some_conversion_function__,
                'datetime_func': __some_conversion_function__,
                # example timezone: `datetime.timezone.utc`
                'default_timezone': __some_timzeone__,  # default: `None`
            }

        In case of absence of a value from `conversions` dictionary default
        value will be used.

        .. note::
            For "date_formats", "time_formats" and "datetime_formats" when
            only a single value is used, you can use that value instead of a
            tuple (or a list).

    :cvar allow_multi_update: If `True` then an instance of this class can
        update multiple models.
        Default: `False`.

    :cvar allow_merge_items:
        If `True` then all items that can potentially pull the same model from a
        database when persisting are merged into one item.
        Default: `False`.

    :cvar update_only_mode: If `True` then a new model in a database will not be
        created if it does not exist.
        Default: `False`.

        .. note:: Can be overwritten on an instance.

    :cvar get_only_mode: If `True` then the item data is used only to pull
        models from database in order to load other models through
        relationships.
        Default: `False`.

        .. note:: Can be overwritten on an instance.

    :cvar norewrite_fields: Dictionary with fields that cannot be changed.
        Example:

        .. code-block:: Python

            from save_to_db import RelationType

            norewrite_fields = {
                # always can rewrite
                'field_1': None,
                # rewrite value if it equals to`None`
                'field_2': True,
                # never rewrite, set only when model is created
                'field_3': False,
                # you can use tuples as keys
                ('field_4', 'field_5'): None,
                # referring to all many-to-many fields
                # (relation type can be used as a key)
                RelationType.MANY_TO_MANY: None,
                True: False,  # `True` for all the other fields
            }

        .. note::

            - You can use a `tuple` as a key to set many fields at once.
            - You can use `True` key for all not listed fields, including
              relations.
            - You can use values from
              :py:class:`~save_to_db.adapters.utils.relation_type.RelationType`
              enumeration for relation fields.

        .. note::
            If norewrite value is `True` for a field (can rewrite `None`),
            for many-to-x relationships the "many" side, even if already
            existed, can be added to by newly created related models.

    :cvar fast_insert: If `True` then models will not be pulled from database
        when persisting to database, new models will be created without trying
        to update.
        Default: `False`.

    :cvar deleter_selectors: Set of item field names that are going to
        be collected from processed (created and updated) ORM models and
        used as selectors.
        See `deleter_keepers` for more details.

    :cvar deleter_keepers: Set of item field names that are going to
        be collected from processed (created and updated) ORM models and used
        as keepers.
        Default value: `None` if `deleter_selectors` are also `None`,
        set of primary key fields otherwise.

        After finishing working with all items, you can call
        :py:meth:`~.persister.Persister.execute_deleter` method or
        :py:meth:`~.persister.Persister.execute_scope_deleter` method of
        :py:class:`~.persister.Persister` class to delete all those models that
        have same field values that were collected using
        `deleter_selectors`, but not the same as collected using
        `deleter_keepers`.

        .. seealso::
            `deleter_execute_on_persist` setting.

        .. seealso::
            :py:class:`~save_to_db.core.model_deleter.ModelDeleter` class.
            An instance of the class is created and stored in
            `item_cls.metadata['model_deleter']` class variable (where
            `item_cls` is a subclass of this class).

    :cvar deleter_execute_on_persist:
        If `True` then model deleter is executed upon item persistence.
        Default: `False`.

    :cvar unref_x_to_many: A dictionary containing x-to-many relationship
        fields as keys, and model deleter settings as values.

        Example:

        .. code-block:: Python

            unref_x_to_many = {
                'field_1_x_first': {
                    'selectors': ['field_1', 'field_2'],
                    # default for keepers: set of primary key fields
                    'keepers': ['field_a', 'field_b'],
                },
                # if you want to use default keepers (primary key fields),
                # you can use a shortcut
                'field_1_x_first': ['field_x', 'field_y']
            }

        Upon saving referenced by the fields models are unreferenced (removed
        from relation) if they can be selected from database by selectors,
        but cannot be selected using keepers.

        Selectors and keepers values are grabbed from the items being added to
        relations.

        .. seealso::
            `deleter_selectors` and `deleter_keepers`.

        .. seealso::
            :py:class:`~save_to_db.core.model_deleter.ModelDeleter` class.
            Instances of the class are created and stored in
            `item_cls.metadata['model_unrefs']` class dictionary (where
            `item_cls` is a subclass of this class). Dictionary keys are
            x-to-many field names, dictionary values are instances of
            :py:class:`~save_to_db.core.model_deleter.ModelDeleter` class.
    """

    DUMP_INSTANCE_ATTRS = ("update_only_mode", "get_only_mode")

    # --- special methods ------------------------------------------------------

    def __init__(self, **kwargs):
        super().__init__()
        self.complete_setup()

        for key, value in kwargs.items():
            item = self
            real_keys = self._get_real_keys(key)
            i = -1
            for i, real_key in enumerate(real_keys[:-1]):
                if item.is_bulk_item():
                    i -= 1
                    break
                item = item[real_key]

            remaining_key = "__".join(real_keys[i + 1 :])
            if not isinstance(value, list):
                item[remaining_key] = value
            else:
                item[remaining_key].add(*value)

    @classmethod
    def _get_real_keys(cls, key, as_string=False):
        result = []
        item_cls = cls

        def add_key_to_result(add_key):
            nonlocal result, item_cls

            item_cls.complete_setup()

            if add_key in item_cls.relations:
                item_cls = item_cls.relations[add_key]["item_cls"]
                result.append(add_key)
            elif add_key in item_cls.fields:
                item_cls = None
                result.append(add_key)
            else:
                raise WrongAlias(
                    "Wrong key: {} (full path: {}), "
                    "alias of: {}".format(add_key, key, cls)
                )

        cur_key = key
        while cur_key:
            if item_cls is None:
                raise WrongAlias(
                    "Cannot process the rest of path: {} (full path: {}), "
                    "alias of: {}".format(cur_key, key, cls)
                )

            aliased = False
            for alias, path in item_cls.aliases.items():
                if cur_key.startswith(alias):
                    cur_key = cur_key.replace(alias, path, 1)
                    aliased = True
                    break
            if aliased:
                continue

            if "__" in cur_key:
                add_key, cur_key = cur_key.split("__", 1)
                add_key_to_result(add_key)
            else:
                add_key_to_result(cur_key)
                break

        if not as_string:
            return result
        return "__".join(result)

    @classmethod
    def _cls_genitem(cls, key):
        """Generates an item for the given relation key.

        :param key: Relation key for which to create related item instance.
        :returns: Generated item.
        """
        relation = cls.relations[key]
        if relation["relation_type"].is_x_to_many():
            item = relation["item_cls"].Bulk()
        else:
            item = relation["item_cls"]()
        return item

    def __setitem__(self, key, value):
        item = self
        real_keys = item._get_real_keys(key)

        for i, real_key in enumerate(real_keys[:-1]):
            if real_key not in item.data:
                new_item = item._cls_genitem(real_key)
                super(Item, item).__setitem__(real_key, new_item)

            item = item.data[real_key]
            if item.is_bulk_item():
                item["__".join(real_keys[i + 1 :])] = value
                return

        super(Item, item).__setitem__(real_keys[-1], value)

    def __getitem__(self, key):
        item = self
        real_keys = item._get_real_keys(key)
        for i, real_key in enumerate(real_keys):
            item.complete_setup()

            if real_key not in item.data:
                if real_key in item.fields:
                    raise KeyError(real_key)

                new_item = item._cls_genitem(real_key)
                super(Item, item).__setitem__(real_key, new_item)

            item = item.data[real_key]
            if isinstance(item, BulkItem):
                bulk_real_keys = real_keys[i + 1 :]
                if not bulk_real_keys:
                    # return the bulk item itself
                    return item
                # something in bulk item
                return item._get_direct(bulk_real_keys)

        return item

    def __delitem__(self, key):
        real_keys = self._get_real_keys(key)
        item = self
        for i, real_key in enumerate(real_keys[:-1]):
            item = item.data[real_key]
            if item.is_bulk_item():
                real_key = "__".join(real_keys[i + 1 :])
                del item[real_key]
                return

        super(Item, item).__delitem__(real_keys[-1])

    def __contains__(self, key):
        try:
            real_keys = self._get_real_keys(key)
        except KeyError:
            return False
        return self._contains_direct(real_keys)

    def _contains_direct(self, real_keys):
        this_key, *those_keys = real_keys
        if this_key in self.data:
            if not those_keys:
                return True
            return self.data[this_key]._contains_direct(those_keys)
        return False

    def __deepcopy__(self, memo={}):
        if self in memo:
            return memo[self]

        self_copy = type(self)()
        memo[self] = self_copy

        # copying fields and relations
        for field_name in chain(self.fields, self.relations):
            if field_name in self.data:
                self_copy.data[field_name] = copy.deepcopy(
                    self.data[field_name], memo=memo
                )

        return self_copy

    def __iter__(self):
        return iter(self.data)

    # --- utility methods ------------------------------------------------------

    def to_dict(self, revert=False):
        return self._to_dict(revert=revert, _item_to_dict={}, _address_to_item={})

    def _to_dict(self, revert, _item_to_dict, _address_to_item):
        self_address = id(self)
        if self_address in _item_to_dict:
            if self_address not in _address_to_item:
                _address_to_item[self_address] = len(_address_to_item) + 1
            self_id = _address_to_item[self_address]
            _item_to_dict[self_address]["id"] = self_id
            return {
                "id": self_id,
            }

        result = {
            "item": {},
        }
        _item_to_dict[self_address] = result

        # relations have to be always processed in the same order to have
        # the same value under "id" key in result dictionary each time
        data_keys = list(self.data)
        data_keys.sort()
        for key in data_keys:
            value = self.data[key]
            if not isinstance(value, ItemBase):
                if revert:
                    value = self.revert_field(key, value, aliased=False)
                result["item"][key] = value
            else:
                result["item"][key] = value._to_dict(
                    revert=revert,
                    _item_to_dict=_item_to_dict,
                    _address_to_item=_address_to_item,
                )

        cls = type(self)
        for key in self.DUMP_INSTANCE_ATTRS:
            self_value = getattr(self, key)
            cls_value = getattr(cls, key)
            if self_value != cls_value:
                result[key] = self_value

        return result

    def load_dict(self, data):
        return self._load_dict(data, _id_to_item={})

    def _load_dict(self, data, _id_to_item):

        if "id" in data:
            if data["id"] not in _id_to_item:
                _id_to_item[data["id"]] = type(self)()

            item = _id_to_item[data["id"]]
            if "item" not in data:
                return item
        else:
            item = type(self)()

        if "item" not in data:
            raise Exception(data.keys())

        for key, value in data["item"].items():
            if key in item.fields:
                item[key] = value
            elif key in item.relations:
                item[key] = item[key]._load_dict(value, _id_to_item)

        for key in self.DUMP_INSTANCE_ATTRS:
            if key in data:
                setattr(item, key, data[key])

        return item

    @classmethod
    def get_item_cls(cls):
        return cls

    @classmethod
    def is_scoped(cls):
        return cls.metadata["collection_id"] is not None

    @classmethod
    def get_collection_id(cls):
        return cls.metadata["collection_id"]

    # --- main methods ---------------------------------------------------------

    @staticmethod
    def _Auto(model_cls, **kwargs):
        """Creates new item class.

        :param model_cls: model for witch new item class is generated.
        :param \*\*kwargs: key-word arguments that will be used as new class
            attributes.
        :returns: Newly created item class.
        """
        kwargs["model_cls"] = model_cls
        item_cls = type("{}Item".format(model_cls.__name__), (Item,), kwargs)
        return item_cls

    @classmethod
    def Bulk(cls, *args, **kwargs):
        """Creates a :py:class:`~.bulk_item.BulkItem` instance for this item
        class.

        :param \*args: Positional arguments that are passed to bulk item
            constructor.
        :param \*\*kwargs: Keyword arguments that are passed to bulk item
            constructor.
        :returns: :py:class:`~.bulk_item.BulkItem` instance for this item class.
        """
        return BulkItem(cls, *args, **kwargs)

    def as_list(self):
        return [self]

    def is_single_item(self):
        return True

    def is_bulk_item(self):
        return False

    @classmethod
    def revert_field(cls, key, value, aliased=True):
        """Converts field into JSON serializable field in such a way
        that :py:meth:`~.process_field` method converts it back to the original
        value.

        :param key: Key using which proper value type can be determined.
            This value can contain double underscores to reference relations.
        :param value: Value to process.
        :param aliased: If it's `True` then `key` contains field aliases.
        :returns: Value converted to proper type.
        """
        if isinstance(value, str):
            return value

        if value is None:
            return

        if aliased:
            real_key = cls._get_real_keys(key, as_string=True)
        else:
            real_key = key

        if "__" in real_key:
            this_key, that_key = real_key.split("__", 1)
            return cls.relations[this_key]["item_cls"].revert_field(
                that_key, value, aliased=False
            )

        conversions = cls.conversions
        column_type = cls.fields[real_key]

        if column_type is ColumnType.DECIMAL:
            return str(value).replace(".", conversions["decimal_separator"])
        elif column_type in (ColumnType.DATE, ColumnType.TIME, ColumnType.DATETIME):
            value = cls.process_field(key, value, aliased)

            if column_type is ColumnType.DATE:
                return value.strftime(conversions["date_formats"][0])
            elif column_type is ColumnType.TIME:
                return value.strftime(conversions["time_formats"][0])
            elif column_type is ColumnType.DATETIME:
                return value.strftime(conversions["datetime_formats"][0])

        return value

    def revert(self):
        return self._revert(_procesed_items=[])

    def _revert(self, _procesed_items):
        if self in _procesed_items:
            return
        _procesed_items.append(self)

        for key, value in self.data.items():
            if not isinstance(value, ItemBase):
                try:
                    self.data[key] = self.revert_field(key, value, aliased=False)
                except:
                    raise ItemRevertError(self, key, value)
            else:
                value._revert(_procesed_items=_procesed_items)

    @classmethod
    def process_field(cls, key, value, aliased=True):
        """Converts `value` to the appropriate data type for the given
        `key`.

        :param key: Key using which proper value type can be determined.
            This value can contain double underscores to reference relations.
        :param value: Value to process.
        :param aliased: If it's `True` then `key` contains field aliases.
        :returns: Value converted to proper type.
        """
        cls.complete_setup()

        if value is None:
            return None

        if aliased:
            real_key = cls._get_real_keys(key, as_string=True)
        else:
            real_key = key

        if "__" in real_key:
            this_key, that_key = real_key.split("__", 1)
            return cls.relations[this_key]["item_cls"].process_field(
                that_key, value, aliased=False
            )

        conversions = cls.conversions
        column_type = cls.fields[real_key]
        if column_type is ColumnType.BINARY:
            if not isinstance(value, bytes):
                if isinstance(value, str):
                    value = bytes(value, "utf-8")
                else:
                    raise ValueError("Cannot convert to bytes: {}".format(value))
        elif column_type is ColumnType.BOOLEAN:
            if not isinstance(value, bool):
                if value.lower() in conversions["boolean_true_strings"]:
                    value = True
                elif value.lower() in conversions["boolean_false_strings"]:
                    value = False
                else:
                    raise ValueError("Cannot convert to boolean: {}".format(value))
        elif column_type.is_str():
            if not isinstance(value, str):
                value = str(value)
        elif column_type.is_num():
            if isinstance(value, str):
                if conversions["decimal_separator"] != ".":
                    value = value.replace(".", "")
                value = value.replace(conversions["decimal_separator"], ".")
                value = _number_regex.sub("", value)
            if column_type is ColumnType.INTEGER:
                if not isinstance(value, int):
                    value = int(value)
            elif column_type is ColumnType.FLOAT:
                if not isinstance(value, float):
                    value = float(value)
            elif column_type is ColumnType.DECIMAL:
                if not isinstance(value, Decimal):
                    value = Decimal(value)
        elif column_type in (ColumnType.DATE, ColumnType.TIME, ColumnType.DATETIME):
            # first trying functions
            wanted_instance = {
                ColumnType.DATE: date,
                ColumnType.TIME: time,
                ColumnType.DATETIME: datetime,
            }[column_type]
            if not isinstance(value, (str, wanted_instance)):
                conversion_func = {
                    ColumnType.DATE: conversions["date_func"],
                    ColumnType.TIME: conversions["time_func"],
                    ColumnType.DATETIME: conversions["datetime_func"],
                }[column_type]

                if conversion_func:
                    value = conversion_func(value)

            if isinstance(value, str):
                format_list = {
                    ColumnType.DATE: conversions["date_formats"],
                    ColumnType.TIME: conversions["time_formats"],
                    ColumnType.DATETIME: conversions["datetime_formats"],
                }[column_type]

                for value_format in format_list:
                    try:
                        value = datetime.strptime(value, value_format)
                        break
                    except ValueError:
                        pass
                else:
                    raise Exception(
                        'Failed to convert key "{}", value: {}'.format(key, value)
                    )

                # converting datetime if needed
                if column_type is ColumnType.DATE:
                    value = value.date()

                elif column_type is ColumnType.TIME:
                    value = value.time().replace(tzinfo=value.tzinfo)

            if (
                isinstance(value, (time, datetime))
                and value.tzinfo is None
                and conversions["default_timezone"] is not None
            ):
                value = value.replace(tzinfo=conversions["default_timezone"])

        return value

    def process(self):
        self._process(_procesed_items=[])
        return complete_item_structure(self)

    def _process(self, _procesed_items):
        if self in _procesed_items:
            return
        _procesed_items.append(self)

        self.before_process()  # hook

        # processing defaults
        keys = list(self.defaults)
        # 1. first processing shortest keys
        # 2. defaults that use functions must be processed at the end
        def get_key_for_default(key):
            value = self.defaults[key]
            order = 0
            if callable(value) and not isinstance(value, ItemBase):
                order = 1
            # (although right now referencing related items is impossible here)
            return (key.count("__"), order)

        keys.sort(key=get_key_for_default)

        for key in keys:
            if key in self.data:
                continue

            value = self.defaults[key]
            if callable(value) and not isinstance(value, ItemBase):
                value = value(self)

            end_item_cls = type(self)
            end_relation = None
            for subkey in key.split("__"):
                if subkey in end_item_cls.relations:
                    end_relation = end_item_cls.relations[subkey]
                    end_item_cls = end_relation["item_cls"]
                else:
                    end_relation = None

            if not end_relation:  # not a relations
                self[key] = self.process_field(key, value, aliased=False)
            else:
                if (
                    not isinstance(value, list)
                    or not end_relation["relation_type"].is_x_to_many()
                ):
                    self[key] = value
                else:
                    bulk_item = self.relations[key]["item_cls"].Bulk()
                    bulk_item.add(*value)
                    self[key] = bulk_item

        # processing nullables
        for key in self.nullables:
            if key in self:
                continue
            if key in self.fields:
                self[key] = None
            elif key in self.relations:
                relation = self.relations[key]
                if relation["relation_type"].is_x_to_many():
                    self[key] = relation["item_cls"].Bulk()
                else:
                    self[key] = None

        # processing remove_null_fields
        for key in self.remove_null_fields:
            if key not in self or key in self.nullables:
                continue
            if (
                key not in self.relations
                or not self.relations[key]["relation_type"].is_x_to_many()
            ):
                if self[key] is None:
                    del self[key]
            else:
                if len(self[key]) == 0:
                    del self[key]

        # processing set fields
        for key, value in list(self.data.items()):  # changes size
            if not isinstance(value, ItemBase):
                try:
                    self[key] = self.process_field(key, value, aliased=False)
                except:
                    raise ItemProcessError(self, key, value)
            else:
                value._process(_procesed_items=_procesed_items)

        self.after_process()  # hook

    def resolve_model(self, models):
        """This function is called during persisting when two or more models
        match the same item and `allow_multi_update` setting is set to `False`.
        It must return a single item to be used instead or raise a
        :py:class:`save_to_db.exceptions.item_persist.MultipleModelsMatch`
        exception.

        .. warning::
            If `allow_multi_update` option is `True`, then this function is
            ignored.

        :param models: List of models that this item matches.
        :returns: Single model to be updated.
        """
        raise MultipleModelsMatch(self, models)

    # --- helper functions -----------------------------------------------------

    def get_config(self):
        """ Returns instance configuration. """

        default_configuration = ItemMetaclass.get_default_configuration()
        config = {}
        for key in default_configuration.keys():
            config[key] = getattr(self, key)
        return config

    def print_config(self):
        """ Pretty prints item instance configuration to console. """

        pprint(self.get_config())

    @classmethod
    def get_cls_config(cls):
        """ Returns class configuration. """

        return cls.get_config(cls)

    @classmethod
    def print_cls_config(cls):
        """ Pretty prints item class configuration to console. """

        pprint(cls.get_cls_config())

    # --- hooks ----------------------------------------------------------------

    def before_process(self):
        """ A hook method that is called before processing fields values. """
        pass

    def after_process(self):
        """A hook method that is called immediately after all fields have been
        processed.
        """
        pass

    def before_model_update(self, model):
        """A hook method that is called before updating matching model with
        item data.

        :param model: Model that was pulled from database or freshly
            created (in case there were no matching models).
        """
        pass

    def after_model_save(self, model):
        """A hook method that is called after updating matching ORM model with
        item data and saving the model to a database.

        :param model: Model that was updated.
        """
        pass

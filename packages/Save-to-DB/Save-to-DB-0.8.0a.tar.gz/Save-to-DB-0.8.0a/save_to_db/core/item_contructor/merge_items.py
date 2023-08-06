from itertools import chain
from save_to_db.core.item_base import ItemBase
from save_to_db.exceptions import MergeItemsNotTheSame


def merge_items(top_item, cls_items, cls_default_items):
    """Merges items that pull the same model from the database into a single
    items.

    :param top_item: the item that is being processed.
    :param cls_items: List of items in which items referring to the same model
        must be merged.
    :param cls_default_items: List of items that do not have to be updated
        (from bulk item default).
    """

    all_items = []

    def collect_items(donor_item, processed_items):
        if donor_item in processed_items:
            return
        processed_items.append(donor_item)

        # colecting from single item and bulk default items
        for key in donor_item.data:
            if isinstance(donor_item[key], ItemBase):
                collect_items(donor_item[key], processed_items=processed_items)

        if donor_item.is_single_item():
            all_items.append(donor_item)
        else:
            for item in donor_item:
                collect_items(item, processed_items=processed_items)

    collect_items(top_item, processed_items=[])

    cls_items_with_defaults = cls_items[:]
    cls_items_with_defaults.extend(cls_default_items)

    item_to_merged = []
    while True:
        item_merged = False
        merged_items = set()

        for i, item in enumerate(cls_items):
            if item not in all_items or item in merged_items or not item.getters:
                continue

            for next_item in cls_items_with_defaults[i + 1 :]:
                if next_item is item or next_item in merged_items:
                    continue

                # not merging second time (`merged_items` missing default items)
                if [item, next_item] in item_to_merged:
                    continue

                if not __same_items(
                    item, next_item, _no_check_pairs=None, _full_compare=False
                ):
                    continue

                __merge_item_into_item(item, next_item, all_items)
                if next_item not in cls_default_items:
                    merged_items.add(next_item)

                # not keeping merged items themselves
                for entry in item_to_merged:
                    if entry[0] is next_item:
                        item_to_merged.remove(entry)
                        break

                item_to_merged.append([item, next_item])
                item_merged = True

        if not item_merged:
            break

        # replacing merged_items with the extended item in single items
        for extended_item, merged_item in item_to_merged:
            for one_item in all_items:
                for key, value in one_item.data.items():
                    if value is merged_item:
                        one_item.data[key] = extended_item

            while merged_item in cls_items:
                cls_items.remove(merged_item)

            while merged_item in cls_items_with_defaults:
                cls_items_with_defaults.remove(merged_item)

        # replacing in bulk items
        __replace_in_bulk_items(top_item, item_to_merged, processed_items=[])


def __replace_in_bulk_items(item, item_to_merged, processed_items):
    if item in processed_items:
        return
    processed_items.append(item)

    if item.is_single_item():
        for f_key, relation in item.relations.items():
            if f_key in item:
                __replace_in_bulk_items(
                    item[f_key], item_to_merged, processed_items=processed_items
                )
    else:
        for extened_item, merged_item in item_to_merged:
            if merged_item in item:
                index = item.bulk.index(merged_item)
                item.bulk.remove(merged_item)
                # can be multiple merged items into the same item
                if extened_item not in item.bulk:
                    item.bulk.insert(index, extened_item)

            # updating defaults
            for key, default_value in item.data.items():
                if not isinstance(default_value, ItemBase):
                    continue

                if default_value is merged_item:
                    item.data[key] = extened_item

                if default_value.is_bulk_item():
                    __replace_in_bulk_items(
                        default_value, item_to_merged, processed_items=processed_items
                    )

        for item_in_bulk in item:
            __replace_in_bulk_items(
                item_in_bulk, item_to_merged, processed_items=processed_items
            )


def __get_item_getter_groups(item):
    getter_groups = []
    for group in item.getters:
        group_can_be_used = True
        for field_name in group:
            if field_name not in item.data and (
                field_name not in item.relations
                or item.relations[field_name]["relation_type"].is_x_to_one()
            ):
                group_can_be_used = False
                break

        if group_can_be_used:
            getter_groups.append(group)
    return getter_groups


def __same_items(item_one, item_two, _no_check_pairs, _full_compare):
    if item_one.is_bulk_item():
        return True

    _no_check_pairs = _no_check_pairs or []
    pair = [item_one, item_two]
    if pair in _no_check_pairs:
        return True
    _no_check_pairs.append(pair)

    if not _full_compare:
        item_one_getter_groups = __get_item_getter_groups(item_one)
        if not item_one_getter_groups:
            return False

        item_two_getter_groups = __get_item_getter_groups(item_two)
        if not item_two_getter_groups:
            return False

        # check if can be got by the same group
        can_be_get_same_group = False
        for group in item_one_getter_groups:
            if group in item_two_getter_groups:
                can_be_get_same_group = True
                break

        if not can_be_get_same_group:
            return

        compare_keys = set(getter for getter in chain(*item_one_getter_groups)) & set(
            getter for getter in chain(*item_two_getter_groups)
        )
    else:
        compare_keys = set(item_one.data) & set(item_two.data)

    # comparing data present in both items
    for key in compare_keys:
        if (
            key in item_one.relations
            and item_one.relations[key]["relation_type"].is_x_to_many()
        ):
            continue

        if item_two.data[key] != item_one.data[key]:

            if key in item_one.relations:
                if type(item_one.data[key]).allow_merge_items:
                    if __same_items(
                        item_one.data[key],
                        item_two.data[key],
                        _no_check_pairs=_no_check_pairs,
                        _full_compare=_full_compare,
                    ):
                        continue

            return False

    return True


def __merge_item_into_item(extended_item, merged_item, all_items):
    if not __same_items(
        extended_item, merged_item, _no_check_pairs=None, _full_compare=True
    ):
        raise MergeItemsNotTheSame(extended_item, merged_item)

    # `merged_item.data` can change size if it is merged with referenced items
    # and references itself through one of its keys
    for key in set(merged_item.data.keys()):
        is_x_to_many = False
        if key in extended_item.relations:
            is_x_to_many = extended_item.relations[key]["relation_type"].is_x_to_many()

            if not is_x_to_many and merged_item[key] not in all_items:
                continue  # merged item was replaced with extened

        if not is_x_to_many:
            if key not in extended_item.data:
                extended_item[key] = merged_item[key]
        else:
            for item in merged_item[key].bulk:
                if item not in all_items:
                    continue  # merged item was replaced with extened
                extended_item[key].add(item)

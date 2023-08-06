""" This module contains exceptions that are raised when there is an error
during processing of an item.
"""


class ItemProcessError(Exception):
    """General exception for processing instances of
    :py:class:`~save_to_db.core.item_base.ItemBase` class.
    """


class ItemRevertError(ItemProcessError):
    """General exception for converting processed field values of instances of
    :py:class:`~save_to_db.core.item_base.ItemBase` class.
    into json encadable values
    """


class MergeItemsNotTheSame(ItemProcessError):
    """Raised when two items have the same values of one of its getter groups
    but not the same.
    """


class MergeMultipleItemsMatch(ItemProcessError):
    """Raised when multiple items match the same model during merging.

    .. note::
        Even if two items contain the same data, they still considered different if
        there are other two items that point to them using one-to-x relationship
        and cannot be merged.
    """

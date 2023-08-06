""" This module contains exceptions for
:py:class:`~save_to_db.core.item_base.ItemBase` class related to persistence.
"""


class ItemPersistError(Exception):
    """General exception for :py:class:`~save_to_db.core.item_base.ItemBase`
    persistence.
    """


class PersistMultipleItemsMatch(ItemPersistError):
    """ Raised when multiple items match the same model during persisting. """


class MultipleModelsMatch(ItemPersistError):
    """Raised when multiple models match the same item:

    - When `allow_multi_update` set to `False` for the item.
    - When trying to set multiple items to x-to-one relationship.
    """


class CannotMergeModelsForItem(ItemPersistError):
    """ Raised when merging two or more ORM models into one is impossible. """


class CannotClearRequiredFieldInRelation(ItemPersistError):
    """Raise when trying to clear one-to-many field using "replace_x_to_many"
    setting of item, but field is required on the other side.
    """

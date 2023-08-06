""" This module contains exceptions for
:py:class:`~save_to_db.core.utils.item_collection.ItemCollection` class.
"""


class ItemCollectionException(Exception):
    """General exception for
    :py:class:`~save_to_db.core.utils.item_collection.ItemCollection`
    class.
    """


class CollectionDoesNotExist(ItemCollectionException):
    """Raised when trying to get collection that does not exist using
    `collection_id`.
    """


class CollectionIdAlreadyInUse(ItemCollectionException):
    """Raised when trying to create new item class collection with
    `collection_id` value already taken.
    """

""" This module contains exceptions for
:py:class:`~save_to_db.core.item_base.ItemBase` related to fields usage.
"""


class ItemFieldError(ValueError):
    """General exception for :py:class:`~save_to_db.core.item_base.ItemBase`
    field usage.
    """


class WrongAlias(ItemFieldError, KeyError):
    """ Raise when wrong alias is used. """


class BulkItemOneToXDefaultError(ItemFieldError):
    """Raised when trying to assing an one-to-x default relationship value
    to a bulk item.

    *Explanation:*

        When trying to use as default item A with an x-to-one relationship with
        items B that we keep in bulk, that means that all items B going to
        referece item A, but item A can reverese refrence only 1 item B, this
        results in an exception.
    """

import copy
import json
from pprint import pprint
from .utils.mapper import mapper
from .utils.proxy_object import ProxyObject
from .utils.selector import select
from .utils.dict_wrapper import DictWrapper


class ItemBase(object):
    """This is an abstract item class that serves as a base class for
    single item and bulk item classes.

    .. seealso::
        :py:class:`~.item.Item` and :py:class:`~.bulk_item.BulkItem` classes.

    :param \*\*kwargs: Values that will be saved as item data.
    """

    # --- special methods ------------------------------------------------------

    def __init__(self):
        self.data = {}
        self.proxy = None
        mapper.item_created(self)

    def __setitem__(self, key, value):
        if key in self.data and self.data[key] is value:
            return

        old_value = self.data.get(key)
        self.data[key] = value
        mapper.item_value_set(self, key, old_value, value)

    def __call__(self, **kwargs):
        for key, value in kwargs.items():
            self[key] = value
        return self

    def __getitem__(self, key):
        raise NotImplementedError()

    def __delitem__(self, key):
        old_value = self.data[key]
        del self.data[key]
        mapper.item_value_deleted(self, key, old_value)

    def __contains__(self, key):
        raise NotImplementedError()

    def __copy__(self):
        raise NotImplementedError("Please user deepcopy")

    def __deepcopy__(self, memodict={}):
        raise NotImplementedError()

    # --- utility methods ------------------------------------------------------

    def to_dict(self, revert=False):
        """Converts item into a Python `dict` object.

        :param revert: If `True` then converts all not JSON serializable field
            values into types that can be serialized.
        :returns: Python `dict` representation of the item.
        """
        raise NotImplementedError()

    def dict_wrapper(self):
        """This method is used for integration with Scrapy project, when
        parsing pages in Scrapy you can yield an item as
        :py:class:`~.utils.dict_wrapper.DictWrapper` (subclass of `dict`)
        and then use :py:meth:`~.utils.dict_wrapper.DictWrapper.get_item`
        method to get the original item.

        :returns: An :py:class:`~.utils.dict_wrapper.DictWrapper` class
            instance.
        """
        return DictWrapper(self)

    def load_dict(self, data):
        """Loads data from dictionary into the item.

        :param data: Dictionary with item data (see :func:`~to_dict` method).
        :returns: The item itself.
        """
        raise NotImplementedError()

    def get_proxy(self):
        """Returns an instancce of
        :py:class:`~save_to_db.core.utils.proxy_object.ProxyObject` for this item.

        .. seealso::
            :py:class:`~save_to_db.core.utils.proxy_object.ProxyObject`.
        """
        if self.proxy is None:
            self.proxy = ProxyObject(self)
        return self.proxy

    def select(self, key):
        """Just calls :py:func:`~.utils.selector.select` function from
        :py:mod:`save_to_db.core.utils.selector` module with `self` as the first
        argument.

            .. seealso::
                :py:func:`save_to_db.core.utils.selector.select` function.
        """
        return select(self, key)

    def get_item_cls(self):
        """Returns class reference of a single item class that this item
        works with.
        """
        raise NotImplementedError()

    def is_scoped(self):
        """ Returns `True` if the item class is scoped """
        raise NotImplementedError()

    def get_collection_id(self):
        """ Returns ID of the collection of the item. """
        raise NotImplementedError()

    # --- helper functions -----------------------------------------------------

    def pprint(self, as_json=True, revert=None, *args, **kwargs):
        """Pretty prints the item.

        :param as_json: If `True` (default), the a JSON representation of item
            is printed, otherwise dictionary representation is printed using
            `pprint` method from `pprint` module.
        :param revert: Convert all not JSON serializable values into
            serializable ones.
        :param \*args: These arguments passed to `pprint.pprint` function or to
            `json.dumps`.
        :param \**kwargs: These key-value arguments passed to `pprint.pprint`
            function or to `json.dumps`.
        """
        if revert is None:
            revert = as_json
        item_as_dict = self.to_dict(revert=revert)

        if not as_json:
            if "width" not in kwargs:
                kwargs["width"] = 80
            pprint(item_as_dict, *args, **kwargs)
        else:
            json_kwargs = {
                "ensure_ascii": False,
                "indent": 4,
                "sort_keys": True,
            }
            json_kwargs.update(kwargs)
            print(json.dumps(item_as_dict, *args, **json_kwargs))

    # --- main methods ---------------------------------------------------------

    def as_list(self):
        """Returns a list of items. For single items simply returns a list
        containing only `self`, for bulk items returns list of all items.
        """
        raise NotImplementedError()

    def is_single_item(self):
        """ Returns `True` if item is a single item. """
        raise NotImplementedError()

    def is_bulk_item(self):
        """ Returns `True` if item is a bulk item. """
        raise NotImplementedError()

    def revert(self):
        """Converts all field values into JSON serializable values in such a
        way that :py:meth:`~.process` method converts them bac to original
        values.
        """
        raise NotImplementedError()

    def process(self):
        """Converts all set values to the appropriate data types, sets default
        values if needed, calls :py:meth:`~.process()` method on all referenced
        items.

        :returns: Dictionary with single item classes as keys and lists of
            single item instances as values.
        """
        raise NotImplementedError()

    def delete(self):
        """ Deletes this item. """
        mapper.item_deleted(self)

    def clone(self):
        """ Deep copies item. """
        return copy.deepcopy(self)

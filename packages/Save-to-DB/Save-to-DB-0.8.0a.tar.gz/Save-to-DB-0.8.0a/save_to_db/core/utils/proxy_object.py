class ProxyObject(object):
    """ProxyObject allows to get contents of instances of
    :py:class:`~save_to_db.core.item_base.ItemBase` using dot notation. Example:

    .. code-block:: python
        :linenos:
        :emphasize-lines: 15

        # using item directly
        item_a = ItemA()
        item_a["field_x"] = 10
        item_a["item_b__field_z"] = 20

        # using proxy object and dot notation
        proxy_a = item_a.get_proxy()  # returns instance of `ProxyObject`
        proxy_a.field_x = 20
        proxy_a.item_b__field_z = 20
        proxy_a.item_b.field_z = 30  # overwrites previous value
        proxy_a["field_x"] = 20  # using as a dictionary is also possible

        # for reference (all prints `True`)
        print(proxy_a() is item_a)  # call proxy itself to get an item
        print(proxy_a.item_b() is item_a["item_b"])  # proxy returns proxy
        print(item_a.get_proxy() is proxy_a)  # always same proxy
        print(item_a["item_b"].get_proxy() is proxy_a.item_b)

    .. note::
        You can call proxy object itself to get the instance of item.

    .. seealso::
        :py:meth:`~save_to_db.core.item_base.ItemBase.get_proxy` method of
        :py:class:`~save_to_db.core.item_base.ItemBase`.

    :param item: An instance of :py:class:`~save_to_db.core.item_base.ItemBase` to
        be proxied.
    """

    EXCLUDE_START_KEY = "_ProxyObject__"

    def __init__(self, item):
        self.__item = item

    def __call__(self):
        return self.__item

    def __setitem__(self, key, value):
        if isinstance(value, ProxyObject):
            value = value()
        self.__item[key] = value

    def __setattr__(self, key, value):
        if key.startswith(self.EXCLUDE_START_KEY):
            self.__dict__[key] = value
        else:
            self.__setitem__(key, value)

    def __getitem__(self, key):
        from ..item_base import ItemBase

        result = self.__item[key]
        if isinstance(result, ItemBase):
            if result.proxy is None:
                result.proxy = ProxyObject(result)
            return result.proxy

        return result

    def __getattr__(self, key):
        if key.startswith(self.EXCLUDE_START_KEY):
            return self.__dict__[key]
        return self.__getitem__(key)

    def __delitem__(self, key):
        del self.__item[key]

    def __delattr__(self, key):
        self.__delitem__(key)

    def __contains__(self, key):
        return key in self.__item

    def __len__(self):
        return len(self.__item)

from save_to_db.adapters.utils.column_type import ColumnType
from save_to_db.core.item import Item
from save_to_db.core.bulk_item import BulkItem
from save_to_db.core.utils.proxy_object import ProxyObject
from save_to_db.utils.test_base import TestBase


class TestProxyObject(TestBase):
    def test_proxy_object_and_with_item(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo

        item_one = ItemGeneralOne(f_integer=1, two_x_1=ItemGeneralTwo(f_string="str-2"))
        item_one_proxy = item_one.get_proxy()

        # --- always the same proxy object ---
        self.assertIs(item_one_proxy, item_one.get_proxy())

        # --- get ---
        # f_integer
        self.assertIs(item_one_proxy(), item_one)
        self.assertTrue("f_integer" in item_one_proxy)
        self.assertEqual(item_one_proxy["f_integer"], 1)
        self.assertEqual(item_one_proxy.f_integer, 1)

        # two_x_1
        self.assertTrue("two_x_1" in item_one_proxy)
        self.assertIsInstance(item_one_proxy.two_x_1, ProxyObject)
        self.assertIs(item_one_proxy.two_x_1(), item_one["two_x_1"])

        # two_x_1.f_string
        self.assertTrue("f_string" in item_one_proxy.two_x_1)
        self.assertEqual(item_one_proxy.two_x_1.f_string, "str-2")
        self.assertEqual(item_one_proxy.two_x_1__f_string, "str-2")
        self.assertEqual(item_one_proxy["two_x_1__f_string"], "str-2")

        # two_x_1.one_1_x[0]
        self.assertTrue("one_1_x" in item_one_proxy.two_x_1)

        self.assertEqual(len(item_one_proxy.two_x_1.one_1_x), 1)
        self.assertEqual(len(item_one_proxy.two_x_1__one_1_x), 1)

        self.assertIsInstance(item_one_proxy.two_x_1.one_1_x(), BulkItem)
        self.assertIsInstance(item_one_proxy.two_x_1__one_1_x(), BulkItem)

        self.assertIs(item_one_proxy.two_x_1.one_1_x(), item_one["two_x_1__one_1_x"])
        self.assertIs(item_one_proxy.two_x_1__one_1_x(), item_one["two_x_1__one_1_x"])

        self.assertIs(item_one_proxy.two_x_1.one_1_x[0], item_one_proxy)
        self.assertIs(item_one_proxy.two_x_1__one_1_x[0], item_one_proxy)

        # --- contanes ---
        self.assertTrue("f_integer", item_one_proxy)
        self.assertTrue("two_x_1", item_one_proxy)
        self.assertTrue("two_x_1__one_1_x", item_one_proxy)

        # --- length ---
        self.assertEqual(len(item_one["two_x_1__one_1_x"]), 1)
        self.assertEqual(len(item_one_proxy["two_x_1__one_1_x"]), 1)

        item_one["two_x_1__one_1_x"].gen()

        self.assertEqual(len(item_one["two_x_1__one_1_x"]), 2)
        self.assertEqual(len(item_one_proxy["two_x_1__one_1_x"]), 2)

        item_one["two_x_1__one_1_x"].remove(item_one["two_x_1__one_1_x"][1])

        self.assertEqual(len(item_one["two_x_1__one_1_x"]), 1)
        self.assertEqual(len(item_one_proxy["two_x_1__one_1_x"]), 1)

        # -- set ---
        # f_integer
        item_one_proxy["f_integer"] = 10
        self.assertEqual(item_one["f_integer"], 10)
        item_one_proxy.f_integer = 100
        self.assertEqual(item_one["f_integer"], 100)

        # two_x_1.f_string
        item_one_proxy["two_x_1__f_string"] = "str-20"
        self.assertEqual(item_one["two_x_1__f_string"], "str-20")
        item_one_proxy.two_x_1.f_string = "str-200"
        self.assertEqual(item_one["two_x_1__f_string"], "str-200")
        item_one_proxy.two_x_1__f_string = "str-2000"
        self.assertEqual(item_one["two_x_1__f_string"], "str-2000")

        # two_x_1.one_1_x[0]
        old_bulk = item_one["two_x_1__one_1_x"]

        # undescore notation
        item_one_bulk_1 = ItemGeneralOne.Bulk()
        item_two = item_one["two_x_1"]
        item_two_proxy = item_one_proxy["two_x_1"]

        item_one_proxy["two_x_1__one_1_x"] = item_one_bulk_1
        # (mapper auto removes reverse relationship)
        self.assertNotIn("two_x_1", item_one)
        # checkins assingment through second item
        self.assertIs(item_two["one_1_x"], item_one_bulk_1)
        self.assertIs(item_two_proxy["one_1_x"](), item_one_bulk_1)

        # dot notation
        item_one_bulk_1 = ItemGeneralOne.Bulk()
        item_two = item_one["two_x_1"]
        item_two_proxy = item_one_proxy["two_x_1"]

        item_one_proxy.two_x_1.one_1_x = item_one_bulk_1
        # (mapper auto removes reverse relationship)
        self.assertNotIn("two_x_1", item_one)
        # checkins assingment through second item
        self.assertIs(item_two["one_1_x"], item_one_bulk_1)
        self.assertIs(item_two_proxy.one_1_x(), item_one_bulk_1)

        item_one["two_x_1__one_1_x"] = old_bulk

        # --- delete ---
        # f_integer
        del item_one_proxy["f_integer"]
        self.assertNotIn("f_integer", item_one_proxy)
        self.assertNotIn("f_integer", item_one)

        item_one_proxy["f_integer"] = 10
        del item_one_proxy.f_integer
        self.assertNotIn("f_integer", item_one_proxy)
        self.assertNotIn("f_integer", item_one)

        # two_x_1__one_1_x
        old_one_1_x_proxy = item_one_proxy["two_x_1__one_1_x"]
        item_two_proxy = item_one_proxy["two_x_1"]
        item_two = item_two_proxy()

        # underscore notation
        del item_one_proxy["two_x_1__one_1_x"]
        self.assertNotIn("one_1_x", item_two_proxy)
        self.assertNotIn("one_1_x", item_two)

        # dot noation
        item_one["two_x_1__one_1_x"] = old_bulk
        item_two_proxy = item_one_proxy["two_x_1"]
        item_two = item_two_proxy()
        self.assertIn("one_1_x", item_two_proxy)
        self.assertIn("one_1_x", item_two)
        del item_one_proxy.two_x_1.one_1_x
        self.assertNotIn("one_1_x", item_two_proxy)
        self.assertNotIn("one_1_x", item_two)

    def test_proxy_object_with_proxy_object(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo

        # --- underscore notation ---
        item_one = ItemGeneralOne()
        item_two = ItemGeneralTwo()

        item_one_proxy = item_one.get_proxy()
        item_two_proxy = item_two.get_proxy()

        # single item
        item_one_proxy["two_x_1"] = item_two_proxy
        self.assertIs(item_one["two_x_1"], item_two)

        # bulk item
        bulk_one = item_one.Bulk()
        bulk_one_proxy = bulk_one.get_proxy()
        item_two_proxy["one_1_x"] = bulk_one_proxy
        self.assertIs(item_two["one_1_x"], bulk_one)

        # --- dot notation ---
        item_one = ItemGeneralOne()
        item_two = ItemGeneralTwo()

        item_one_proxy = item_one.get_proxy()
        item_two_proxy = item_two.get_proxy()

        # single item
        item_one_proxy.two_x_1 = item_two_proxy
        self.assertIs(item_one["two_x_1"], item_two)

        # bulk item
        bulk_one = item_one.Bulk()
        bulk_one_proxy = bulk_one.get_proxy()
        item_two_proxy.one_1_x = bulk_one_proxy
        self.assertIs(item_two["one_1_x"], bulk_one)

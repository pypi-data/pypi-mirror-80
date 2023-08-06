from itertools import chain

from save_to_db.core.item import Item
from save_to_db.utils.test_base import TestBase
from save_to_db.exceptions import MergeItemsNotTheSame, MergeMultipleItemsMatch


class TestAllowMergeItems(TestBase):
    def test_allow_merge_items(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ["f_integer"]
            getters = ["f_integer"]
            allow_merge_items = True

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ["f_integer"]
            getters = ["f_integer"]
            allow_merge_items = True

        # item_one #1 (no merged in items)
        item_one_1 = ItemGeneralOne(f_integer="1000")

        # item_two #1 (1 merged in item)
        item_one_1["two_1_x"].gen(f_integer="1001", f_text="text-1")
        # item_two #2 mergable to #1
        item_two_2 = item_one_1["two_1_x"].gen(f_integer="1001", f_string="str-1")

        # item_one #2 (2 merged in items)
        item_two_2["one_x_x"].gen(f_integer="2001", f_text="text-2")
        # item_one #3 mergable to 2
        item_two_2["one_x_x"].gen(f_integer="2001", f_string="str-2")
        # item_one #4 mergable to 2
        item_two_2["one_x_x"].gen(f_integer="2001", f_float="2001.2001")

        # item_one #5 (no merged in items)
        item_two_2["one_x_x"].gen(f_integer="9999", f_string="str-9")

        item_one_1.process()

        # item_one #1
        self.assertEqual(item_one_1["f_integer"], 1000)

        # item_two #1
        two_1_x = item_one_1["two_1_x"]
        self.assertEqual(len(two_1_x), 1)
        self.assertEqual(two_1_x[0]["f_integer"], 1001)
        self.assertEqual(two_1_x[0]["f_text"], "text-1")
        self.assertEqual(two_1_x[0]["f_string"], "str-1")

        # item_one #2
        item_two_2 = item_one_1["two_1_x"][0]  # 'two_1_x' could be replaced
        one_x_x = item_two_2["one_x_x"]

        self.assertEqual(len(one_x_x), 2)
        self.assertEqual(one_x_x[0]["f_integer"], 2001)
        self.assertEqual(one_x_x[0]["f_text"], "text-2")  # item_one #2
        self.assertEqual(one_x_x[0]["f_string"], "str-2")  # item_one #3
        self.assertEqual(one_x_x[0]["f_float"], 2001.2001)  # item_one #4

        self.assertEqual(one_x_x[1]["f_integer"], 9999)
        self.assertEqual(one_x_x[1]["f_string"], "str-9")
        self.assertNotIn("f_text", one_x_x[1])
        self.assertNotIn("f_float", one_x_x[1])

        # merging at top level
        bulk_one = ItemGeneralOne.Bulk()
        bulk_one.gen(f_integer="1", f_string="str-1")
        bulk_one.gen(f_integer="1", f_text="text-1")
        bulk_one.process()

        self.assertEqual(len(bulk_one), 1)
        self.assertEqual(bulk_one[0]["f_integer"], 1)
        self.assertEqual(bulk_one[0]["f_string"], "str-1")
        self.assertEqual(bulk_one[0]["f_text"], "text-1")

        # merging default
        bulk_one = ItemGeneralOne.Bulk()
        item_one_1 = bulk_one.gen(f_integer="1")
        item_one_2 = bulk_one.gen(f_integer="1")

        item_one_1["two_x_1"](f_integer=200, f_string="str-1")
        item_one_2["two_x_1"](f_integer=200, f_text="text-1")

        bulk_one["two_x_1"] = ItemGeneralTwo(f_integer=200, f_float=200.200)

        bulk_one.process()

        self.assertEqual(len(bulk_one), 1)
        item_one = bulk_one[0]
        self.assertEqual(item_one["two_x_1__f_integer"], 200)
        self.assertEqual(item_one["two_x_1__f_string"], "str-1")
        self.assertEqual(item_one["two_x_1__f_text"], "text-1")
        self.assertEqual(item_one["two_x_1__f_float"], 200.200)

        # merge deep default single item
        bulk_one = ItemGeneralOne.Bulk()
        item_one_1 = bulk_one.gen(f_integer="1")

        item_one_1["two_x_1"](f_integer=200, f_string="str-1")

        bulk_one["two_x_1"] = ItemGeneralTwo(f_integer=300)
        bulk_one["two_x_1"]["one_x_x"].gen(
            two_x_1=ItemGeneralTwo(f_integer=200, f_text="deep")
        )

        bulk_one.process()

        self.assertEqual(item_one_1["f_integer"], 1)
        self.assertEqual(item_one_1["two_x_1__f_integer"], 200)
        self.assertEqual(item_one_1["two_x_1__f_string"], "str-1")
        self.assertEqual(item_one_1["two_x_1__f_text"], "deep")  # from default

        two_x_1 = bulk_one["two_x_1"]["one_x_x"][0]["two_x_1"]
        self.assertEqual(two_x_1["f_integer"], 200)
        self.assertEqual(two_x_1["f_text"], "deep")

        # default must be replaced
        self.assertIs(
            bulk_one["two_x_1"]["one_x_x"][0]["two_x_1"], item_one_1["two_x_1"]
        )

        # merge deep default in bulk item
        bulk_one = ItemGeneralOne.Bulk()
        bulk_one.gen(f_integer=100, f_string="str-1")
        bulk_one["two_x_1"]["one_x_x"].gen(f_integer=100, f_text="text-1")

        self.assertIsNot(bulk_one["two_x_1"]["one_x_x"][0], bulk_one[0])

        bulk_one.process()
        self.assertEqual(bulk_one[0]["f_integer"], 100)
        self.assertEqual(bulk_one[0]["f_string"], "str-1")
        self.assertEqual(bulk_one[0]["f_text"], "text-1")

        # default must be replaced
        self.assertIs(bulk_one["two_x_1"]["one_x_x"][0], bulk_one[0])
        self.assertIsNot(bulk_one["two_x_1"]["one_x_x"], bulk_one)

        # merge default bulk in bulk
        bulk_one = ItemGeneralOne.Bulk()
        item_one = bulk_one.gen(f_integer=100)
        item_one["two_x_1"](f_integer=200, f_string="str-1")
        bulk_one["two_x_x"].gen(f_integer=200, f_text="text-1")

        item_two_1 = bulk_one[0]["two_x_1"]
        item_two_2 = bulk_one["two_x_x"][0]

        self.assertIsNot(item_two_1, item_two_2)

        bulk_one.process()

        self.assertEqual(bulk_one[0]["two_x_1__f_integer"], 200)
        self.assertEqual(bulk_one[0]["two_x_1__f_string"], "str-1")
        self.assertEqual(bulk_one[0]["two_x_1__f_text"], "text-1")

        item_two_1 = bulk_one[0]["two_x_1"]
        item_two_2 = bulk_one["two_x_x"][0]

        self.assertIs(item_two_1, item_two_2)

        # two items + two items in bulk default and all must merged
        bulk_one = ItemGeneralOne.Bulk()
        bulk_one["parent_x_x"].add(ItemGeneralOne(f_integer=1, f_string="str-1"))
        bulk_one["parent_x_1"] = ItemGeneralOne(f_integer=1, f_text="text-1")

        bulk_one.gen(f_integer=1, f_float=2.0)
        bulk_one.gen(f_integer=1, f_boolean=True)

        bulk_one.process()

        self.assertEqual(len(bulk_one), 1)
        self.assertIs(bulk_one[0]["f_integer"], 1)
        self.assertIs(bulk_one[0]["f_string"], "str-1")
        self.assertIs(bulk_one[0]["f_text"], "text-1")
        self.assertIs(bulk_one[0]["f_float"], 2.0)
        self.assertIs(bulk_one[0]["f_boolean"], True)

        self.assertEqual(len(bulk_one[0]["parent_x_x"]), 1)
        self.assertIs(bulk_one[0]["parent_x_x"][0], bulk_one[0])
        self.assertEqual(len(bulk_one[0]["child_x_x"]), 1)
        self.assertIs(bulk_one[0]["child_x_x"][0], bulk_one[0])

        self.assertIs(bulk_one[0]["parent_x_1"], bulk_one[0])
        self.assertEqual(len(bulk_one[0]["child_1_x"]), 1)
        self.assertIs(bulk_one[0]["child_1_x"][0], bulk_one[0])

        # defaults
        self.assertEqual(len(bulk_one["parent_x_x"]), 1)
        self.assertIs(bulk_one["parent_x_x"][0], bulk_one[0])
        self.assertIs(bulk_one["parent_x_1"], bulk_one[0])

    def test_merge_bulk_items(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ["f_integer"]
            getters = ["f_integer"]

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ["f_integer"]
            getters = ["f_integer"]

        def gen_bulk_one():
            bulk_one = ItemGeneralOne.Bulk()
            bulk_one.gen(
                f_integer=1,
                two_x_x=[ItemGeneralTwo(f_integer=10), ItemGeneralTwo(f_integer=11)],
            )
            bulk_one.gen(
                f_integer=2,
                two_x_x=[ItemGeneralTwo(f_integer=11), ItemGeneralTwo(f_integer=12)],
            )
            return bulk_one

        bulk_one = gen_bulk_one()
        with self.assertRaises(MergeMultipleItemsMatch):
            bulk_one.process()

        ItemGeneralOne.allow_merge_items = True
        ItemGeneralTwo.allow_merge_items = True
        bulk_one = gen_bulk_one()
        bulk_one[0]["two_x_x"][1]["f_float"] = 1  # f_integer=11
        bulk_one[1]["two_x_x"][0]["f_float"] = 2  # f_integer=11

        with self.assertRaises(MergeItemsNotTheSame):
            bulk_one.process()

        bulk_one = gen_bulk_one()
        # both have f_integer=11
        self.assertIsNot(bulk_one[0]["two_x_x"][1], bulk_one[1]["two_x_x"][0])
        bulk_one.process()

        self.assertEqual(len(bulk_one[0]["two_x_x"]), 2)
        self.assertEqual(len(bulk_one[1]["two_x_x"]), 2)

        two_x_x = {
            item for item in chain(bulk_one[0]["two_x_x"], bulk_one[1]["two_x_x"])
        }
        self.assertEqual(len(two_x_x), 3)

    def test_item_bulk_and_content_merging(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ["f_integer"]
            getters = ["f_integer"]
            allow_merge_items = True

            def __repr__(self):
                return f"<One: {self['f_integer']}, ID={id(self)}>"

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ["f_integer"]
            getters = ["f_integer"]
            allow_merge_items = True

            def __repr__(self):
                return f"<Two: {self['f_integer']}, ID={id(self)}>"

        # one to one
        item_one_a = ItemGeneralOne(f_integer=101, f_string="str-1")
        item_one_a["two_1_1"](f_integer=202, f_string="str-2")

        item_one_b = ItemGeneralOne(f_integer=101, f_text="text-1")
        item_one_b["two_1_1"](f_integer=202, f_text="text-2")

        item_one_bulk = ItemGeneralOne.Bulk()
        item_one_bulk.add(item_one_a, item_one_b)

        item_one_bulk.process()

        self.assertEqual(len(item_one_bulk), 1)
        self.assertEqual(item_one_bulk[0]["f_integer"], 101)
        self.assertEqual(item_one_bulk[0]["f_string"], "str-1")
        self.assertEqual(item_one_bulk[0]["f_text"], "text-1")

        self.assertIs(item_one_bulk[0]["two_1_1__one_1_1"], item_one_bulk[0])
        self.assertEqual(item_one_bulk[0]["two_1_1__f_integer"], 202)
        self.assertEqual(item_one_bulk[0]["two_1_1__f_string"], "str-2")
        self.assertEqual(item_one_bulk[0]["two_1_1__f_text"], "text-2")

        # meny to one
        item_one_a = ItemGeneralOne(f_integer=1001, f_string="str-1")
        item_one_a["two_x_1"](f_integer=2002, f_string="str-2")

        item_one_b = ItemGeneralOne(f_integer=1001, f_text="text-1")
        item_one_b["two_x_1"](f_integer=2002, f_text="text-2")

        item_one_bulk = ItemGeneralOne.Bulk()
        item_one_bulk.add(item_one_a, item_one_b)

        item_one_bulk.process()

        self.assertEqual(len(item_one_bulk), 1)
        self.assertEqual(item_one_bulk[0]["f_integer"], 1001)
        self.assertEqual(item_one_bulk[0]["f_string"], "str-1")
        self.assertEqual(item_one_bulk[0]["f_text"], "text-1")

        self.assertEqual(len(item_one_bulk[0]["two_x_1__one_1_x"]), 1)
        self.assertIs(item_one_bulk[0]["two_x_1__one_1_x"][0], item_one_bulk[0])
        self.assertEqual(item_one_bulk[0]["two_x_1__f_integer"], 2002)
        self.assertEqual(item_one_bulk[0]["two_x_1__f_string"], "str-2")
        self.assertEqual(item_one_bulk[0]["two_x_1__f_text"], "text-2")

        # many to many
        item_one_a = ItemGeneralOne(f_integer=10001, f_string="str-1")
        item_one_a["two_x_x"].gen(f_integer=20002, f_string="str-2")

        item_one_b = ItemGeneralOne(f_integer=10001, f_text="text-1")
        item_one_b["two_x_x"].gen(f_integer=20002, f_text="text-2")

        item_one_bulk = ItemGeneralOne.Bulk()
        item_one_bulk.add(item_one_a, item_one_b)

        item_one_bulk.process()

        self.assertEqual(len(item_one_bulk), 1)
        self.assertEqual(item_one_bulk[0]["f_integer"], 10001)
        self.assertEqual(item_one_bulk[0]["f_string"], "str-1")
        self.assertEqual(item_one_bulk[0]["f_text"], "text-1")

        self.assertEqual(len(item_one_bulk[0]["two_x_x"][0]["one_x_x"]), 1)
        self.assertIs(item_one_bulk[0]["two_x_x"][0]["one_x_x"][0], item_one_bulk[0])
        self.assertEqual(item_one_bulk[0]["two_x_x"][0]["f_integer"], 20002)
        self.assertEqual(item_one_bulk[0]["two_x_x"][0]["f_string"], "str-2")
        self.assertEqual(item_one_bulk[0]["two_x_x"][0]["f_text"], "text-2")

    def test_merge_one_to_one_no_reverse_with_exception(self):
        self.item_cls_manager.autogenerate = True

        class ItemAutoReverseOne(Item):
            model_cls = self.ModelAutoReverseOne
            creators = ["f_integer"]
            getters = ["f_integer", "two_b_1_1"]
            allow_merge_items = True

        # does not have reverse relations
        class ItemAutoReverseTwoB(Item):
            model_cls = self.ModelAutoReverseTwoB
            creators = ["f_integer"]
            getters = ["f_integer"]
            allow_merge_items = True

        # does not have reverse relations
        class ItemAutoReverseThreeB(Item):
            model_cls = self.ModelAutoReverseThreeB
            creators = ["f_integer"]
            getters = ["f_integer"]
            allow_merge_items = True

        # --- parent allows merge ---
        # one-to-one
        ItemAutoReverseOne.allow_merge_items = True

        bulk_one = ItemAutoReverseOne.Bulk()
        bulk_one.gen(
            f_integer=1, two_b_1_1=ItemAutoReverseTwoB(f_integer=2, f_string="str-1")
        )
        bulk_one.gen(
            f_integer=3, two_b_1_1=ItemAutoReverseTwoB(f_integer=2, f_text="text-1")
        )

        with self.assertRaises(MergeMultipleItemsMatch):
            bulk_one.process()

        # --- parent does not allow merge ---
        # one-to-one
        ItemAutoReverseOne.allow_merge_items = False

        bulk_one = ItemAutoReverseOne.Bulk()
        bulk_one.gen(
            f_integer=1, two_b_1_1=ItemAutoReverseTwoB(f_integer=2, f_string="str-1")
        )
        bulk_one.gen(
            f_integer=3, two_b_1_1=ItemAutoReverseTwoB(f_integer=2, f_text="text-1")
        )

        with self.assertRaises(MergeMultipleItemsMatch):
            bulk_one.process()

    def test_merge_one_to_one_with_reverse_with_exception(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ["f_integer"]
            getters = ["f_integer", "two_1_1"]
            allow_merge_items = True

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ["f_integer"]
            getters = ["f_integer", "one_1_1"]
            allow_merge_items = True

        # --- parent allows merge ---
        # one-to-one
        ItemGeneralOne.allow_merge_items = True

        bulk_one = ItemGeneralOne.Bulk()
        bulk_one.gen(f_integer=1, two_1_1=ItemGeneralTwo(f_integer=2, f_string="str-1"))
        bulk_one.gen(f_integer=3, two_1_1=ItemGeneralTwo(f_integer=2, f_text="text-1"))

        with self.assertRaises(MergeMultipleItemsMatch):
            bulk_one.process()

        # --- parent does not allow merge ---
        # one-to-one
        ItemGeneralOne.allow_merge_items = False

        bulk_one = ItemGeneralOne.Bulk()
        bulk_one.gen(f_integer=1, two_1_1=ItemGeneralTwo(f_integer=2, f_string="str-1"))
        bulk_one.gen(f_integer=3, two_1_1=ItemGeneralTwo(f_integer=2, f_text="text-1"))

        with self.assertRaises(MergeMultipleItemsMatch):
            bulk_one.process()

    def test_merging_items_point_each_other(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            creators = ["f_integer"]
            getters = ["f_integer"]
            getters_autoconfig = True
            allow_merge_items = True

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            creators = ["f_integer"]
            getters = ["f_integer"]
            getters_autoconfig = True
            allow_merge_items = True

        # many-to-many
        item_one = ItemGeneralOne(f_integer=1, parent_x_x=[ItemGeneralOne(f_integer=1)])
        item_one.process()

        self.assertEqual(len(item_one["parent_x_x"]), 1)
        self.assertEqual(len(item_one["parent_x_x"][0]["child_x_x"]), 1)
        self.assertIs(
            item_one["parent_x_x"][0], item_one["parent_x_x"][0]["child_x_x"][0]
        )

        # many-to-one
        item_one = ItemGeneralOne(f_integer=1, parent_x_1=ItemGeneralOne(f_integer=1))
        item_one.process()

        self.assertIs(item_one["parent_x_1"], item_one["parent_x_1"]["child_1_x"][0])
        self.assertEqual(len(item_one["parent_x_1"]["child_1_x"]), 1)

        # one-to-one
        item_one = ItemGeneralOne(f_integer=1, parent_1_1=ItemGeneralOne(f_integer=1))
        item_one.process()

        self.assertIs(item_one["parent_1_1"], item_one["parent_1_1"]["child_1_1"])

        # one-to-many
        item_one = ItemGeneralOne(f_integer=1, child_1_x=[ItemGeneralOne(f_integer=1)])
        item_one.process()

        self.assertEqual(len(item_one["child_1_x"]), 1)
        self.assertIs(item_one["child_1_x"][0], item_one["parent_x_1"])

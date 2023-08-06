import copy
from itertools import chain
from save_to_db.core.item import Item
from save_to_db.utils.test_base import TestBase


class TestItemCopy(TestBase):
    def test_deepcopy_single_item(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo

        parent_x_x = ItemGeneralOne.Bulk(f_boolean="+")
        parent_x_x.add(ItemGeneralOne(f_string="parent_x_x-1", f_integer="991"))
        parent_x_x.add(
            ItemGeneralOne(
                f_string="parent_x_x-2",
                f_integer="992",
            )
        )

        child_1_x = ItemGeneralOne.Bulk(f_boolean="+")
        child_1_x.add(ItemGeneralOne(f_string="child_1_x-1", f_integer="911"))
        child_1_x.add(
            ItemGeneralOne(
                f_string="child_1_x-2",
                f_integer="912",
            )
        )

        two_1_x = ItemGeneralTwo.Bulk(f_boolean="+")
        two_1_x.add(ItemGeneralTwo(f_string="two_1_x-1", f_integer="191"))
        two_1_x.add(ItemGeneralTwo(f_string="two_1_x-2", f_integer="192"))

        two_x_x = ItemGeneralTwo.Bulk(f_boolean="+")
        two_x_x.add(ItemGeneralTwo(f_string="two_x_x-1", f_integer="991"))
        two_x_x.add(ItemGeneralTwo(f_string="two_x_x-2", f_integer="992"))

        item_one = ItemGeneralOne(
            f_integer="1",
            f_string="self",
            # ItemGeneralOne
            parent_1_1=ItemGeneralOne(
                f_integer="11",
                f_string="parent_1_1",
            ),
            parent_x_1=ItemGeneralOne(f_string="parent_x_1", f_integer="91"),
            child_1_x=child_1_x,
            parent_x_x=parent_x_x,
            # ItemGeneralTwo
            two_1_1=ItemGeneralTwo(f_string="two_1_1", f_integer="11"),
            two_x_1=ItemGeneralTwo(f_string="two_x_1", f_integer="91"),
            two_1_x=two_1_x,
            two_x_x=two_x_x,
        )
        item_one_copy = copy.deepcopy(item_one)

        # making sure items were copied
        self.assertIsNot(item_one, item_one_copy)

        # direct items
        self.assertIsNot(item_one["parent_1_1"], item_one_copy["parent_1_1"])
        self.assertIsNot(item_one["parent_x_1"], item_one_copy["parent_x_1"])
        self.assertIsNot(item_one["child_1_x"], item_one_copy["child_1_x"])
        self.assertIsNot(item_one["parent_x_x"], item_one_copy["parent_x_x"])

        self.assertIsNot(item_one["two_1_1"], item_one_copy["two_1_1"])
        self.assertIsNot(item_one["two_x_1"], item_one_copy["two_x_1"])
        self.assertIsNot(item_one["two_1_x"], item_one_copy["two_1_x"])
        self.assertIsNot(item_one["two_x_x"], item_one_copy["two_x_x"])

        # bulk items
        self.assertEqual(len(item_one["child_1_x"]), 2)
        self.assertEqual(len(item_one["child_1_x"]), len(item_one_copy["child_1_x"]))
        self.assertEqual(len(item_one["parent_x_x"]), 2)
        self.assertEqual(len(item_one["parent_x_x"]), len(item_one_copy["parent_x_x"]))
        self.assertEqual(len(item_one["two_1_x"]), 2)
        self.assertEqual(len(item_one["two_1_x"]), len(item_one_copy["two_1_x"]))
        self.assertEqual(len(item_one["two_x_x"]), 2)
        self.assertEqual(len(item_one["two_x_x"]), len(item_one_copy["two_x_x"]))
        for item_a, item_b in chain(
            zip(item_one["child_1_x"], item_one_copy["child_1_x"]),
            zip(item_one["parent_x_x"], item_one_copy["parent_x_x"]),
            zip(item_one["two_1_x"], item_one_copy["two_1_x"]),
            zip(item_one["two_x_x"], item_one_copy["two_x_x"]),
        ):
            self.assertIsNot(item_a, item_b)

        self.assertEqual(item_one.to_dict(), item_one_copy.to_dict())

        item_one.process()
        self.assertNotEqual(item_one.to_dict(), item_one_copy.to_dict())

        item_one_copy.process()
        self.assertEqual(item_one.to_dict(), item_one_copy.to_dict())

    def test_deepcopy_bulk_item(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo

        # --- testing bulk items ---
        bulk_item = ItemGeneralOne.Bulk()
        bulk_item.gen(f_integer="1")
        bulk_item.gen(f_integer="2")

        bulk_item_copy = copy.deepcopy(bulk_item)

        # bulk itself
        self.assertIsNot(bulk_item, bulk_item_copy)

        # items in bulk
        self.assertEqual(len(bulk_item), 2)
        self.assertEqual(len(bulk_item), len(bulk_item_copy))
        for item_a, item_b in zip(bulk_item, bulk_item_copy):
            self.assertIsNot(item_a, item_b)

        # --- testing defaults ---

        parent_x_x = ItemGeneralOne.Bulk(f_boolean="+")
        parent_x_x.add(ItemGeneralOne(f_string="parent_x_x-1", f_integer="991"))
        parent_x_x.add(
            ItemGeneralOne(
                f_string="parent_x_x-2",
                f_integer="992",
            )
        )

        two_x_x = ItemGeneralTwo.Bulk(f_boolean="+")
        two_x_x.add(ItemGeneralTwo(f_string="two_x_x-1", f_integer="991"))
        two_x_x.add(ItemGeneralTwo(f_string="two_x_x-2", f_integer="992"))

        bulk_item = ItemGeneralOne.Bulk(
            f_string="self",
            f_integer="1",
            parent_x_1=ItemGeneralOne(f_string="parent_x_1", f_integer="91"),
            parent_x_x=parent_x_x,
            two_x_1=ItemGeneralTwo(f_string="two_x_1", f_integer="91"),
            two_x_x=two_x_x,
        )

        bulk_item_copy = copy.deepcopy(bulk_item)

        # making sure items were copied
        self.assertIsNot(bulk_item, bulk_item_copy)

        # direct items
        self.assertIsNot(bulk_item["parent_x_1"], bulk_item_copy["parent_x_1"])
        self.assertIsNot(bulk_item["parent_x_x"], bulk_item_copy["parent_x_x"])
        self.assertIsNot(bulk_item["two_x_1"], bulk_item_copy["two_x_1"])
        self.assertIsNot(bulk_item["two_x_x"], bulk_item_copy["two_x_x"])

        # bulk items
        self.assertEqual(len(bulk_item["parent_x_x"]), 2)
        self.assertEqual(
            len(bulk_item["parent_x_x"]), len(bulk_item_copy["parent_x_x"])
        )
        self.assertEqual(len(bulk_item["two_x_x"]), 2)
        self.assertEqual(len(bulk_item["two_x_x"]), len(bulk_item_copy["two_x_x"]))

        for item_a, item_b in chain(
            zip(bulk_item["parent_x_x"], bulk_item_copy["parent_x_x"]),
            zip(bulk_item["two_x_x"], bulk_item_copy["two_x_x"]),
        ):
            self.assertIsNot(item_a, item_b)

        self.assertEqual(bulk_item.to_dict(), bulk_item_copy.to_dict())

        bulk_item.process()
        self.assertNotEqual(bulk_item.to_dict(), bulk_item_copy.to_dict())

        bulk_item_copy.process()
        self.assertEqual(bulk_item.to_dict(), bulk_item_copy.to_dict())

    def test_shellow_copy_not_implemented(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo

        # single item
        item_one = ItemGeneralOne()
        with self.assertRaises(NotImplementedError) as context_one:
            copy.copy(item_one)
        self.assertEqual(str(context_one.exception), "Please user deepcopy")

        # bulk item
        bulk_item_two = ItemGeneralTwo.Bulk()
        with self.assertRaises(NotImplementedError) as context_two:
            copy.copy(bulk_item_two)
        self.assertEqual(str(context_two.exception), "Please user deepcopy")

    def test_simple_clone(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo

        # single item
        item_one = ItemGeneralOne()
        item_one_clone = item_one.clone()
        self.assertIsNot(item_one, item_one_clone)

        # bulk item
        bulk_item_two = ItemGeneralTwo.Bulk()
        bulk_item_two_clone = bulk_item_two.clone()
        self.assertIsNot(bulk_item_two, bulk_item_two_clone)

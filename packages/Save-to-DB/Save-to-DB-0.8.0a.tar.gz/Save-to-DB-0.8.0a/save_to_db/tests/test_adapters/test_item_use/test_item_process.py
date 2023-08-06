import datetime
from collections import OrderedDict

from save_to_db.core.item import Item
from save_to_db.utils.test_base import TestBase
from save_to_db.exceptions import ItemProcessError, ItemRevertError


class TestItemProcess(TestBase):
    @classmethod
    def setup_models(cls, aliased=False):
        cls.item_cls_manager.clear()

        class ItemFieldTypes(Item):
            model_cls = cls.ModelFieldTypes
            conversions = {
                "decimal_separator": ",",
            }

        cls.ItemFieldTypes = ItemFieldTypes

        dct_1 = {"model_cls": cls.ModelGeneralOne}
        dct_2 = {"model_cls": cls.ModelGeneralTwo}

        if aliased:
            dct_1.update(
                {
                    "aliases": {
                        "alias_1": "two_1_1__f_integer",
                        "alias_2": "two_x_x__one_1_1__f_integer",
                    }
                }
            )
            dct_2.update(
                {
                    "aliases": {
                        "alias_1__post": "f_string",
                        "alias_2__post": "one_x_1__alias_1",
                        "alias_3__post": "one_x_x__two_1_x__alias_1__post",
                    }
                }
            )

        cls.ItemGeneralOne = type("ItemGeneralOne", (Item,), dct_1)
        cls.ItemGeneralTwo = type("ItemGeneralTwo", (Item,), dct_2)

        cls.ItemGeneralOne.complete_setup()
        cls.ItemGeneralTwo.complete_setup()

    def test_field_convesion_funcs(self):
        date_one = datetime.date(2010, 10, 20)
        date_two = datetime.date(2011, 10, 20)
        date_three = datetime.date(2012, 10, 20)

        time_one = datetime.time(10, 20, 30)
        time_two = datetime.time(10, 20, 40)
        time_three = datetime.time(10, 20, 50)

        datetime_one = datetime.datetime(2010, 10, 20, 10, 20, 30)
        datetime_two = datetime.datetime(2011, 10, 20, 10, 20, 40)
        datetime_three = datetime.datetime(2012, 10, 20, 10, 20, 50)

        class ItemFieldTypes(Item):
            model_cls = self.ModelFieldTypes
            conversions = {
                "date_func": lambda value: {1: date_one, 2: date_two, 3: "2012-10-20"}[
                    value
                ],
                "time_func": lambda value: {1: time_one, 2: time_two, 3: "10:20:50"}[
                    value
                ],
                "datetime_func": lambda value: {
                    1: datetime_one,
                    2: datetime_two,
                    3: "2012-10-20 10:20:50",
                }[value],
            }

        # --- first case ---
        item = ItemFieldTypes(date_1=1, time_1=1, datetime_1=1)

        # no change
        dict_data = item.to_dict()
        expected_dict_data = {"item": {"date_1": 1, "datetime_1": 1, "time_1": 1}}
        self.assertEqual(dict_data, expected_dict_data)

        # process
        item.process()
        dict_data = item.to_dict()
        expected_dict_data = {
            "item": {
                "date_1": datetime.date(2010, 10, 20),
                "datetime_1": datetime.datetime(2010, 10, 20, 10, 20, 30),
                "time_1": datetime.time(10, 20, 30),
            }
        }
        self.assertEqual(dict_data, expected_dict_data)

        # revert
        item.revert()
        dict_data = item.to_dict()
        expected_dict_data = {
            "item": {
                "date_1": "2010-10-20",
                "datetime_1": "2010-10-20 10:20:30",
                "time_1": "10:20:30",
            }
        }
        self.assertEqual(dict_data, expected_dict_data)

        # process after reverted
        item.process()
        dict_data = item.to_dict()
        expected_dict_data = {
            "item": {
                "date_1": datetime.date(2010, 10, 20),
                "datetime_1": datetime.datetime(2010, 10, 20, 10, 20, 30),
                "time_1": datetime.time(10, 20, 30),
            }
        }
        self.assertEqual(dict_data, expected_dict_data)

        # --- second case ---
        item = ItemFieldTypes(date_1=2, time_1=2, datetime_1=2)
        item.process()
        self.assertEqual(item["date_1"], date_two)
        self.assertEqual(item["time_1"], time_two)
        self.assertEqual(item["datetime_1"], datetime_two)

        item = ItemFieldTypes(date_1=3, time_1=3, datetime_1=3)
        item.process()
        self.assertEqual(item["date_1"], date_three)
        self.assertEqual(item["time_1"], time_three)
        self.assertEqual(item["datetime_1"], datetime_three)

        # --- third case ---
        item = ItemFieldTypes(date_1=1, time_1=2, datetime_1=3)

        # no change
        dict_data = item.to_dict()
        expected_dict_data = {"item": {"date_1": 1, "datetime_1": 3, "time_1": 2}}
        self.assertEqual(dict_data, expected_dict_data)

        # processed
        item.process()
        dict_data = item.to_dict()
        expected_dict_data = {
            "item": {
                "date_1": datetime.date(2010, 10, 20),
                "datetime_1": datetime.datetime(2012, 10, 20, 10, 20, 50),
                "time_1": datetime.time(10, 20, 40),
            }
        }
        self.assertEqual(dict_data, expected_dict_data)

        # revert
        item.revert()
        dict_data = item.to_dict()
        expected_dict_data = {
            "item": {
                "date_1": "2010-10-20",
                "datetime_1": "2012-10-20 10:20:50",
                "time_1": "10:20:40",
            }
        }
        self.assertEqual(dict_data, expected_dict_data)

        # process after reverted
        item.process()
        dict_data = item.to_dict()
        expected_dict_data = {
            "item": {
                "date_1": datetime.date(2010, 10, 20),
                "datetime_1": datetime.datetime(2012, 10, 20, 10, 20, 50),
                "time_1": datetime.time(10, 20, 40),
            }
        }
        self.assertEqual(dict_data, expected_dict_data)

    def test_field_convesion_no_funcs(self):
        self.setup_models()

        # --- simple conversion ---
        item = self.ItemFieldTypes(
            binary_1="binary data",
            string_1=1000,
            text_1=2000,
            integer_1="10",
            boolean_1="TRUE",
            float_1="1.120,30",  # with comma as decimal separator and a dot
            date_1="2000-10-30",
            time_1="20:30:40",
            datetime_1="2000-10-30 20:30:40",
        )

        item.process()

        expected_value = {
            "binary_1": b"binary data",
            "boolean_1": True,
            "date_1": datetime.date(2000, 10, 30),
            "datetime_1": datetime.datetime(2000, 10, 30, 20, 30, 40),
            "float_1": 1120.3,
            "integer_1": 10,
            "string_1": "1000",
            "text_1": "2000",
            "time_1": datetime.time(20, 30, 40),
        }
        for key, value in expected_value.items():
            self.assertEqual(item[key], value)

        item.process()  # second processing does nothing

        # --- conversions with relations ---
        item = self.ItemGeneralOne(
            f_integer="10", two_x_1__f_integer="20", two_x_x__f_integer="30"
        )
        item["two_x_x"].gen(f_integer="40")
        item.process()

        self.assertEqual(item["f_integer"], 10)
        self.assertEqual(item["two_x_1__f_integer"], 20)
        self.assertEqual(item["two_x_x__f_integer"], 30)
        self.assertEqual(item["two_x_x"][0]["f_integer"], 40)

    def test_inject_nullables(self):
        self.setup_models()

        self.item_cls_manager.clear()

        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            # using normal fields
            nullables = ["f_integer", "f_string"]

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            # using relations
            nullables = ["one_1_1", "one_x_1", "one_1_x", "one_x_x"]

        # no overwrite for normal fields
        item = ItemGeneralOne(f_integer="10", f_string="20", f_text="30")
        item.process()
        self.assertEqual(item["f_integer"], 10)
        self.assertEqual(item["f_string"], "20")
        self.assertEqual(item["f_text"], "30")

        # normal fields nullables added
        item = ItemGeneralOne()
        item.process()
        self.assertIsNone(item["f_integer"])
        self.assertIsNone(item["f_string"])
        with self.assertRaises(KeyError):
            item["f_text"]

        # no overwrite for relations
        item = ItemGeneralTwo(
            one_1_1__f_integer="10",
            one_1_1__f_string="20",
            one_x_1__f_integer="10",
            one_x_1__f_string="20",
        )
        item["one_1_x"].gen(f_integer="10", f_string="20")
        item["one_x_x"].gen(f_integer="10", f_string="20")
        item.process()

        self.assertEqual(item["one_1_1"]["f_integer"], 10)
        self.assertEqual(item["one_1_1"]["f_string"], "20")
        self.assertEqual(item["one_x_1"]["f_integer"], 10)
        self.assertEqual(item["one_x_1"]["f_string"], "20")

        for key in ["one_1_x", "one_x_x"]:
            for item_one in item[key]:
                self.assertEqual(item_one["f_integer"], 10)
                self.assertEqual(item_one["f_string"], "20")

        # relation fields nullables added
        item = ItemGeneralTwo()
        item.process()

        for key in ["one_1_1", "one_x_1", "one_1_x", "one_x_x"]:
            self.assertIn(key, item)

        self.assertIsNone(item["one_1_1"])
        self.assertIsNone(item["one_x_1"])

        self.assertEqual(len(item["one_1_x"]), 0)
        self.assertEqual(len(item["one_x_x"]), 0)

    def test_aliases_process(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            aliases = {
                "alias_1": "two_x_1__f_integer",
                "alias_2": "two_x_x__f_integer",
            }

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            aliases = {
                "alias_1__post": "f_float",
                "alias_2__post": "one_x_1__alias_1",
                "alias_3__post": "one_x_x__two_x_1__alias_1__post",
            }

        ItemGeneralOne.complete_setup()
        ItemGeneralTwo.complete_setup()

        # processing individual fields
        value = ItemGeneralOne.process_field("alias_1", "1")
        self.assertEqual(value, 1)

        value = ItemGeneralTwo.process_field("alias_1__post", "3.3")
        self.assertEqual(value, 3.3)
        value = ItemGeneralTwo.process_field("alias_2__post", "4")
        self.assertEqual(value, 4)
        value = ItemGeneralTwo.process_field("alias_3__post", "5.5")
        self.assertEqual(value, 5.5)

        # processing items
        item = ItemGeneralOne(
            alias_1="1",
            alias_2="2",
            two_1_1__alias_1__post="3.3",
            two_1_1__alias_2__post="5",
            two_1_1__alias_3__post="5.5",
        )
        item.process()

        self.assertEqual(item["alias_1"], 1)
        self.assertEqual(item["alias_2"], 2)
        self.assertEqual(item["two_x_1__f_integer"], 1)
        self.assertEqual(item["two_x_x__f_integer"], 2)

        two_1_1 = item["two_1_1"]
        self.assertEqual(two_1_1["alias_1__post"], 3.3)
        self.assertEqual(two_1_1["alias_2__post"], 5)
        self.assertEqual(two_1_1["alias_3__post"], 5.5)

        self.assertEqual(two_1_1["f_float"], 3.3)
        self.assertEqual(two_1_1["one_x_1__two_x_1__f_integer"], 5)
        self.assertEqual(two_1_1["one_x_x__two_x_1__f_float"], 5.5)

        bulk = ItemGeneralOne.Bulk()
        # generating same item as before
        bulk.gen(
            alias_1="1",
            alias_2="2",
            two_1_1__alias_1__post="3.3",
            two_1_1__alias_2__post="5",
            two_1_1__alias_3__post="5.5",
        )

        # two_1_1__alias_2__post
        bulk["two_1_1__one_x_1__two_x_1__f_integer"] = "6"
        # two_x_1__one_x_x__two_x_1__f_float
        bulk["two_x_1__alias_3__post"] = "6.6"
        bulk.process()

        self.assertEqual(bulk["two_1_1__alias_2__post"], 6)
        self.assertEqual(bulk["two_x_1__alias_3__post"], 6.6)

        self.assertEqual(bulk["two_1_1__one_x_1__two_x_1__f_integer"], 6)
        self.assertEqual(bulk["two_x_1__one_x_x__two_x_1__f_float"], 6.6)

        item = bulk[0]

        self.assertEqual(item["alias_1"], 1)
        self.assertEqual(item["alias_2"], 2)
        self.assertEqual(item["two_x_1__f_integer"], 1)
        self.assertEqual(item["two_x_x__f_integer"], 2)

        self.assertEqual(item["two_1_1__alias_1__post"], 3.3)
        self.assertEqual(item["two_1_1__alias_2__post"], 5)
        self.assertEqual(item["two_1_1__alias_3__post"], 5.5)
        self.assertEqual(item["two_x_1__alias_3__post"], 6.6)

        self.assertEqual(item["two_1_1__f_float"], 3.3)
        self.assertEqual(item["two_1_1__one_x_1__two_x_1__f_integer"], 5)
        self.assertEqual(item["two_1_1__one_x_x__two_x_1__f_float"], 5.5)
        self.assertEqual(item["two_x_1__one_x_x__two_x_1__f_float"], 6.6)

    def test_inject_bulk_defaults(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            # using normal fields
            nullables = ["f_integer", "f_string"]

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            # using relations
            nullables = ["one_x_1", "one_x_x"]

        # default regular fields
        # (first default fields must be injected only then nullables)
        bulk = ItemGeneralOne.Bulk(f_integer="1000", f_text="text-value")
        bulk.gen(f_integer="10", f_float="20.30")
        bulk.gen(f_string="str-value", f_float="20.30")
        bulk.process()
        expect = {
            "bulk": [
                {
                    "item": {
                        "f_float": 20.3,
                        "f_integer": 10,
                        "f_string": None,
                        "f_text": "text-value",
                    }
                },
                {
                    "item": {
                        "f_float": 20.3,
                        "f_integer": 1000,
                        "f_string": "str-value",
                        "f_text": "text-value",
                    }
                },
            ],
            "defaults": {"f_integer": 1000, "f_text": "text-value"},
        }
        self.assertEqual(bulk.to_dict(), expect)

        # default relations
        # many-to-many using item
        default_two_x_1 = ItemGeneralTwo(f_integer="10", f_float="20.30")
        default_two_x_x = ItemGeneralTwo.Bulk()
        default_two_x_x.gen(f_integer="20")
        default_two_x_x.gen(f_float="40.50")

        bulk = ItemGeneralOne.Bulk(two_x_1=default_two_x_1, two_x_x=default_two_x_x)
        bulk.gen(two_x_1__f_integer=40)
        bulk.gen(two_x_x__f_text="text-value")
        bulk.process()
        expect = {
            "bulk": [
                # first item: `bulk.gen(two_x_1__f_integer=40)`
                # + nullables + defaults
                {
                    "id": 1,
                    "item": {
                        "f_integer": None,
                        "f_string": None,
                        "two_x_1": {
                            "item": {
                                "f_integer": 40,
                                "one_1_x": {"bulk": [{"id": 1}], "defaults": {}},
                                "one_x_1": None,
                                "one_x_x": {"bulk": [], "defaults": {}},
                            }
                        },
                        # `default_two_x_x = ItemGeneralTwo.Bulk()` with two
                        # items:
                        # `default_two_x_x.gen(f_integer='20')` and
                        # `default_two_x_x.gen(f_float='40.50')` + nullables
                        "two_x_x": {
                            "bulk": [
                                {
                                    "item": {
                                        "f_integer": 20,
                                        "one_x_1": None,
                                        "one_x_x": {
                                            "bulk": [{"id": 1}],
                                            "defaults": {},
                                        },
                                    }
                                },
                                {
                                    "item": {
                                        "f_float": 40.5,
                                        "one_x_1": None,
                                        "one_x_x": {
                                            "bulk": [{"id": 1}],
                                            "defaults": {},
                                        },
                                    }
                                },
                            ],
                            "defaults": {},
                        },
                    },
                },
                {
                    "id": 2,
                    "item": {
                        "f_integer": None,
                        "f_string": None,
                        # `ItemGeneralTwo(f_integer='10', f_float='20.30')`
                        # + nullables
                        "two_x_1": {
                            "item": {
                                "f_float": 20.3,
                                "f_integer": 10,
                                "one_1_x": {"bulk": [{"id": 2}], "defaults": {}},
                                "one_x_1": None,
                                "one_x_x": {"bulk": [], "defaults": {}},
                            }
                        },
                        # already existed
                        "two_x_x": {"bulk": [], "defaults": {"f_text": "text-value"}},
                    },
                },
            ],
            "defaults": {
                "two_x_1": {
                    "item": {
                        "f_float": 20.3,
                        "f_integer": 10,
                        "one_x_1": None,
                        "one_x_x": {"bulk": [], "defaults": {}},
                    }
                },
                "two_x_x": {
                    "bulk": [
                        {
                            "item": {
                                "f_integer": 20,
                                "one_x_1": None,
                                "one_x_x": {"bulk": [], "defaults": {}},
                            }
                        },
                        {
                            "item": {
                                "f_float": 40.5,
                                "one_x_1": None,
                                "one_x_x": {"bulk": [], "defaults": {}},
                            }
                        },
                    ],
                    "defaults": {},
                },
            },
        }
        self.assertTrue(bulk.to_dict(), expect)

        # many-to-many using list value
        bulk = ItemGeneralOne.Bulk(
            two_x_1=default_two_x_1, two_x_x=default_two_x_x.as_list()
        )
        bulk.gen(two_x_1__f_integer=40)
        bulk.gen(two_x_x__f_text="text-value")
        bulk.process()
        self.assertTrue(bulk.to_dict(), expect)

    def test_plain_defaults_injection(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            defaults = {
                "f_integer": "100",
                "f_boolean": "true",
                "f_string": lambda item: "INT: {}".format(item["f_integer"]),
            }

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo

        item = ItemGeneralOne(f_integer="400")
        item.process()
        self.assertEqual(item["f_integer"], 400)
        self.assertIs(item["f_boolean"], True)
        self.assertEqual(item["f_string"], "INT: 400")

        item = ItemGeneralOne(f_boolean="false")
        item.process()
        self.assertEqual(item["f_integer"], 100)
        self.assertIs(item["f_boolean"], False)
        self.assertEqual(item["f_string"], "INT: 100")

    def test_item_defaults_injection(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo

        # regular default values -----------------------------------------------
        default_bulk = ItemGeneralOne.Bulk()
        default_bulk.add(ItemGeneralOne(f_float="19.1"), ItemGeneralOne(f_float="19.2"))
        ItemGeneralTwo.defaults.update(
            {
                "one_1_x": default_bulk,  # as bulk
                "one_x_x": [
                    ItemGeneralOne(f_float="99.1"),
                    ItemGeneralOne(f_float="99.2"),
                ],  # as list
            }
        )

        item_two = ItemGeneralTwo(f_float="2")
        item_two.process()

        # making sure that all items were processed (converted to float)
        self.assertEqual(item_two["f_float"], 2)
        self.assertEqual(item_two["one_1_x"][0]["f_float"], 19.1)
        self.assertEqual(item_two["one_1_x"][1]["f_float"], 19.2)
        self.assertEqual(item_two["one_x_x"][0]["f_float"], 99.1)
        self.assertEqual(item_two["one_x_x"][1]["f_float"], 99.2)

        # must not be overwritten with default
        item_two = ItemGeneralTwo(
            f_float="2.2",
            one_1_x=[ItemGeneralOne(f_float="19.12"), ItemGeneralOne(f_float="19.22")],
        )
        item_two["one_x_x"].add(
            ItemGeneralOne(f_float="99.12"), ItemGeneralOne(f_float="99.22")
        )
        item_two.process()
        self.assertEqual(item_two["f_float"], 2.2)
        self.assertEqual(item_two["one_1_x"][0]["f_float"], 19.12)
        self.assertEqual(item_two["one_1_x"][1]["f_float"], 19.22)
        self.assertEqual(item_two["one_x_x"][0]["f_float"], 99.12)
        self.assertEqual(item_two["one_x_x"][1]["f_float"], 99.22)

        # function default values ----------------------------------------------
        def gen_bulk_item(_):
            bulk_two = ItemGeneralTwo.Bulk()
            bulk_two.gen(f_float="99.1")
            bulk_two.gen(f_float="99.2")
            return bulk_two

        default_bulk = ItemGeneralTwo.Bulk()
        default_bulk.add(ItemGeneralTwo(f_float="19.1"), ItemGeneralTwo(f_float="19.2"))
        ItemGeneralTwo.defaults.clear()
        ItemGeneralOne.defaults.update(
            {
                "two_1_x": lambda _: default_bulk.as_list(),  # as list
                "two_x_x": gen_bulk_item,  # as item
            }
        )

        default_bulk.add(ItemGeneralTwo(f_float="19.1"))

        item_one = ItemGeneralOne(f_float="1")

        item_one.process()

        # making sure that all items were processed (converted to float)
        self.assertEqual(item_one["f_float"], 1)
        self.assertEqual(item_one["two_1_x"][0]["f_float"], 19.1)
        self.assertEqual(item_one["two_1_x"][1]["f_float"], 19.2)
        self.assertEqual(item_one["two_x_x"][0]["f_float"], 99.1)
        self.assertEqual(item_one["two_x_x"][1]["f_float"], 99.2)

        # must not be overwritten with default
        item_one = ItemGeneralOne(
            f_float="1.2",
            two_1_x=[ItemGeneralTwo(f_float="19.12"), ItemGeneralTwo(f_float="19.22")],
        )
        item_one["two_x_x"].add(
            ItemGeneralTwo(f_float="99.12"), ItemGeneralTwo(f_float="99.22")
        )
        item_one.process()
        self.assertEqual(item_one["f_float"], 1.2)
        self.assertEqual(item_one["two_1_x"][0]["f_float"], 19.12)
        self.assertEqual(item_one["two_1_x"][1]["f_float"], 19.22)
        self.assertEqual(item_one["two_x_x"][0]["f_float"], 99.12)
        self.assertEqual(item_one["two_x_x"][1]["f_float"], 99.22)

    def test_defaults_injection_order_in_bulk(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo

        bulk_one = ItemGeneralOne.Bulk()
        # making sure that default iteration will be in a certain order
        bulk_one.data = OrderedDict()
        bulk_one["two_x_1__one_x_1__f_string"] = "default-1"
        bulk_one["two_x_1__f_string"] = "default-2"
        bulk_one.gen(f_string="test-item")
        bulk_one.process()

        def assertItem(bulk_one):
            self.assertEqual(bulk_one["two_x_1__one_x_1__f_string"], "default-1")
            self.assertEqual(bulk_one["two_x_1__f_string"], "default-2")

            item_one = bulk_one[0]
            # value from the item itself
            self.assertEqual(item_one["f_string"], "test-item")
            # "two_x_1" must contain this value from default ...
            self.assertEqual(item_one["two_x_1"]["f_string"], "default-2")
            # ... and contain an item from default
            one_x_1 = item_one["two_x_1"]["one_x_1"]
            self.assertEqual(one_x_1["f_string"], "default-1")

        assertItem(bulk_one)

        bulk_one = ItemGeneralOne.Bulk()
        bulk_one.data = OrderedDict()
        # different order
        bulk_one["two_x_1__f_string"] = "default-2"
        bulk_one["two_x_1__one_x_1__f_string"] = "default-1"
        bulk_one.gen(f_string="test-item")
        bulk_one.process()

        # but result is the same
        assertItem(bulk_one)

    def test_remove_null_fields(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            remove_null_fields = ["f_integer", "f_string", "two_1_x", "two_1_1"]

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo
            remove_null_fields = ["f_integer", "f_string", "one_1_x", "one_1_1"]
            nullables = ["f_string", "one_1_1"]

        item_one = ItemGeneralOne(
            f_integer=None,
            f_string="string-value",
            two_1_x=[],
            two_1_1=None,
            two_x_x=[],
            two_x_1=None,
        )
        item_one.process()
        # remove_null_fields must not be present
        self.assertNotIn("f_integer", item_one)
        self.assertNotIn("two_1_x", item_one)
        self.assertNotIn("two_1_1", item_one)
        # f_string field has not None value
        self.assertIn("f_string", item_one)

        item_two = ItemGeneralTwo(
            f_integer=None, f_string=None, one_1_x=[ItemGeneralOne()], one_1_1=None
        )
        item_two.process()
        # remove_null_fields must not be present
        self.assertNotIn("f_integer", item_two)
        self.assertNotIn("two_1_x", item_two)
        # f_string and one_1_1 are nullables
        self.assertIn("f_string", item_two)
        self.assertIn("one_1_1", item_two)
        # one_1_x has value
        self.assertIn("one_1_x", item_two)

    def test_default_timezone(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne
            conversions = {
                "time_formats": ["%H:%M:%S%z", "%H:%M:%S"],
                "datetime_formats": ["%Y-%m-%d %H:%M:%S%z", "%Y-%m-%d %H:%M:%S"],
            }

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo

        # no default timezone for fromat source (tzinfo=None)
        item_one = ItemGeneralOne(
            f_time="10:20:30",
            f_datetime="2020-01-01 10:20:30",
        )
        item_one.process()
        self.assertIsNone(item_one["f_time"].tzinfo)
        self.assertIsNone(item_one["f_datetime"].tzinfo)

        # no default timezone for fromat source (tzinfo=__value__)
        item_one = ItemGeneralOne(
            f_time="10:20:30+0100",
            f_datetime="2020-01-01 10:20:30+0200",
        )
        item_one.process()
        self.assertEqual(str(item_one["f_time"].tzinfo), "UTC+01:00")
        self.assertEqual(str(item_one["f_datetime"].tzinfo), "UTC+02:00")

        # no default timezone for func source (tzinfo=None)
        ItemGeneralOne.conversions["time_func"] = lambda value: (
            datetime.datetime.fromtimestamp(value).time()
        )
        ItemGeneralOne.conversions["datetime_func"] = lambda value: (
            datetime.datetime.fromtimestamp(value)
        )
        item_one = ItemGeneralOne(
            f_time=1600262001,
            f_datetime=1600262001,
        )
        item_one.process()
        self.assertIsNone(item_one["f_time"].tzinfo)
        self.assertIsNone(item_one["f_datetime"].tzinfo)

        # no default timezone for func source (tzinfo=__value___)
        ItemGeneralOne.conversions["time_func"] = lambda value: (
            datetime.datetime.fromtimestamp(value)
            .time()
            .replace(tzinfo=datetime.timezone(offset=datetime.timedelta(hours=11)))
        )
        ItemGeneralOne.conversions["datetime_func"] = lambda value: (
            datetime.datetime.fromtimestamp(value).replace(
                tzinfo=datetime.timezone(offset=datetime.timedelta(hours=12))
            )
        )

        item_one = ItemGeneralOne(
            f_time=1600262001,
            f_datetime=1600262001,
        )
        item_one.process()
        self.assertEqual(str(item_one["f_time"].tzinfo), "UTC+11:00")
        self.assertEqual(str(item_one["f_datetime"].tzinfo), "UTC+12:00")

        ItemGeneralOne.conversions["time_func"] = None
        ItemGeneralOne.conversions["datetime_func"] = None

        # default timezone for format source
        ItemGeneralOne.conversions["default_timezone"] = datetime.timezone(
            offset=datetime.timedelta(hours=10)
        )

        item_one = ItemGeneralOne(
            f_time="10:20:30",
            f_datetime="2020-01-01 10:20:30",
        )
        item_one.process()
        self.assertEqual(str(item_one["f_time"].tzinfo), "UTC+10:00")
        self.assertEqual(str(item_one["f_datetime"].tzinfo), "UTC+10:00")

        # default timezone for func
        ItemGeneralOne.conversions["time_func"] = lambda value: (
            datetime.datetime.fromtimestamp(value).time()
        )
        ItemGeneralOne.conversions["datetime_func"] = lambda value: (
            datetime.datetime.fromtimestamp(value)
        )
        item_one = ItemGeneralOne(
            f_time=1600262001,
            f_datetime=1600262001,
        )
        item_one.process()
        self.assertEqual(str(item_one["f_time"].tzinfo), "UTC+10:00")
        self.assertEqual(str(item_one["f_datetime"].tzinfo), "UTC+10:00")

        ItemGeneralOne.conversions["time_func"] = None
        ItemGeneralOne.conversions["datetime_func"] = None

        # no overwrite with default (formats)
        item_one = ItemGeneralOne(
            f_time="10:20:30+0100",
            f_datetime="2020-01-01 10:20:30+0200",
        )
        item_one.process()
        self.assertEqual(str(item_one["f_time"].tzinfo), "UTC+01:00")
        self.assertEqual(str(item_one["f_datetime"].tzinfo), "UTC+02:00")

        # no overwrite with default (funcs)
        ItemGeneralOne.conversions["time_func"] = lambda value: (
            datetime.datetime.fromtimestamp(value)
            .time()
            .replace(tzinfo=datetime.timezone(offset=datetime.timedelta(hours=21)))
        )
        ItemGeneralOne.conversions["datetime_func"] = lambda value: (
            datetime.datetime.fromtimestamp(value).replace(
                tzinfo=datetime.timezone(offset=datetime.timedelta(hours=22))
            )
        )

        item_one = ItemGeneralOne(
            f_time=1600262001,
            f_datetime=1600262001,
        )
        item_one.process()
        self.assertEqual(str(item_one["f_time"].tzinfo), "UTC+21:00")
        self.assertEqual(str(item_one["f_datetime"].tzinfo), "UTC+22:00")

    def test_item_process_error(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo

        # --- single item ---

        item_one = ItemGeneralOne(f_integer="invalid")
        with self.assertRaises(ItemProcessError):
            item_one.process()

        # --- bulk item ---
        bulk_one = ItemGeneralOne.Bulk(f_integer="invalid")
        with self.assertRaises(ItemProcessError):
            bulk_one.process()

    def test_item_revert_error(self):
        class ItemGeneralOne(Item):
            model_cls = self.ModelGeneralOne

        class ItemGeneralTwo(Item):
            model_cls = self.ModelGeneralTwo

        # --- single item ---
        item_one = ItemGeneralOne(f_integer="invalid")
        with self.assertRaises(ItemProcessError):
            item_one.process()

        # --- related item ---
        item_one = ItemGeneralOne(two_x_1=ItemGeneralTwo(f_integer="invalid"))
        with self.assertRaises(ItemProcessError):
            item_one.process()

        item_one = ItemGeneralOne(two_x_x=[ItemGeneralTwo(f_integer="invalid")])
        with self.assertRaises(ItemProcessError):
            item_one.process()

        # --- bulk item ---
        bulk_one = ItemGeneralOne.Bulk(f_integer="invalid")
        with self.assertRaises(ItemProcessError):
            bulk_one.process()

        # --- item in bulk ---
        bulk_one = ItemGeneralOne.Bulk()
        bulk_one.gen(f_integer="invalid")
        with self.assertRaises(ItemProcessError):
            bulk_one.process()

        # --- default item in bulk ---
        bulk_one = ItemGeneralOne.Bulk(two_x_1=ItemGeneralTwo(f_integer="invalid"))
        with self.assertRaises(ItemProcessError):
            bulk_one.process()

        bulk_one = ItemGeneralOne.Bulk(two_x_x=[ItemGeneralTwo(f_integer="invalid")])
        with self.assertRaises(ItemProcessError):
            bulk_one.process()

import unittest
import backend

class DatabaseRead(unittest.TestCase):
    def setUp(self):
        self.emptyDB = {}
        self.fullDB = {
            "str":"str",
            "level1": {
                "str1" : "str1",
                "level2": {
                    "str2": "str2",
                    "level3": {
                        "str3": "str3"
                    }
                }
            }
        }

    def test_empty_db(self):
        self.assertEqual(backend.read_from_db(self.emptyDB, ""), None)
        self.assertEqual(backend.read_from_db(self.emptyDB, "/"), None)
        self.assertEqual(backend.read_from_db(self.emptyDB, "/a"), None)
        self.assertEqual(backend.read_from_db(self.emptyDB, "/a/"), None)
        self.assertEqual(backend.read_from_db(self.emptyDB, "/a/b"), None)
        self.assertEqual(backend.write_to_db(self.fullDB, "/int", 1), 1)
        self.assertEqual(backend.write_to_db(self.fullDB, "/bool/", True), True)

    def test_valid_read_db(self):
        self.assertEqual(backend.read_from_db(self.fullDB, "/str"), "str")
        self.assertEqual(backend.read_from_db(self.fullDB, "/str/"), "str")
        self.assertEqual(backend.read_from_db(self.fullDB, "/level1/str1"), 'str1')
        self.assertEqual(backend.read_from_db(self.fullDB, "/level1/level2/level3/str3"), 'str3')

    def test_invalid_read_db(self):
        self.assertEqual(backend.read_from_db(self.fullDB, ""), None)
        self.assertEqual(backend.read_from_db(self.fullDB, "/"), None)
        self.assertEqual(backend.read_from_db(self.fullDB, "/NoPath"), None)
        self.assertEqual(backend.read_from_db(self.fullDB, "/No/Path"), None)

    def test_valid_write_db(self):
        self.assertEqual(backend.write_to_db(self.fullDB, "/int", 1), 1)
        self.assertEqual(backend.write_to_db(self.fullDB, "/bool/", True), True)
        self.assertEqual(backend.write_to_db(self.fullDB, "/l1", {}), {})
        self.assertEqual(backend.write_to_db(self.fullDB, "/l1/str11", "str11"), "str11")
        self.assertEqual(backend.write_to_db(self.fullDB, "/level1/level2/level3/str31", "str31"), "str31")

    def test_invalid_write_db(self):
        with self.assertRaises(AttributeError) as context:
            backend.write_to_db(self.fullDB, "", "test")
            self.assertTrue("Empty path/DB" in context.exception)

        with self.assertRaises(AttributeError) as context:
            backend.write_to_db(self.fullDB, "/", "test")
            self.assertTrue("Empty path/DB" in context.exception)

        with self.assertRaises(KeyError) as context:
            backend.write_to_db(self.fullDB, "/no/key", "test")
            self.assertTrue("/no/key" in context.exception)

        with self.assertRaises(TypeError) as context:
            backend.write_to_db(self.fullDB, "/str/key", "test")
            self.assertTrue("/no/key" in context.exception)

if __name__ == '__main__':
    unittest.main()
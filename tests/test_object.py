import unittest

from object.object import String, Boolean, Integer


class TestObject(unittest.TestCase):
    def test_string_hash_key(self):
        hello1 = String("Hello World")
        hello2 = String("Hello World")
        diff1 = String("My name is johnny")
        diff2 = String("My name is johnny")

        self.assertEqual(hello1.hash_key(), hello2.hash_key())
        self.assertEqual(diff1.hash_key(), diff2.hash_key())
        self.assertNotEqual(hello1.hash_key(), diff1.hash_key())

    def test_boolean_hash_key(self):
        true1 = Boolean(True)
        true2 = Boolean(True)
        false1 = Boolean(False)
        false2 = Boolean(False)

        self.assertEqual(true1.hash_key(), true2.hash_key())
        self.assertEqual(false1.hash_key(), false2.hash_key())
        self.assertNotEqual(true1.hash_key(), false1.hash_key())

    def test_integer_hash_key(self):
        one1 = Integer(1)
        one2 = Integer(1)
        two1 = Integer(2)
        two2 = Integer(2)

        self.assertEqual(one1.hash_key(), one2.hash_key())
        self.assertEqual(two1.hash_key(), two2.hash_key())
        self.assertNotEqual(one1.hash_key(), two1.hash_key())


if __name__ == "__main__":
    unittest.main()

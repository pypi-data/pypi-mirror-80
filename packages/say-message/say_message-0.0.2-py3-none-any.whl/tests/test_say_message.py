import unittest
from say_message.say_message import say_message


class TestMessage(unittest.TestCase):
    def test_say_hello(self):
        message = say_message("Hi")
        self.assertEqual(message, "Hi")


if __name__ == "__main__":
    unittest.main()
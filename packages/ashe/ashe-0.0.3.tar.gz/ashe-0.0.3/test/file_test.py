import unittest

from ashe import read
from ashe import write


class DictTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = "123"
        self.path = "./test/test.txt"

    def test_write_and_read(self) -> None:
        write(self.path, self.data)
        self.assertEqual(read(self.path), self.data)


if __name__ == '__main__':
    unittest.main()

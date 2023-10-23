import unittest
from tournament import *


class TestTournament(unittest.TestCase):
    def test_get_by_order(self):
        a = int(10)
        self.assertEqual(type(a), int)


if __name__ == "__main__":
    unittest.main()

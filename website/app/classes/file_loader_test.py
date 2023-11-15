import unittest

from threading import Lock, Thread

from .file_loader import FileLoader

class TestSingleton(unittest.TestCase):
    def test_creating(self):
        a = FileLoader('Strategy_game/test_solutions/draught.cpp')


if __name__ == '__main__':
    unittest.main()

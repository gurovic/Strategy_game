import unittest

from singleton import Singleton 

class TestSingleton(unittest.TestCase):

    def test_unique(self):
        class A(metaclass=Singleton):
            pass

	
        a = A()
        b = A()
        self.assertEqual(id(a), id(b))


    def test_different(self):
        class A(metaclass=Singleton):
            pass

        class B(metaclass=Singleton):
            pass

	
        a = A()
        b = B()
        self.assertNotEqual(id(a), id(b))


if __name__ == '__main__':
    unittest.main()
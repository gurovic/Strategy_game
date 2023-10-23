import unittest

from threading import Lock, Thread

from .singleton import Singleton


class TestSingleton(unittest.TestCase):

    def test_async_unique(self):
        class A(metaclass=Singleton):
            pass

        singletons = []

        def create():
            singletons.append(A())

        process1 = Thread(target=create)
        process2 = Thread(target=create)
        process1.start()
        process2.start()
        self.assertEqual(id(singletons[0]), id(singletons[1]))

    def test_async_different(self):
        class A(metaclass=Singleton):
            pass

        class B(metaclass=Singleton):
            pass

        singletons = []

        def create(id):
            if id == 0:
                singletons.append(A())
            else:
                singletons.append(B())

        process1 = Thread(target=create, args=(0,))
        process2 = Thread(target=create, args=(1,))
        process1.start()
        process2.start()
        self.assertNotEqual(id(singletons[0]), id(singletons[1]))

    def test_can_be_instantiated(self):
        class A(metaclass=Singleton):
            pass

        a = A()
        self.assertNotEqual(a, None)

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

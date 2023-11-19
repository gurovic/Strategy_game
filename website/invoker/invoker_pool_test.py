from django.test import TestCase

from invoker.invoker_pool import InvokerPool, LowInvokerCap


class TestLowInvokerCap(TestCase):
    def test_str(self):
        exception = LowInvokerCap(2, 1)
        self.assertEquals(str(exception), "Need 2 but have only 1")


class TestInvokerPool(TestCase):
    def test_different(self):
        class TestPool(InvokerPool):
            pass

        first_pool = TestPool(100)
        second_pool = TestPool(100)
        self.assertNotEqual(first_pool, second_pool)

    def test_invoker_count(self):
        class TestPool(InvokerPool):
            pass

        pool = TestPool(100)
        self.assertEqual(len(pool.all_invokers), 100)

    def test_get_invokers(self):
        class TestPool(InvokerPool):
            pass

        pool = TestPool(16)
        first_group = pool.get(10)
        self.assertEqual(len(first_group), 10)
        with self.assertRaises(LowInvokerCap):
            pool.get(10)
        second_group = pool.get(6)
        self.assertEqual(len(second_group), 6)

    def test_free_invokers_count(self):
        class TestPool(InvokerPool):
            pass

        pool = TestPool(100)
        self.assertEqual(pool.free_invokers_count, 100)
        first_group = pool.get(20)
        self.assertEqual(pool.free_invokers_count, 80)
        second_group = pool.get(60)
        self.assertEqual(pool.free_invokers_count, 20)
        third_group = pool.get(20)
        self.assertEqual(pool.free_invokers_count, 0)

    def test_free_invokers(self):
        class TestPool(InvokerPool):
            pass

        pool = TestPool(100)
        first_group = pool.get(20)
        self.assertEqual(pool.free_invokers_count, 80)
        for i in first_group:
            pool.free(i)
        self.assertEqual(pool.free_invokers_count, 100)
        second_group = pool.get(30)
        self.assertEqual(pool.free_invokers_count, 70)
        for i in second_group:
            pool.free(i)
        self.assertEqual(pool.free_invokers_count, 100)

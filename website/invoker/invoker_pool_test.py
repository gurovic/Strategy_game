from django.test import TestCase
from django.conf import settings
from unittest.mock import patch, Mock

from invoker.invoker_pool import InvokerPool, LowInvokerCap


class TestLowInvokerCap(TestCase):
    def test_str(self):
        exception = LowInvokerCap(2, 1)
        self.assertEquals(str(exception), "Need 2 but have only 1")


class TestInvokerPool(TestCase):
    def test_unique(self):
        class TestPool(InvokerPool):
            pass

        first_pool = TestPool()
        second_pool = TestPool()
        self.assertEqual(first_pool, second_pool)

    @patch("invoker.invoker_pool.settings")
    def test_invoker_count(self, mock_settings: Mock):
        for invokers_count in range(1, 100):
            mock_settings.MAX_INVOKERS_COUNT = invokers_count

            class TestPool(InvokerPool):
                pass

            pool = TestPool()
            self.assertEqual(len(pool.all_invokers), mock_settings.MAX_INVOKERS_COUNT)

    @patch("invoker.invoker_pool.settings")
    def test_get_invokers(self, mock_settings: Mock):
        mock_settings.MAX_INVOKERS_COUNT = 16

        class TestPool(InvokerPool):
            pass

        pool = TestPool()
        first_group = pool.get(10)
        self.assertEqual(len(first_group), 10)
        with self.assertRaises(LowInvokerCap):
            pool.get(10)
        second_group = pool.get(6)
        self.assertEqual(len(second_group), 6)

    @patch("invoker.invoker_pool.settings")
    def test_free_invokers_count(self, mock_settings: Mock):
        mock_settings.MAX_INVOKERS_COUNT = 100

        class TestPool(InvokerPool):
            pass

        pool = TestPool()
        self.assertEqual(pool.free_invokers_count, 100)
        first_group = pool.get(20)
        self.assertEqual(pool.free_invokers_count, 80)
        second_group = pool.get(60)
        self.assertEqual(pool.free_invokers_count, 20)
        third_group = pool.get(20)
        self.assertEqual(pool.free_invokers_count, 0)

    @patch("invoker.invoker_pool.settings")
    def test_free_invokers(self, mock_settings: Mock):
        mock_settings.MAX_INVOKERS_COUNT = 100

        class TestPool(InvokerPool):
            pass

        pool = TestPool()
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

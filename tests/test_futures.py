import time
import unittest

from threading_futures.exceptions import (
    AlreadyRunError,
    CancelledError,
    NotCallableError,
)
from threading_futures.futures import Future


class FuturesTestCase(unittest.TestCase):

    def setUp(self):
        self.test_callback = False

    def _test_add_method(self, a, b):
        return a + b

    def _test_exception_raised_method(self):
        raise IndexError

    def _test_callback_method(self, future):
        self.test_callback = True

    def _test_long_run_method(self):
        time.sleep(1)

    def test_sum_method(self):
        a = 2
        b = 3
        future = Future(self._test_add_method, (a, b))
        future.add_done_callback(self._test_callback_method)
        future.start()
        time.sleep(1)
        self.assertTrue(future.done())
        self.assertFalse(future.cancelled())
        self.assertEqual(future.result(), 5)
        self.assertIsNone(future.exception())
        self.assertTrue(future.cancel())
        self.assertTrue(self.test_callback)

    def test_exception_raised_method(self):
        future = Future(self._test_exception_raised_method)
        future.add_done_callback(self._test_callback_method)
        future.start()
        time.sleep(1)
        self.assertTrue(future.done())
        self.assertFalse(future.cancelled())
        self.assertRaises(IndexError, future.result)
        self.assertIsInstance(future.exception(), IndexError)
        self.assertTrue(future.cancel())
        self.assertTrue(self.test_callback)

    def test_cancel_future(self):
        future = Future(self._test_add_method, (2, 3))
        future.add_done_callback(self._test_callback_method)
        self.assertTrue(future.cancel())
        self.assertTrue(future.done())
        self.assertTrue(future.cancelled())
        self.assertRaises(CancelledError, future.result)
        self.assertIsNone(future.exception())
        self.assertTrue(future.cancel())
        self.assertFalse(self.test_callback)

    def test_cancel_run_future(self):
        future = Future(self._test_long_run_method)
        future.add_done_callback(self._test_callback_method)
        future.start()
        self.assertFalse(future.cancel())
        self.assertRaises(AlreadyRunError,
                          future.add_done_callback,
                          self._test_callback_method)
        time.sleep(2)
        self.assertTrue(future.done())
        self.assertFalse(future.cancelled())
        self.assertIsNone(future.result())
        self.assertIsNone(future.exception())
        self.assertTrue(future.cancel())
        self.assertTrue(self.test_callback)

    def test_not_callable(self):
        self.assertRaises(NotCallableError, Future, None)


if __name__ == "__main__":
    unittest.main()

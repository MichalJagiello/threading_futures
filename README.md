Sometimes you need to run some code in another thread. Using threading_futures you can call your code in another thread, do not care about it and be notify when it is done.

## Code Example

Run a future with a method which returns some value

```python
>>> from threading_futures.futures import Future
>>> future = Future(add, 1, 2)
>>> future.start()
>>> future.done()
True
>>> future.result()
3
```

Run a future with an `add` method which raise an exception

```python
>>> from threading_futures.futures import Future
>>> future = Future(add, 1, 'a')
>>> future.start()
>>> future.done()
True
>>> future.exception()
TypeError("unsupported operand type(s) for +: 'int' and 'str'",)
>>> future.result()
Traceback (most recent call last):
  File "<input>", line 1, in <module>
  File ".../threading_futures/threading_futures/futures.py", line 76, in result
    raise self._exception
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

Adding a done callback to the Future

```python
>>> def notify(future):
...     print("Future result: {}".format(future.result()))
>>> from threading_futures.futures import Future
>>> future = Future(add, 1, 2)
>>> future.add_done_callback(notify)
>>> future.start()
Future result: 3
```

## Installation

In project main directory run `python setup.py install`

## API Reference

`class threading_futures.Future(callable, *args, **kwargs)`

This class is _almost_ compatible with class [concurrent.futures.Future](https://docs.python.org/3/library/concurrent.futures.html#future-objects)

cancel()

    Attempt to cancel the call. If the call is currently being executed and cannot be cancelled then the method will return False, otherwise the call will be cancelled and the method will return True.

cancelled()

    Return True if the call was successfully cancelled.

running()

    Return True if the call is currently being executed and cannot be cancelled.

done()

    Return True if the call was successfully cancelled or finished running.

result()

    Return the value returned by the call.

    If the future is cancelled before completing then CancelledError will be raised.

    If the call raised, this method will raise the same exception.

exception()

    Return the exception raised by the call.

    If the call completed without raising, None is returned.

add_done_callback(fn)

    Attaches the callable fn to the future. fn will be called, with the future as its only argument, when the future finishes running.

## Tests

To run tests you have to get installed [`nosetests`](http://nose.readthedocs.io/en/latest/) . If you do not have it installed already call `pip install nose`.
In project main directory call `nosetests`.

## License

MIT

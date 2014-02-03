import unittest

__all__ = [
    'Future'
]

class Future(object):
    def __init__(self, future, callback):
        self.future = future
        self.callback = callback

    def get_result(self):
        return self.callback(self.future)



## TESTS:

class RpcStubException(Exception):
    pass

class RpcStub(object):
    def __init__(self, exc=False):
        self.exc = exc

    def get_result(self):
        if self.exc:
            raise RpcStubException('stub')
        return ['stub']

class FutureTest(unittest.TestCase):

    def test_order(self):
        callbacks_logs = []

        def callback1(future):
            callbacks_logs.append('1_before')
            result = future.get_result()
            result.append('callback1')
            callbacks_logs.append('1_after')
            return result

        def callback2(future):
            callbacks_logs.append('2_before')
            result =  future.get_result()
            result.append('callback2')
            callbacks_logs.append('2_after')
            return result

        def callback3(future):
            callbacks_logs.append('3_before')
            result = future.get_result()
            result.append('callback3')
            callbacks_logs.append('3_after')
            return result

        rpc_stub = RpcStub()

        future1 = Future(rpc_stub, callback1)
        future2 = Future(future1, callback2)
        future3 = Future(future2, callback3)

        result = future3.get_result()
        self.assertEqual(result, ['stub', 'callback1', 'callback2', 'callback3'])
        self.assertEqual(callbacks_logs, ['3_before', '2_before', '1_before', '1_after', '2_after', '3_after'])

    def test_exceptions(self):
        callbacks_logs = []

        class Exception1(Exception): pass
        class Exception2(Exception): pass
        class Exception3(Exception): pass

        def callback1(future):
            callbacks_logs.append('1_before')
            try:
                result = future.get_result()
            except RpcStubException as e:
                callbacks_logs.append('1_after')
                raise Exception1(str(e)+'exception1')
            return result

        def callback2(future):
            callbacks_logs.append('2_before')
            try:
                result = future.get_result()
            except Exception1 as e:
                callbacks_logs.append('2_after')
                raise Exception2(str(e)+'exception2')
            return result

        def callback3(future):
            callbacks_logs.append('3_before')
            try:
                result = future.get_result()
            except Exception2 as e:
                callbacks_logs.append('3_after')
                raise Exception3(str(e)+'exception2')
            return result

        rpc_stub = RpcStub(exc=True)

        future1 = Future(rpc_stub, callback1)
        future2 = Future(future1, callback2)
        future3 = Future(future2, callback3)

        try:
            future3.get_result()
        except Exception3 as e:
            self.assertEqual(str(e), 'stubexception1exception2exception2')


if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.WARN)
    unittest.main()

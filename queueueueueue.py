from multiprocessing import Process, Queue, Lock

# TODO(yurass130@gmail.com) try to create Multiprocess Singleton Queue 
class Singleton(type):
    _instances = {}
    _lock: Lock = Lock()
    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class MultiQueue(Queue):
    __metaclass__= Singleton

def foo():
    q = MultiQueue()
    q.put('foo')
    print('foo', q)

def bar():
    q = MultiQueue()
    q.put('bar')
    print('bar', q)

if __name__ == "__main__":
    f = Process(target=foo, name="foo")
    b = Process(target=bar, name="bar")
    f.run()
    b.run()

    q = MultiQueue()
    print(q.get(), "taked from MultiQueue")
    again = Process(target=bar, name="bar2")
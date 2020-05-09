import time
import types
import logging

logging.basicConfig(level=logging.INFO,
                    filename='lab_lru_cache_output.txt',
                    filemode='w',)
                    # format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class DNode:
    def __init__(self, key_=None, value_=None):
        self.value = value_
        self.key = key_
        self.prev = None
        self.next = None


class lru_cache:

    def __init__(self, capacity: int):
        self.dict = dict()
        self.capacity = capacity
        self.size = 0
        self.head = DNode()
        self.tail = DNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def push(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        return node

    def remove(self, node):
        prev = node.prev
        nxt = node.next
        prev.next = nxt
        nxt.prev = prev

    def top(self, node):
        self.remove(node)
        self.push(node)

    def pop(self):
        k = self.tail.prev.key
        self.remove(self.tail.prev)
        return k

    def get(self, key: int) -> int:
        if key not in self.dict:
            return -1
        else:
            node = self.dict[key]
            self.top(node)
            return node.value

    def put(self, key: int, value: int) -> None:
        node = DNode(key, value)
        if key not in self.dict:
            if self.size >= self.capacity:
                del self.dict[self.pop()]
                self.size -= 1
            self.dict[key] = self.push(node)
            self.size += 1
        else:
            self.top(self.dict[key])
            self.dict[key].value = value

    def __call__(self, func, *args, **kwargs):
        def wrapper(*args, **kwargs):
            key = args[0]
            v = self.get(key)
            start_time = time.time()
            if v == -1:
                v = func(*args, **kwargs)
                self.put(key, v)
                logging.info("[%.8fs] %s(%s) -> %s " % (time.time() - start_time, func.__name__, key, v))
            else:
                logging.info("[cache_hit] %s(%s) -> %s " % (func.__name__, key, v))
            return v

        return wrapper

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

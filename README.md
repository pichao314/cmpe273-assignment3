# LRU Cache and Bloom Filter

## 1.DELETE operation

### Serialize DELETE operation

Full implementation in [here](pickle_hash.py).

```python
def serialize_DELETE(id):
    envelope_bytes = pickle.dumps({
        'operation': 'DELETE',
        'id': id
    })
    return envelope_bytes, id
```

### Server Process Delete

Full implementation in [here](cache_server.py).

```python
if operation == 'DELETE':
    if self.db.delete(key):
        return "Success"
    else:
        return "ID not exists!"
```

### Delete operation of DB

Full implementation in [here](cache_server.py).

```python
class MyDict(dict):
    def delete(self, key):
        return self.pop(key)
```

### Client test

Full implementation in [here](cache_client.py).

```python
for hc in hash_codes:
    data_bytes, key = serialize_DELETE(hc)
    response = client_ring.get_node(key).send(data_bytes)
    print(response)
```

## 2.LRU Cache

Use double-linked-list to realize the LRU cache.
Full code in [here](lru_cache.py),and test result in [here](lab_lru_cache_output.txt)

```python
class DNode:
    def __init__(self, key_=None, value_=None):
        self.value = value_
        self.key = key_
        self.prev = None
        self.next = None

class lru_cache:
    # initialize cache
    def __init__(self, capacity: int)
    # push a node into the top after head
    def push(self, node):
    # remove a node
    def remove(self, node):
    # move a node to top
    def top(self, node):
    # pop a node before tail
    def pop(self):
    # get a node by key, if not found return -1, otherwise move the node to top
    def get(self, key: int) -> int:
    # put a node with key and value to top, pop LRU node from tail
    def put(self, key: int, value: int) -> None:
```

## 3.Bloom Filter

Full code in [here](bloom_filter.py), and test result in [here](lab_bloom_filter_output.txt)

```python
class BloomFilter:
    # figure the bit size and hash func size, initialize the bit array with 0
    def __init__(self, n, fp):

    # add a key by setting all relative bit into 1
    def add(self, key):

    # check if the key is a member
    def is_member(self, url):

    # get the positive bits of a key
    def get_positions(self, key):
```

We can calculate the bit array size(m) and hash function count(k) by following function:

```python
def calc(n, p):
    BIT_SIZE = -(n * log(p))/(log(2)**2) 
    HASH_NUM = int(BIT_SIZE/n)*log(2)
    return BIT_SIZE,HASH_NUM
```

Here we have n = 1,000,000,000, assume fp is still 0.05, then we have

```python
m = 6235224230
k = 4
```

# Appendix

The assignment 3 is based on our simple [distributed cache](https://github.com/sithu/cmpe273-spring20/tree/master/midterm) where you have implmented the GET and PUT operations.

## 1. DELETE operation

You will be adding the DELETE operation to delete entires from the distributed cache.

_Request_

```json
{ 
    'operation': 'DELETE',
    'id': 'hash_code_of_the_object',
}
```

_Response_

```json
{
    'success'
}
```

## 2. LRU Cache

In order to reduce unnecessary network calls to the servers, you will be adding LRU cache on client side. On each GET call, you will be checking against data from a local cache.

Implement LRU cache as Python decorator and you can pass cache size as argument. You must name the name as lru_cache.py and can be tested via test_lru_cache.py.

```python
@lru_cache(5)
def get(...):
    ...
    return ...
    

def put(...):
    ...
    return ...

def delete(...):
    ...
    return ...

```

@lru_cache is your implementation as a decorator function and do NOT use any existing LRU libraries. 

> Although you do not need to print execution time __[0.00000191s]__ and cache hit logs __[cache-hit]__, you should able to run test_lru_cache.py successfully without any errors in order to get full credits.

## 3. Bloom Filter

Finally, you will be implementing a bloom filter so that we can validate any key lookup without hitting the servers. The bloom filter will have two operations:

### Add

This add() function handles adding new key to the membership set.

### Is_member

This is_member() function checks whether a given key is in the membership or not.

On the client side, the GET and DELETE will invoke is_member(key) function first prior to calling the servers while the PUT and DELETE will call add(key) function to update the membership.

Bit array and hash libraries:

```
pipenv install bitarray
pipenv install mmh3
```

Use this formula to calculate Bit array size:

```
m = - (n * log(p)) / (log(2)^2) 

```

where,
- m = bit array size
- n = number of expected keys to be stored
- p = Probability of desired false positive rate

Answer the following question:

* What are the best _k_ hashes and _m_ bits values to store one million _n_ keys (E.g. e52f43cd2c23bb2e6296153748382764) suppose we use the same MD5 hash key from [pickle_hash.py](https://github.com/sithu/cmpe273-spring20/blob/master/midterm/pickle_hash.py#L14) and explain why?

```python
@lru_cache(5)
def get(key):
    if bloomfilter.is_member(key):
        return udp_client.get(key)
    else:
        return None

def put(key, value):
    bloomfilter.add(key)
    return udp_client.put(key, value)

def delete(key):
    if bloomfilter.is_member(key):
        return udp_client.delete(key)
    else:
        return None

```

You can validate your implementation using _test_bloom_filter.py_ and should get the expected output as test_bloom_filter_output.txt .






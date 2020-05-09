import pickle
import hashlib


def serialize(object):
    return pickle.dumps(object)


def deserialize(object_bytes):
    return pickle.loads(object_bytes)


# create md5 hex hash value of byte object
def hash_code_hex(data_bytes):
    hash_code = hashlib.md5(data_bytes)
    return hash_code.hexdigest()


# serialize the PUT request and pack with its md5
def serialize_PUT(object):
    object_bytes = pickle.dumps(object)
    hash_code = hash_code_hex(object_bytes)
    envelope_bytes = pickle.dumps({
        'operation': 'PUT',
        'id': hash_code,
        'payload': object
    })
    return envelope_bytes, hash_code


# serialize GET request
def serialize_GET(id):
    envelope_bytes = pickle.dumps({
        'operation': 'GET',
        'id': id
    })
    return envelope_bytes, id


# serialize DELETE request
def serialize_DELETE(id):
    envelope_bytes = pickle.dumps({
        'operation': 'DELETE',
        'id': id
    })
    return envelope_bytes, id


def test():
    data_bytes, hash_code = serialize_PUT({'user': 'Foo'})
    print(f"Data Bytes={data_bytes}\nHash Code={hash_code}")
    data = deserialize(data_bytes)
    print(data)


if __name__ == "__main__":
    test()

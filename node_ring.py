# serialize and deserialize methods with md5 hash as id
import hashlib

# node with their sockets
from server_config import NODES


class NodeRing():
    # creator of ring
    def __init__(self, nodes):
        assert len(nodes) > 0
        self.nodes = nodes

    # get node's socket by index
    def get_node(self, key_hex):
        # the md5 hash was digest by hex, so convert to int base on 16
        key = int(key_hex, 16)
        # get the node index by modulus
        node_index = key % len(self.nodes)
        # return the socket of the node
        return self.nodes[node_index]


def test():
    # create a ring with provided Nodes sockets
    ring = NodeRing(nodes=NODES)
    # get the node socket of provided md5 hash value
    node = ring.get_node('9ad5794ec94345c4873c4e591788743a')
    print(node)
    print(ring.get_node('ed9440c442632621b608521b3f2650b8'))


# Uncomment to run the above local test via: python3 node_ring.py
if __name__ == "__main__":
    test()

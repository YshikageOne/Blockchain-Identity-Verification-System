import hashlib
import json

#Basic Block Class
class Block:

    def __init__(self, index, timestamp, data, previousHash):
        self.index = index #position in the blockchain
        self.timestamp = timestamp #time of block creation
        self.data = data #main data
        self.previousHash = previousHash
        self.nonce = 0 #number used for finding valid hashes for a new block
        self.hash = self.calculate_hash()


    #makes the hash using sha256
    def calculate_hash(self):
        blockInfoString = f"{self.index}{self.timestamp}{json.dumps(self.data, sort_keys = True)}{self.previousHash}{self.nonce}"
        return hashlib.sha256(blockInfoString.encode()).hexdigest()

    #proof of work algorithm
    #to make it difficult to mine a block
    def mine_block(self, difficulty):
        target = '0' * difficulty

        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

        print(f"Block mined: {self.hash}")
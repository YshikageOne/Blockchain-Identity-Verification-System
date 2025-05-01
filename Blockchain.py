import time
import uuid
from Block import *

#Blockchain implementation
class Blockchain:
    def __init__(self):
        self.chain = [self.create_firstBlock()]
        self.difficulty = 2
        self.pending_identities = []

    #create the first block in the blockchain
    def create_firstBlock(self):
        return Block(0, time.time(), {"message": "First Block"}, "0")

    #returns the most recent block
    def get_latestBlock(self):
        return self.chain[-1]


    #creates new block and identity on the blockchain
    def add_block(self, new_block):
        new_block.previousHash = self.get_latestBlock().hash
        new_block.mine_block(self.difficulty)

        self.chain.append(new_block)

    def register_identity(self, identity_data):
        identity_id = str(uuid.uuid4())
        identity_data["identity_id"] = identity_id
        identity_data["registration_time"] = time.time()

        new_block = Block(
            len(self.chain),
            time.time(),
            identity_data,
            self.get_latestBlock().hash
        )
        self.add_block(new_block)
        return identity_id

    #search the blockchain with a specific ID
    def verify_identity(self, identity_id, provided_data = None):
        for block in self.chain[1:]: #skip the first block because it doesn't have any identity data
            if 'identity_id' in block.data and block.data['identity_id'] == identity_id:
                if provided_data:
                    match = True
                    #to make sure that all data matches with the stored data
                    for key, value in provided_data.items():
                        if key in block.data and block.data[key] != value:
                            match = False
                            break

                    if match:
                        return True, block.data
                    else:
                        return False, "Provided data doesn't match blockchain record"

                else:
                    return True, block.data


        return False, "Identity not found in the blockchain"


    #vibe check the integrity of the blockchain
    #by verifiying each block's hash and links
    def is_chain_valid(self):

        for i in range(1, len(self.chain)): #for each loop from the beginning to the last block
            current_block = self.chain[i]
            previous_block =  self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previousHash != previous_block.hash:
                return False

        return True

    #save the blockchain to a file
    def save_blockchain(self):
        blockchain_data = []

        for block in self.chain:
            block_data = {
                "index": block.index,
                "timestamp": block.timestamp,
                "data": block.data,
                "previousHash": block.previousHash,
                "nonce": block.nonce,
                "hash": block.hash
            }
            blockchain_data.append(block_data)

        try:
            with open("blockchain_data.json", "w") as file:
                json.dump(blockchain_data, file, indent = 4)
        except Exception as e:
            print(f"Error saving blockchain: {str(e)}")


    #loading the json file to blockchain
    def load_blockchain(self):
        try:
            with open("blockchain_data.json", "r") as file:
                blockchain_data = json.load(file)

            self.chain = []
            for block_data in blockchain_data:
                block = Block(
                    block_data["index"],
                    block_data["timestamp"],
                    block_data["data"],
                    block_data["previousHash"]
                )
                block.nonce = block_data["nonce"]
                block.hash = block.data["hash"]
                self.chain.append(block)

            print(f"Loaded blockchain with {len(self.chain)} blocks")
            return True

        except Exception as e:
            print(f"Error loading blockchain: {str(e)}")
            return False

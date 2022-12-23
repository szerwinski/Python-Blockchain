import hashlib
import json
import datetime
from api import Api

api = Api() # Global API Instance

class Blockchain(object): 

    def __init__(self):
        
        self.chain = []
        self.pending_transactions = [] # Todo: Populate with current data in DB -> self.chain = api.getChain()

        self.new_block(previous_hash="0000", proof=100)

# Create a new block listing key/value pairs of block information in a JSON object. Reset the list of pending transactions & append the newest block to the chain.

    def new_block(self, proof, previous_hash):

        timestamp = datetime.datetime.now().isoformat()
        
        block = {
            'index': len(self.chain) + 1,
            'timestamp': timestamp,
            'proof': proof,
            'previous_hash': previous_hash or self.chain[-1]["hash"],
        }

        blockHash = self.hash(block)

        block['hash'] = blockHash

        self.pending_transactions = [] # Make it dynamic from db
        self.chain.append(block) # Remove This

        api.postBlock(block=block, blockHash=blockHash)

        return block

# Add a transaction with relevant info to the 'blockpool' - list of pending tx's. 

    def new_transaction(self, sender, recipient, data):
        transaction = {
            'from': sender,
            'to': recipient,
            'transaction': data,
        }

        self.pending_transactions.append(transaction)

        api.postTransaction(blockHash=self.last_block['hash'], transaction=transaction)

        return self.last_block['index'] + 1

# receive one block. Turn it into a string, turn that into Unicode (for hashing). Hash with SHA256 encryption, then translate the Unicode into a hexidecimal string.

    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash

# Search the blockchain for the most recent block.

    @property
    def last_block(self):
 
        return self.chain[-1]

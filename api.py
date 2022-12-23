from google.cloud import firestore

class Api(object):

    def connect(self):
        print('Connecting to DataBase\n')
        self.db = firestore.Client(project='blockchain-2cc54')
        pass

    def postBlock(self, block, blockHash) :
        self.db = firestore.Client(project='blockchain-2cc54')
        print('\nNew block Hash: ' + blockHash + '\n')
        print('Previous block Hash: ' + block['previous_hash'] + '\n')
        doc_ref = self.db.collection(u'blockchain').document(blockHash)
        doc_ref.set(block)
        pass

    # POST new Transaction 
    def postTransaction(self, blockHash, transaction) :
        doc_ref = self.db.collection(u'blockchain').document(blockHash).collection('transactions').document()
        doc_ref.set(transaction)
        pass

    # GET Blockchain
    def getChain(self): 
        self.db = firestore.Client(project='blockchain-2cc54')
        doc_ref = self.db.collection(u'blockchain')
        doc = doc_ref.get()

        chain = []
        
        for block in doc:
            chain.append(block.to_dict())

        return chain

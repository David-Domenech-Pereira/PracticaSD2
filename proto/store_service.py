
from proto import store_pb2
import time

class StoreService:
    def set_store(self, store):
        self.store = store
    
    def __init__(self):
        self.store = {}
        self.slow_down_seconds = 0
       

    def put(self, put_request, context):
        # forbiden, as the master node will handle this
        return store_pb2.PutResponse(success=False)
    

    def get(self, get_request, context):
        value = self.store.get(get_request.key)
        time.sleep(self.slow_down_seconds)
        if value is None:
            return store_pb2.GetResponse(value="", found=False)
        return store_pb2.GetResponse(value=value, found=True)
    
    def slowDown(self, slow_down_request, context):
        self.slow_down_seconds = slow_down_request.delay
        return store_pb2.SlowDownResponse(success=True)
    
    def restore(self, restore_request, context):
        self.slow_down_seconds = 0
        return store_pb2.RestoreResponse(success=True)
    
    def canCommit(self, commit_request, context):
        # return success = True
        time.sleep(self.slow_down_seconds)
        return store_pb2.CommitRespone(success=True)

    def doCommit(self, commit_request, context):
        # return success = True
        self.store[commit_request.key] = commit_request.value
        return store_pb2.doCommitRespone(success=True)
    def discoverMessage(self, discover_request, context):
       
        return store_pb2.Empty()
    
    def askVotePut(self, vote_request, context):
        return store_pb2.askVotePutRespone(success=False, vote_size=0)
    
    def askVoteGet(self, vote_request, context):
        return store_pb2.askVoteGetRespone(success=False, vote_size=0, value="")
    
class MasterService(StoreService):
    
    def setDiscoverQueue(self, discover_queue):
        self.discover_queue = discover_queue
    def __init__(self):
        super().__init__()
    def put(self, put_request, context):
        # cridem al master.py el métode 2PC
        from centralized import master
        if(master.two_phase_commit(self.store, put_request, context)):
            # si ok devolvemos PutResponse(True)
            self.store[put_request.key] = put_request.value
            return store_pb2.PutResponse(success=True)
        else:
            # si no devolvemos PutResponse(False)
            return store_pb2.PutResponse(success=False)
    def discoverMessage(self, discover_request, context):
        
        self.discover_queue.append(discover_request.ip+":"+str(discover_request.port))
        return store_pb2.Empty()
        

class NodeService(StoreService):
    def setVoteSize(self, vote_size):
        self.vote_size = vote_size
    def __init__(self):
        self.vote_size = 3
        super().__init__()
    
    def put(self, put_request, context):
        from decentralized import node
        if(node.askPutVote(self.store, put_request, context)):
            self.store[put_request.key] = put_request.value
            return store_pb2.PutResponse(success=True)
        else:
            return store_pb2.PutResponse(success=False)
    
    def get(self, get_request, context):
        from decentralized import node
        value = node.askGetVote(self.store, get_request, context, self.store.get(get_request.key), self.vote_size)
        if value is None:
            return store_pb2.GetResponse(value="", found=False)
        return store_pb2.GetResponse(value=value, found=True)
    
    def askVotePut(self, vote_request, context):
        # devolver success = True
        time.sleep(self.slow_down_seconds)
        return store_pb2.askVotePutRespone(success=True, vote_size=self.vote_size)
        
    def askVoteGet(self, vote_request, context):
        # si la key esta en el store devolver success = True
        # si no devolver success = False
        value = self.store.get(vote_request.key)
        time.sleep(self.slow_down_seconds)
        print("Vote request for key: "+vote_request.key+" value: "+str(value)+" vote_size: "+str(self.vote_size))
        if value is None:
            return store_pb2.askVoteGetRespone(success=False, vote_size=self.vote_size, value="")
        return store_pb2.askVoteGetRespone(success=True, vote_size=self.vote_size, value=value)
        
        

store_service = StoreService()
master_service = MasterService()
node_service = NodeService()
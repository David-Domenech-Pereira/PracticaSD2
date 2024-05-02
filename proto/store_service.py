
from proto import store_pb2
import time
import redis
class StoreService:
    # Aquesta classe és la base de les altres dues, és la que tenen els slaves del centralized
    def set_store(self, store):
        self.store = store
    
    def __init__(self):
        self.store = {}
        self.slow_down_seconds = 0
       

    def put(self, put_request, context):
        # forbiden, as the master node will handle this
        return store_pb2.PutResponse(success=False)
    

    def get(self, get_request, context):
        # Return the value of the key
        value = self.store.get(get_request.key)
        time.sleep(self.slow_down_seconds)
        if value is None:
            return store_pb2.GetResponse(value="", found=False)
        return store_pb2.GetResponse(value=value, found=True)
    
    def slowDown(self, slow_down_request, context):
        # Aquesta funció fa que el servidor es guardi el temps que ha de retardar-se
        self.slow_down_seconds = slow_down_request.delay
        return store_pb2.SlowDownResponse(success=True)
    
    def restore(self, restore_request, context):
        # Reinicia el temps a retardar-se
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
        # This cannot be called to a slave
        return store_pb2.Empty()
    
    def askVotePut(self, vote_request, context):
        # forbiden, as the decentralized nodes will handle this
        return store_pb2.askVotePutRespone(success=False, vote_size=0)
    
    def askVoteGet(self, vote_request, context):
        # forbiden, as the decentralized nodes will handle this
        return store_pb2.askVoteGetRespone(success=False, vote_size=0, value="")
    
class MasterService(StoreService):
    # Aquesta service és el que implementa el master del centralized
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
            r = redis.Redis(host='localhost', port=6379, decode_responses=True)# redis.Redis(host='localhost', port=6379)
            r.set(put_request.key, put_request.value)
            return store_pb2.PutResponse(success=True)
        else:
            # si no devolvemos PutResponse(False)
            return store_pb2.PutResponse(success=False)
    def discoverMessage(self, discover_request, context):
        # afegim la ip i port a la llista de clients
        self.discover_queue.append(discover_request.ip+":"+str(discover_request.port))
        return store_pb2.Empty()
        

class NodeService(StoreService):
    # Aquesta service és el que implementen els nodes del decentralized
    def setVoteSize(self, vote_size):
        self.vote_size = vote_size
    def __init__(self):
        self.vote_size = 3
        super().__init__()
    
    def put(self, put_request, context):
        """funció que fa un put request."""
        from decentralized import node
        # Cridem al algoritme de votació
        if(node.askPutVote(self.store, put_request, context)):
            self.store[put_request.key] = put_request.value
            r = redis.Redis(host='localhost', port=6379, decode_responses=True)# redis.Redis(host='localhost', port=6379)
            r.set(put_request.key, put_request.value)
            return store_pb2.PutResponse(success=True)
        else:
            return store_pb2.PutResponse(success=False)
    
    def get(self, get_request, context):
        """funció que fa un get request."""
        # Cridem al algoritme de votació
        from decentralized import node
        value = node.askGetVote(self.store, get_request, context, self.store.get(get_request.key), self.vote_size)
        if value is None:
            return store_pb2.GetResponse(value="", found=False)
        return store_pb2.GetResponse(value=value, found=True)
    
    def askVotePut(self, vote_request, context):
        """Funció quan es rep un ask vote per un put request."""
        # devolver success = True
        time.sleep(self.slow_down_seconds)
        return store_pb2.askVotePutRespone(success=True, vote_size=self.vote_size)
        
    def askVoteGet(self, vote_request, context):
        """Funció quan es rep un ask vote per un get request."""
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
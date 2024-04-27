
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
    
    
class MasterService(StoreService):
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
    
        

store_service = StoreService()
master_service = MasterService()
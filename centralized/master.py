
import grpc
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent import futures
import multiprocessing
try:
    from proto import store_pb2_grpc, store_pb2
    from proto.store_service import master_service
except:
    import sys
    sys.path.append('proto')
    from proto import store_pb2_grpc, store_pb2
from proto.store_service import master_service

store = {}
ipports = []

def main():
    master_service.set_store(store)
    master_service.setnodeIdentifier("Master")
    master_service.load_values()
    master_service.setDiscoverQueue(ipports)

    iniciar_grpcApi()
  
    
    while True:
        time.sleep(86400)
        pass

    
def iniciar_grpcApi():
    """Funció que inicialitza el servidor gRPC."""
    # Inicialitzem el servidor gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(master_service, server)
    #will run the master node on port 32770
    server.add_insecure_port('localhost:32770')
    server.start()
    server.wait_for_termination()
    
def two_phase_commit(store, put_request, context):
    """Funció que fa un put amb 2 phase commit."""
    try:
        for ipport in ipports:
            
            channel = grpc.insecure_channel(ipport)

            # create a stub (client)
            stub = store_pb2_grpc.KeyValueStoreStub(channel) #MessagingServiceStub metode del .proto
            
            # create a valid request message
            doCommit = store_pb2.CommitRequest(key=put_request.key, value=put_request.value)
            pot = stub.canCommit(doCommit) #sendMessage metode del grpc server
            if not pot.success:
                return False
        # si estem aqui es que tots els slaves han dit que si
        for ipport in ipports:
            channel = grpc.insecure_channel(ipport)
            stub = store_pb2_grpc.KeyValueStoreStub(channel)
            doCommit = store_pb2.doCommitRequest(key=put_request.key, value=put_request.value)
            pot = stub.doCommit(doCommit)
            if not pot.success:
                return False
        return True
    except:
        # in case of a node failing in the middle of the process
        return False
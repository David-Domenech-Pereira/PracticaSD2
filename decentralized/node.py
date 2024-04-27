
import grpc
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent import futures
try:
    from proto import store_pb2_grpc, store_pb2
    from proto.store_service import node_service
except:
    import sys
    sys.path.append('proto')
    from proto import store_pb2_grpc, store_pb2
from proto.store_service import node_service

quorum_put = 3
quorum_get = 2
ipports = ['localhost:32771','localhost:32771', 'localhost:32772'] # TODO detect neighbors
ipport_loc = ""
global this_vote_size
this_vote_size = 1
def main(port):
    ipport_loc = "localhost:"+str(port)
   
    # si es el segundo ponemos voto 2
    if port == 32771:
        print("Vote size 2")
        node_service.setVoteSize(2)
        this_vote_size = 2
    else:
         node_service.setVoteSize(1)
    iniciar_grpcApi(port)

def iniciar_grpcApi(port):
    # Inicialitzem el servidor gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(node_service, server)
    #will run the master node on port 32770
    print('localhost:'+str(port))
    server.add_insecure_port('localhost:'+str(port))
    server.start()
    server.wait_for_termination()
    
    
def askPutVote(store, put_request, context):
    # send a vote request to all nodes
    votos_totales = 0
    for ipport in ipports:
        if ipport == ipport_loc:
            votos_totales += this_vote_size
            continue
        channel = grpc.insecure_channel(ipport)
        stub = store_pb2_grpc.KeyValueStoreStub(channel)
        doCommit = store_pb2.askVotePutRequest(key=put_request.key, value=put_request.value)
        pot = stub.askVotePut(doCommit)
        if pot.success:
            votos_totales += pot.vote_size
    print("Votos totales: "+str(votos_totales))
    #si es >= quorum_put
    if votos_totales >= quorum_put:
        print("DoCommit")
        # hacemos un doCommit
        for ipport in ipports:
            channel = grpc.insecure_channel(ipport)
            stub = store_pb2_grpc.KeyValueStoreStub(channel)
            doCommit = store_pb2.doCommitRequest(key=put_request.key, value=put_request.value)
            pot = stub.doCommit(doCommit)
            if not pot.success:
                return False
        return True
    else:
        return False
        
    
def askGetVote(store, get_request, context, local_value, local_vote_size):
    # send a vote request to all nodes
    values ={}
    values[local_value] = local_vote_size
    for ipport in ipports:
        if ipport == ipport_loc:
            continue
        channel = grpc.insecure_channel(ipport)
        stub = store_pb2_grpc.KeyValueStoreStub(channel)
        doCommit = store_pb2.askVoteGetRequest(key=get_request.key)
        pot = stub.askVoteGet(doCommit)
        if pot.success:
            if pot.value in values:
                values[pot.value] += pot.vote_size
            else:
                values[pot.value] = pot.vote_size
    #Cogemos el valor con mas votos y >= quorum_get
    max_value = local_value
    max_vote = local_vote_size
    for key in values:
        if values[key] > max_vote:
            max_vote = values[key]
            max_value = key
    if max_vote >= quorum_get:
        return max_value
    else:
        return None
    

import grpc
import time
import socket
import random
import json
from concurrent.futures import ThreadPoolExecutor
from concurrent import futures
import multiprocessing
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
ipports = [] 
ipport_loc = ""
global this_vote_size
this_vote_size = 1

def listen_for_broadcasts(sock):
    """Funció que escolta tots els broadcasts (nous nodes).
    Si rep un broadcast, respon amb la seva informació.
    Si rep una resposta, guarda la informació del node.
    @param sock: socket per escoltar els broadcasts.
    """
    # Cada node tindrà un port random entre 25000 i 26000
    # Només es permeten 1000 nodes
   
    
    
   

    while True:
        data, addr = sock.recvfrom(1024)
     
        # parse data
        # si empieza por Discovery; es un mensaje de descubrimiento
        if data.startswith(b"Discovery;"):
            parts = data.decode().split(";")
            if len(parts) == 2 and parts[0] == "Discovery":
                ipport = parts[1]
                if ipport not in ipports:
                    ipports.append(ipport)
                    try:
                        response = "DiscoveryResponse;-;"+node_service.parseJson()
                        sock.sendto(response.encode(), addr)
                    except Exception as e:
                        print("Error sending response: "+str(e))
                    
        # si empieza por DiscoveryResponse; es un mensaje de respuesta
        elif data.startswith(b"DiscoveryResponse;"):
        
            parts = data.decode().split(";-;")

            if len(parts) == 2 and parts[0] == "DiscoveryResponse":
                data = parts[1]
                data = data.encode()
                # decode the response, we get the json and add manually to the list
                data = data.decode()
                data = json.loads(data)
                # we recieve key=>value con los valores para no perder consistencia
                # no se recibe ippuertos, sino valores para añadir a la lista
                for key in data:
                    node_service.store[key] = data[key]
                   
                
        

def send_broadcast(ipport,sock):
    """Función que envia una trama broadcast a tots els ports enre 25000 i 26000.
    Parametros:
    @param ipport -- ip i port del node actual
    @param sock -- socket per enviar els broadcasts
    """
    for port in range(25000, 26000):
        sock.sendto(b"Discovery;"+bytes(ipport,"utf-8"), ('255.255.255.255', port))  # Cambiado a puerto 5000
        




def main(port):
    # encendemos el listener de broadcasts
    port_socket = 25000 + random.randint(0, 1000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    sock.bind(('', port_socket))  # Cambiado a puerto 5000
    listener_thread = futures.ThreadPoolExecutor(max_workers=1)
    listener_thread.submit(listen_for_broadcasts,sock)
    ipport_loc = "localhost:"+str(port)
    node_service.setnodeIdentifier("Node"+str(port))
    node_service.load_values()
    send_broadcast(ipport_loc,sock)
    # si es el segundo ponemos voto 2
    if port == 32771:
        # TODO Que fem amb això?
        print("Vote size 2")
        node_service.setVoteSize(2)
        this_vote_size = 2
    else:
         node_service.setVoteSize(1)

    
    iniciar_grpcApi(port)

def iniciar_grpcApi(port):
    """Funció que inicialitza el servidor gRPC.
    @param port: port del servidor gRPC.
    """
    # Inicialitzem el servidor gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(node_service, server)
    #will run the master node on port 32770
    print('localhost:'+str(port))
    server.add_insecure_port('localhost:'+str(port))
    server.start()
    server.wait_for_termination()
    
    
def askPutVote(put_request):
    """Funció que fa una votació per fer un put.
    @param put_request: petició de put que ha rebut
    """
    # send a vote request to all nodes
    try:
        votos_totales = 0
        for ipport in ipports:
            if ipport == ipport_loc:
                # comptem a nosaltres
                votos_totales += this_vote_size
                continue
            # fem la crida grpc
            channel = grpc.insecure_channel(ipport)
            stub = store_pb2_grpc.KeyValueStoreStub(channel)
            doCommit = store_pb2.askVotePutRequest(key=put_request.key, value=put_request.value)
            pot = stub.askVotePut(doCommit)
            if pot.success:
                # si ha dit que si sumem els vots
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
                    # si falla algun return False
                    return False
            return True
        else:
            return False
    except:
        # en caso de que caiga algo
        return False
        
    
def askGetVote( get_request,  local_value, local_vote_size):
    # send a vote request to all nodes
    try:
        values ={}
        values[local_value] = local_vote_size
        for ipport in ipports:
            if ipport == ipport_loc:
                # comptem a nosaltres
                continue
            # fem la crida grpc
            channel = grpc.insecure_channel(ipport)
            stub = store_pb2_grpc.KeyValueStoreStub(channel)
            doCommit = store_pb2.askVoteGetRequest(key=get_request.key)
            pot = stub.askVoteGet(doCommit)
            if pot.success:
                # si ha dit que si sumem els vots
                if pot.value in values:
                    # si ja hi es sumem
                    values[pot.value] += pot.vote_size
                else:
                    # si no hi es creem
                    values[pot.value] = pot.vote_size
                    
        #Cogemos el valor con mas votos y >= quorum_get
        max_value = local_value
        max_vote = local_vote_size
        for key in values:
            # si te mas votos y es >= quorum_get
            if values[key] > max_vote:
                max_vote = values[key]
                max_value = key
        # solo devolvemos el valor si tiene mas votos que el mínimo
        # sino no hay consenso
        if max_vote >= quorum_get:
            return max_value
        else:
            return None
    except:
        # en caso de que caiga algo
        return None
    
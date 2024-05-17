from concurrent import futures
import time
import grpc
import json

from proto import store_pb2_grpc, store_pb2

from proto.store_service import store_service

store = {}


def main(port):
    store_service.set_store(store)
    store_service.setnodeIdentifier("Slave"+str(port))
    store_service.load_values()
    registrarClient("localhost",port)
    
    time.sleep(1)
    iniciar_grpcApi(port)
    while True:
        #infinite loop
        pass
    
def iniciar_grpcApi(port):
    """Funció que inicialitza el servidor gRPC."""
    # Inicialitzem el servidor gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(store_service, server)
    #will run the master node on port 32770
    server.add_insecure_port('localhost:'+str(port))
    server.start()
    server.wait_for_termination()

    
    
def registrarClient(ip, port):
    """Funció que registra un nou client al servidor master."""
    
    master="localhost:32770"
    channel = grpc.insecure_channel(master)

    # create a stub (client)
    stub = store_pb2_grpc.KeyValueStoreStub(channel) #MessagingServiceStub metode del .proto
    
    response = stub.discoverMessage(store_pb2.dMessage(ip=ip, port=port))
    
    # decode the response, we get the json and add manually to the list
    data = response.data
    data = json.loads(data)
    # we recieve key=>value con los valores para no perder consistencia
    # no se recibe ippuertos, sino valores para añadir a la lista
    for key in data:
        store_service.store[key] = data[key]
        store_service.store_values(key, data[key])
    
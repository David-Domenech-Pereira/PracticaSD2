from concurrent import futures
import time
import grpc

from proto import store_pb2_grpc, store_pb2

from proto.store_service import store_service

store = {}


def main(port):
    store_service.set_store(store)
    registrarClient("localhost",port)
    
    time.sleep(1)
    iniciar_grpcApi(port)
    while True:
        #infinite loop
        pass
    
def iniciar_grpcApi(port):
    # Inicialitzem el servidor gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(store_service, server)
    #will run the master node on port 32770
    print('localhost:'+str(port))
    server.add_insecure_port('localhost:'+str(port))
    server.start()
    server.wait_for_termination()

    
    
def registrarClient(ip, port):
    
    master="localhost:32770"
    channel = grpc.insecure_channel(master)

    # create a stub (client)
    stub = store_pb2_grpc.KeyValueStoreStub(channel) #MessagingServiceStub metode del .proto
    
    stub.discoverMessage(store_pb2.dMessage(ip=ip, port=port))
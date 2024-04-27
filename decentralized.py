# The system must be launched using only one script per version: centralised.py to launch the centralised, master-slave server

from decentralized import node



def iniciar_threadSlaves():
    # Creem un thread per a cada slave
    # Cada thread executa el centralized/slave.py (el servidor esclau)
    
    ports = [32770,32771, 32772]
    n_threads = len(ports)
    for i in range(n_threads):
        print('Starting slave on port: '+str(ports[i]))
        thread = threading.Thread(target=node.main, args=(ports[i],))
        thread.start()
        


import threading



iniciar_threadSlaves()

while True:
    # infinite loop
    pass
        
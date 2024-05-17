# The system must be launched using only one script per version: centralised.py to launch the centralised, master-slave server

from decentralized import node



def iniciar_threadNodes():
    # Creem un thread per a cada node
    # Cada thread executa el main de decentralized/node.py (el servidor node)
    
    ports = [32770,32771, 32772]
    n_threads = len(ports)
    for i in range(n_threads):
        print('Starting decentralized node on port: '+str(ports[i]))
        thread = threading.Thread(target=node.main, args=(ports[i],))
        thread.start()
        


import threading



iniciar_threadNodes()

while True:
    # infinite loop
    pass
        
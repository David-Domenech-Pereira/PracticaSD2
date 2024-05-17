# The system must be launched using only one script per version: centralised.py to launch the centralised, master-slave server

from centralized import master, slave


def iniciar_threadMaster():
    # Creem un thread, que executa el centralized/master.py (el servidor centralitzat)
    
    threadMaster = threading.Thread(target=master.main)
    threadMaster.start()

def iniciar_threadSlaves():
    # Creem un thread per a cada slave
    # Cada thread executa el centralized/slave.py (el servidor esclau)
    
    ports = [32771, 32772]
    n_threads = len(ports)
    for i in range(n_threads):
        thread = threading.Thread(target=slave.main, args=(ports[i],))
        thread.start()
        


import threading

iniciar_threadMaster()

iniciar_threadSlaves()

while True:
    # infinite loop
    pass
        
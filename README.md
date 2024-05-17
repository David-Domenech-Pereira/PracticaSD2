# Distributed storage systems and the CAP theorem

This project is developed under the course of Distributed Systems at the Universitat Rovira i Virgili, Tarragona, Spain. The project aims to implement two distributed storage systems, a centralized and a decentralized one, and evaluate their performance in terms of the CAP theorem.

For more information, please refer to the project documentation.

@Authors: Assmaa Ouladali (assmaa.ouladali@estudiants.urv.cat) and David Domènech Pereira Da Silva (david.domenechp@estudiants.urv.cat)

Copyright 2024, Universitat Rovira i Virgili, Tarragona, Spain

# Running the centralized and decentralized storage systems

To run the centralized storage system, use the following command:

```bash python centralized.py```

To run the decentralized storage system, use the following command:

```bash python decentralized.py```

To run the tests for the centralized storage system, use the following command:

```bash python eval/test_centralized_system.py```

To run the tests for the decentralized storage system, use the following command:

```bash python eval/test_decentralized_system.py```

To run both tests, use the following command:

```bash python eval/eval.py```

# Directory Structure
```
Project/

├── README.md
├── centralized/
│   ├── master.py
│   ├── slave.py
├── decentralized/
│   ├── node.py 
│
├── proto/
│   ├── store.proto
│   ├── store_pb2.py
│   └── store_pb2_grpc.py
│
├── config_centralized.yaml
├── centralized.py
├── decentralized.py
├── eval/
│   ├── test_centralized_system.py
│   └── test_decentralized_system.py
│

```

## Directory Structure Explanation

- **centralized.py**: Contains the implementation of the centralized storage system. The system is implemented as a gRPC server that listens for requests from clients. The server stores key-value pairs in memory and responds to client requests for reading and writing data.

- **decentralized.py**: Contains the implementation of the decentralized storage system. The system is implemented as a gRPC server that listens for requests from clients. The server stores key-value pairs in memory and responds to client requests for reading and writing data. The decentralized system uses a gossip protocol to replicate data across multiple nodes in the system.

- **proto/**: Contains Protocol Buffer files used for defining gRPC services and messages. Generated Python files (`store_pb2.py` and `store_pb2_grpc.py`) based on `store.proto` should be stored here.

- **centralized_config.yaml and decentralized_config.yaml**: YAML configuration files containing settings for the centralized and decentralized systems.

- **eval/**: Directory containing evaluation scripts and tests.

  - **test_centralized_system.py**: Script containing unit tests for the centralized system.

    
  
  - **test_decentralized_system.py**: Script containing unit tests for the decentralized system.

    

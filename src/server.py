import sys
import os
from concurrent import futures
import grpc
from bio_sequence_services import bioSequencesService_pb2, bioSequencesService_pb2_grpc
import traceback
from src.BIO_transform import BIO_TRANSFORM

def Server(port=5001, database_base_path='/'):
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        
      
        bioSequencesService_pb2_grpc.add_biosequenceservicesServicer_to_server(
            BIO_TRANSFORM(database_base_path=database_base_path),
            server
        )
        
        server.add_insecure_port(f'[::]:{port}')
        server.start()
        print(f"server running on port {port}")
        server.wait_for_termination()

    except grpc.RpcError as error:
        print(f"Type: {type(error).__name__}")
        print(f"Details: {error}")
        traceback.print_exc()


    except Exception as error:
        print("\n==== INTERNAL SERVER ERROR ====")
        print(f"Type: {type(error).__name__}")
        print(f"Details: {error}")
        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("You should set a port number")
    if len(sys.argv) < 3:
        database_base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database')
        os.makedirs(database_base_path,exist_ok=True)
    else:
        database_base_path = sys.argv[2]
    try:
        port = int(sys.argv[1])
        Server(port=port,database_base_path=database_base_path)

    except Exception as e:
        port = 5001
        Server(port=port)
        raise RuntimeError(f"Error {e}. Set port {port} to server")


from bio_sequence_services import bioSequencesService_pb2, bioSequencesService_pb2_grpc
import os
from threading import Lock

class processProtobufFile:

    @staticmethod
    def save_object_protobuf(destine_file: str, protobuf_obj, lock):
        try:
            with lock:
                data = protobuf_obj.SerializeToString()

                with open(destine_file, "wb") as f:
                    f.write(data)

        except IOError as error:
            raise error
        except Exception as error:
            raise error

    @staticmethod
    def load_object_protobuf(file_path: str, protobuf_class, lock):

        try:
            with lock:
                with open(file_path, "rb") as f:
                    data = f.read()

            obj = protobuf_class()           
            obj.ParseFromString(data)        
            return obj

        except IOError as error:
            raise error
        except Exception as error:
            raise error




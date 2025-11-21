import os
import grpc
from bio_sequence_services import bioSequencesService_pb2, bioSequencesService_pb2_grpc
from src.bio_processor import BIO_Processor
from src.process_protoburf_file import processProtobufFile


class BIO_TRANSFORM(bioSequencesService_pb2_grpc.biosequenceservicesServicer):

    def __init__(self, database_base_path=None):
        self.database_base_path = database_base_path
        self.nucleotides_sequences_path = 'nucleotides_sequences'
        self.Numeric_codons_sequences = 'numericCodonsSequences'
        self.proteinSequences = 'proteinSequences'
        self.STATE_MAP = {
            bioSequencesService_pb2.StatusDataset.state_origin: "state_origin",
            bioSequencesService_pb2.StatusDataset.state_transformed_to_codon: "state_transformed_to_codon",
            bioSequencesService_pb2.StatusDataset.state_protein: "state_protein"
        }

        super().__init__()

    def receive_sequeces(self, request, context):
        try:
            sequences = list(request.sequences)
            dataset_id = request.dataset_id_process

            if not sequences:
                return bioSequencesService_pb2.ResponseStore(
                    status=False,
                    msg="Empty nucleotide sequence list"
                )

            if not dataset_id:
                return bioSequencesService_pb2.ResponseStore(
                    status=False,
                    msg="dataset_id is required"
                )

            dest_dir = os.path.join(
                self.database_base_path, 
                dataset_id, 
                self.nucleotides_sequences_path
            )
            os.makedirs(dest_dir, exist_ok=True)

            
            filepath = os.path.join(dest_dir, "sequences.pb")

           
            sequence_pb = bioSequencesService_pb2.StoreNucleotid_processeSequences()
            sequence_pb.sequences.extend(sequences)
            sequence_pb.dataset_id_process = dataset_id  # CORRETO



            processProtobufFile.save_object_protobuf(
                    destine_file=filepath,
                    protobuf_obj=sequence_pb
                )

            return bioSequencesService_pb2.ResponseStore(
                status=True,
                msg="Nucleotide sequences stored successfully"
            )

        except grpc.RpcError as error:
            return bioSequencesService_pb2.ResponseStore(
                status=False,
                msg=f"gRPC error: {error}"
            )

        except Exception as error:
            return bioSequencesService_pb2.ResponseStore(
                status=False,
                msg=f"Internal error: {error}"
            )


    def nucleotid_processesToCodons(self, request, context):
        try:
            id_process = request.dataset_id_process
            dataset_dir = os.path.join(self.database_base_path, id_process)
            nucleotides_sequences_path = os.path.join(dataset_dir, self.nucleotides_sequences_path, 'sequences.pb')

            if not os.path.exists(nucleotides_sequences_path):
                return bioSequencesService_pb2.ResponseTransformNToC(
                    status=False,
                    msg=f"Not found nucleotide sequences for id process: {id_process}"
                )

            sequence_pb = processProtobufFile.load_object_protobuf(
                file_path=nucleotides_sequences_path,
                protobuf_class=bioSequencesService_pb2.StoreNucleotid_processeSequences
            )

            numeric_codons_seq_pb = bioSequencesService_pb2.NumericCodonsSequence()
            numeric_codons_seq_pb.id_process = id_process

            for seq in sequence_pb.sequences:  
                codons_list = BIO_Processor.nucleotideSequenceToCodons(seq)
                codon_seq_pb = bioSequencesService_pb2.NumericCodons()
                codon_seq_pb.codon_sequence.extend(codons_list) 
                numeric_codons_seq_pb.sequences.append(codon_seq_pb)



            dest_dir = os.path.join(dataset_dir, self.Numeric_codons_sequences)
            os.makedirs(dest_dir, exist_ok=True)
            filepath = os.path.join(dest_dir, "numeric_codons_sequences.pb")

            processProtobufFile.save_object_protobuf(
                destine_file=filepath,
                protobuf_obj=numeric_codons_seq_pb
            )

            return bioSequencesService_pb2.ResponseTransformNToC(
                status=True,
                msg='Sequences transformed successfully'
            )

        except grpc.RpcError as error:
            return bioSequencesService_pb2.ResponseTransformNToC(
                status=False,
                msg=f"gRPC error: {error}"
            )

        except Exception as error:
            return bioSequencesService_pb2.ResponseTransformNToC(
                status=False,
                msg=f"Internal error: {error}"
            )


    def codonToProtain(self, request, context):
        try:
            id_process = request.dataset_id_process
            dataset_dir = os.path.join(self.database_base_path, id_process)
            nucleotides_sequences_path = os.path.join(dataset_dir, self.nucleotides_sequences_path, 'sequences.pb')

            if not os.path.exists(nucleotides_sequences_path):
                return bioSequencesService_pb2.ResponseTransformNToC(
                    status=False,
                    msg=f"Not found nucleotide sequences for id process: {id_process}"
                )

            sequence_pb = processProtobufFile.load_object_protobuf(
                file_path=nucleotides_sequences_path,
                protobuf_class=bioSequencesService_pb2.StoreNucleotid_processeSequences
            )

            protein_pb = bioSequencesService_pb2.Protein()
            protein_pb.id_process = id_process
            all_proteins = protein_pb.protein  

            for nucleotide_sequence in sequence_pb.sequences:
                protein = BIO_Processor.nucleotide_list_to_protein(nucleotide_sequence)
                all_proteins.append(protein)  

         

            dest_dir = os.path.join(dataset_dir, self.proteinSequences)
            os.makedirs(dest_dir, exist_ok=True)
            filepath = os.path.join(dest_dir, "proteinSequences.pb")

            processProtobufFile.save_object_protobuf(
                destine_file=filepath,
                protobuf_obj=protein_pb
            )

            return bioSequencesService_pb2.ResponsetraductionToProtein(
                status=True,
                msg='Sequences transformed successfully'
            )

        except grpc.RpcError as error:
            return bioSequencesService_pb2.ResponsetraductionToProtein(
                    status=False,
                    msg=f"gRPC error: {error}"
                )

        except Exception as error:
            return bioSequencesService_pb2.ResponsetraductionToProtein(
                    status=False,
                    msg=f"Internal error: {error}"
                )

    def getDataset(self, request, context):
        try:

            id_process = request.dataset_id_process
            dataset_dir = os.path.join(self.database_base_path, id_process)

            state = request.status_dataset

                
            if not os.path.exists(dataset_dir):
                return bioSequencesService_pb2.ResponsegetDataset(
                    status=False,
                    msg=f"Dataset base not found for client: {id_process}"
                )

            state_str = self.STATE_MAP.get(state)

            if state_str is None:
                return bioSequencesService_pb2.ResponsegetDataset(
                    status=False,
                    msg=f"Invalid state code {state}"
                )
            
            print(type(state_str))
            print(state_str)
            response = bioSequencesService_pb2.ResponsegetDataset()

            response.dataset_id_process = id_process
            response.status_dataset = state
            response.status = True
            response.msg = "Dataset loaded successfully"

            response.dataset.CopyFrom(
                self.get_dataset_response(id_process=id_process, state=state_str)
            )

            return response



        except grpc.RpcError as error:
            return bioSequencesService_pb2.ResponsegetDataset(
                    status=False,
                    msg=f"gRPC error: {error}"
                )

        except Exception as error:
            return bioSequencesService_pb2.ResponsegetDataset(
                    status=False,
                    msg=f"Internal error: {error}"
                )
    

    def get_dataset_response(self, id_process: str, state: str):
        try:

            """
            Builds a ResponsegetDataset depending on the dataset state.

            state can be:
                - "state_origin" : returns nucleotide sequences
                - "state_transformed_to_codon" : returns codon sequences
                - "state_protein" : returns protein sequences
            """

           

            dataset_dir = os.path.join(self.database_base_path, id_process)

            dataset = bioSequencesService_pb2.Dataset_response()
            
           
            if state == 'state_origin':
                nucleotides_sequences_path = os.path.join(
                    dataset_dir,
                    self.nucleotides_sequences_path,
                    'sequences.pb'
                )

                sequence_pb = processProtobufFile.load_object_protobuf(
                    file_path=nucleotides_sequences_path,
                    protobuf_class=bioSequencesService_pb2.StoreNucleotid_processeSequences
                )

                dataset.nucleotid_processes_sequences.CopyFrom(sequence_pb)
            
            elif state == 'state_transformed_to_codon':
                codons_sequences_path = os.path.join(
                    dataset_dir,
                    self.Numeric_codons_sequences,
                    'numeric_codons_sequences.pb'
                )

                codons_pb = processProtobufFile.load_object_protobuf(
                    file_path=codons_sequences_path,
                    protobuf_class=bioSequencesService_pb2.NumericCodonsSequence
                )

                dataset.codo_sequences.CopyFrom(codons_pb)

            elif state == 'state_protein':
                protein_sequences_path = os.path.join(
                    dataset_dir,
                    self.proteinSequences,
                    'proteinSequences.pb'
                )

                protein_pb = processProtobufFile.load_object_protobuf(
                    file_path=protein_sequences_path,
                    protobuf_class=bioSequencesService_pb2.Protein
                )

                dataset.proteins.append(protein_pb)
            
            return dataset


        except FileNotFoundError as error:
            raise error
        
        except Exception as error:
            raise error
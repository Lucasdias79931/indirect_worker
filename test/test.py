import grpc
from bio_sequence_services import bioSequencesService_pb2, bioSequencesService_pb2_grpc
import os
import traceback
from Bio.SeqIO.FastaIO import SimpleFastaParser

here = os.path.abspath(os.path.dirname(__file__))
dataset_path = os.path.join(here, "file_to_test/sequencias_tratadas.fasta")

print("here =", here)
print("dataset_path =", dataset_path)
print("exists?", os.path.exists(dataset_path))



try:
    all_sequences = []
    with open(dataset_path, "r") as file:
        for header, sequence in SimpleFastaParser(file):
            all_sequences.append(sequence)

except FileNotFoundError as e:
    print(f"Error: {e}")
    exit(1)

except Exception as e:
    print(f"Erro genérico: {e}")
    traceback.print_exc()
    exit(1)

host = "localhost"
port = 50052
channel = grpc.insecure_channel(f"{host}:{port}")
stub = bioSequencesService_pb2_grpc.biosequenceservicesStub(channel)

try:

    print("test to service receive_sequeces ")
    request = bioSequencesService_pb2.StoreNucleotid_processeSequences(
        dataset_id_process="teste01",
        sequences=all_sequences
    )

    response = stub.receive_sequeces(request)

    print("Status:", response.status)
    print("Mensagem:", response.msg)
except Exception as error:
    print(f"error: {error}")
    exit(1)



try:

    print("test to service nucleotid_processesToCodons ")
    request = bioSequencesService_pb2.TransformFromNucleotid_processesToCodons(
        dataset_id_process="teste01"
    )

    response = stub.nucleotid_processesToCodons(request)

    print("Status:", response.status)
    print("Mensagem:", response.msg)
except Exception as error:
    print(f"error: {error}")
    exit(1)



try:

    print("test to service codonToProtain ")
    request = bioSequencesService_pb2.traductionToProtein(
        dataset_id_process="teste01"
    )

    
    response = stub.codonToProtain(request)

    print("Status:", response.status)
    print("Mensagem:", response.msg)
except Exception as error:
    print(f"error: {error}")
    exit(1)

try:
    print("test to service getDataset")

    #
    # === TESTE 1 : NUCLEOTÍDEOS ===
    #
    request = bioSequencesService_pb2.Dataset(
        dataset_id_process="teste01",
        status_dataset=bioSequencesService_pb2.StatusDataset.state_origin
    )

    response = stub.getDataset(request)

    print("\n--- NUCLEOTÍDEOS ---")
    all_sequences = [seq for seq in response.dataset.nucleotid_processes_sequences.sequences]
    print("Primeiros nucleotídeos da primeira sequência:", all_sequences[0][:10])
    print("Status:", response.status)
    print("Mensagem:", response.msg)



    #
    # === TESTE 2 : CÓDONS NUMÉRICOS ===
    #
    request = bioSequencesService_pb2.Dataset(
        dataset_id_process="teste01",
        status_dataset=bioSequencesService_pb2.StatusDataset.state_transformed_to_codon
    )

    response = stub.getDataset(request)

    print("\n--- CÓDONS NUMÉRICOS ---")
    all_codon_sequences = [
        list(codon_seq.codon_sequence)
        for codon_seq in response.dataset.codo_sequences.sequences
    ]

    print("Primeiros códigos da primeira sequência:", all_codon_sequences[0][:10])
    print("Status:", response.status)
    print("Mensagem:", response.msg)



    #
    # === TESTE 3 : PROTEÍNAS ===
    #
    request = bioSequencesService_pb2.Dataset(
        dataset_id_process="teste01",
        status_dataset=bioSequencesService_pb2.StatusDataset.state_protein
    )

    response = stub.getDataset(request)

    print("\n--- PROTEÍNAS ---")
    all_proteins = list(response.dataset.proteins[0].protein)
    print("Primeiros aminoácidos da primeira proteína:", all_proteins[0][:10])
    print("Status:", response.status)
    print("Mensagem:", response.msg)
   

except Exception as error:
    print(f"error: {error}")
    exit(1)



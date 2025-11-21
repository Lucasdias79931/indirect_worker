# Exemplo de Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 


RUN python -m grpc_tools.protoc \
    -I./bio_sequence_services \
    --python_out=./bio_sequence_services \
    --grpc_python_out=./bio_sequence_services \
    ./bio_sequence_services/bioSequencesService.proto


RUN sed -i 's/^import bioSequencesService_pb2/from . import bioSequencesService_pb2/g' bio_sequence_services/bioSequencesService_pb2_grpc.py
# -----------------------------------------------------------

# Comando de execução
CMD ["python", "-m", "src.server", "50051", "dataset/"]
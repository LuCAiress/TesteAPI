from fastapi import FastAPI, Request
from pydantic import BaseModel, EmailStr
import boto3
import json
import os

class Pedido(BaseModel):
    email: EmailStr       # força ser email válido
    order_id: str         # ID do pedido (string obrigatória)
    details: str        # detalhes do pedido (pode ser JSON livre)

app = FastAPI()

s3_client = boto3.client("s3")
BUCKET_NAME = "pedido-novo-empresa"

@app.post("/pedido")
async def salvar_pedido(pedido: Pedido):
    # Converte o objeto para dict
    pedido_dict = pedido.model_dump()

    # Nome único do arquivo
    file_name = f"order-file.json"

    # Salva no S3
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=file_name,
        Body=json.dumps(pedido_dict),
        ContentType="application/json"
    )

    return {"status": "sucesso", "arquivo": file_name}

@app.get("/")
def read_root():
    return {"Hello": "World"}

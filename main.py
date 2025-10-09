from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import boto3
import json
from dotenv import load_dotenv
import os

load_dotenv()

class Pedido(BaseModel):
    email: EmailStr       # força ser email válido
    order_id: str         # ID do pedido (string obrigatória)
    details: str        # detalhes do pedido (pode ser JSON livre)

app = FastAPI()

# AWS Credentials
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Configure S3 client with credentials
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # permite todos os métodos: GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # permite todos os headers
)

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

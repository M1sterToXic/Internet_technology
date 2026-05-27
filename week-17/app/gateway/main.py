from fastapi import FastAPI, HTTPException
import grpc
import sys
from pathlib import Path
from pydantic import BaseModel
from typing import List

PROTO_DIR = Path(__file__).resolve().parent.parent / 'proto'
sys.path.insert(0, str(PROTO_DIR))

import invoices_pb2
import invoices_pb2_grpc

app = FastAPI()

class InvoiceSchema(BaseModel):
    id: str
    name: str
    amount: float

class CreateInvoiceSchema(BaseModel):
    name: str
    amount: float

def get_grpc_client():
    channel = grpc.insecure_channel('invoices-svc-s13:8228')
    return invoices_pb2_grpc.InvoicesServiceStub(channel)

@app.get("/api/invoices", response_model=List[InvoiceSchema])
async def list_invoices():
    client = get_grpc_client()
    try:
        response = client.ListInvoices(invoices_pb2.ListInvoicesRequest())
        return [InvoiceSchema(id=i.id, name=i.name, amount=i.amount) for i in response]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/invoices", response_model=InvoiceSchema, status_code=201)
async def create_invoice(invoice: CreateInvoiceSchema):
    client = get_grpc_client()
    try:
        response = client.CreateInvoice(invoices_pb2.CreateInvoiceRequest(
            name=invoice.name, 
            amount=invoice.amount
        ))
        i = response.invoice
        return InvoiceSchema(id=i.id, name=i.name, amount=i.amount)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

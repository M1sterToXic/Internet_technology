import grpc
from concurrent import futures
import sys
from pathlib import Path

PROTO_DIR = Path(__file__).resolve().parent.parent / 'proto'
sys.path.insert(0, str(PROTO_DIR))

import invoices_pb2
import invoices_pb2_grpc

class InvoicesServiceServicer(invoices_pb2_grpc.InvoicesServiceServicer):
    def __init__(self):
        self._invoices = {
            "1": invoices_pb2.Invoice(id="1", name="Service Fee", amount=150.0),
            "2": invoices_pb2.Invoice(id="2", name="Hardware Purchase", amount=1200.50),
        }

    def GetInvoice(self, request, context):
        invoice = self._invoices.get(request.id)
        if invoice:
            return invoices_pb2.GetInvoiceResponse(invoice=invoice)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details(f'Invoice with id={request.id} not found')
        return invoices_pb2.GetInvoiceResponse()

    def CreateInvoice(self, request, context):
        new_id = str(len(self._invoices) + 1)
        invoice = invoices_pb2.Invoice(id=new_id, name=request.name, amount=request.amount)
        self._invoices[new_id] = invoice
        return invoices_pb2.CreateInvoiceResponse(invoice=invoice)

    def ListInvoices(self, request, context):
        for invoice in self._invoices.values():
            yield invoice

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    invoices_pb2_grpc.add_InvoicesServiceServicer_to_server(InvoicesServiceServicer(), server)
    server.add_insecure_port('[::]:8228')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

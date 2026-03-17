import time
import requests
import grpc
import sys
from pathlib import Path

PROTO_DIR = Path(__file__).resolve().parent.parent / 'proto'
sys.path.insert(0, str(PROTO_DIR))

import service_pb2
import service_pb2_grpc

REST_URL = "http://localhost:8222/api/orders"
GRPC_TARGET = "localhost:50051"
NUM_REQUESTS = 1000


def run_rest_bench():
    print("Starting REST benchmark...")
    start = time.time()
    for _ in range(NUM_REQUESTS):
        try:
            requests.get(f"{REST_URL}/1", timeout=5)
        except requests.exceptions.RequestException:
            pass
    end = time.time()
    print(f"REST: {end - start:.4f} sec")
    return end - start


def run_grpc_bench():
    print("Starting gRPC benchmark...")
    with grpc.insecure_channel(GRPC_TARGET) as channel:
        stub = service_pb2_grpc.OrdersServiceStub(channel)
        start = time.time()
        for _ in range(NUM_REQUESTS):
            stub.GetOrder(service_pb2.GetOrderRequest(id="1"))
        end = time.time()
        print(f"gRPC: {end - start:.4f} sec")
        return end - start


if __name__ == "__main__":
    rest_time = run_rest_bench()
    grpc_time = run_grpc_bench()
    print(f"\nResults:")
    print(f"REST time: {rest_time:.4f} sec ({NUM_REQUESTS / rest_time:.2f} RPS)")
    print(f"gRPC time: {grpc_time:.4f} sec ({NUM_REQUESTS / grpc_time:.2f} RPS)")
    print(f"gRPC is {rest_time / grpc_time:.2f}x faster")

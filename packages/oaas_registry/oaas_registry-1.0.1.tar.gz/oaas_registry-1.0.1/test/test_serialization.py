import unittest
from typing import Dict

import oaas
from oaas_grpc.client.client import OaasGrpcClient
from oaas_grpc.server import OaasGrpcServer
from oaas_simple import OaasSimpleServer, OaasSimpleClient

import test.grpc.test_pb2 as test_pb2
import test.grpc.test_pb2_grpc as test_pb2_grpc
from oaas_registry.oaas_grpc_registry import noop

noop()


oaas.client("ping-pong-grpc-service")(test_pb2_grpc.TestServiceStub)


@oaas.client("ping-pong-simple-service")
class TestSimpleServiceClient:
    def ping(self, text: str) -> Dict:
        ...


@oaas.service("ping-pong-simple-service")
class TestSimpleService:
    def ping(self, text: str) -> Dict:
        return {"text": text + "-pong", "len": len(text)}


@oaas.service("ping-pong-grpc-service")
class TestService(test_pb2_grpc.TestServiceServicer):
    def ping(self, request: test_pb2.Ping, context) -> test_pb2.Pong:
        return test_pb2.Pong(text=request.text + "-pong", len=len(request.text))


class TestGrpcSerialization(unittest.TestCase):
    @staticmethod
    def setUpClass() -> None:
        oaas.register_server_provider(OaasGrpcServer())
        oaas.register_client_provider(OaasGrpcClient())
        oaas.register_server_provider(OaasSimpleServer())
        oaas.register_client_provider(OaasSimpleClient())

        oaas.serve()

    @staticmethod
    def tearDownClass() -> None:
        pass

    def test_grpc_serialization(self) -> None:
        client = oaas.get_client(test_pb2_grpc.TestServiceStub)
        result = client.ping(test_pb2.Ping(text="ping"))

        self.assertEqual("ping-pong", result.text)
        self.assertEqual(4, result.len)

    def test_simple_serialization(self) -> None:
        client = oaas.get_client(TestSimpleServiceClient)
        result = client.ping("ping")

        self.assertEqual("ping-pong", result["text"])
        self.assertEqual(4, result["len"])

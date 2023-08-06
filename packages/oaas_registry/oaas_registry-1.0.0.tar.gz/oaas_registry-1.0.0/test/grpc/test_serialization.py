import unittest
import oaas

# we import these two, to expose the oaas-registry service
import oaas_registry.oaas_grpc_registry

# FIXME: multiple types should be ok
# import oaas_registry.oaas_simple_registry

from oaas_grpc.client.client import OaasGrpcClient
from oaas_grpc.server import OaasGrpcServer

import test.grpc.test_pb2 as test_pb2
import test.grpc.test_pb2_grpc as test_pb2_grpc

oaas.client("ping-pong-service")(test_pb2_grpc.TestServiceStub)


@oaas.service("ping-pong-service")
class TestService(test_pb2_grpc.TestServiceServicer):
    def ping(self, request: test_pb2.Ping, context) -> test_pb2.Pong:
        return test_pb2.Pong(text=request.text + "-pong", len=len(request.text))


class TestGrpcSerialization(unittest.TestCase):
    @staticmethod
    def setUpClass() -> None:
        oaas.register_server_provider(OaasGrpcServer())
        oaas.register_client_provider(OaasGrpcClient())

        oaas.serve()

    @staticmethod
    def tearDownClass() -> None:
        pass

    def test_serialization(self) -> None:
        client = oaas.get_client(test_pb2_grpc.TestServiceStub)
        result = client.ping(test_pb2.Ping(text="ping"))

        self.assertEqual("ping-pong", result.text)
        self.assertEqual(4, result.len)

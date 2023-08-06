import time
from concurrent import futures

import grpc
import oaas
import oaas._registrations as registrations
from oaas_registry_api.rpc.registry_pb2 import OaasServiceDefinition
from oaas_registry_api.rpc.registry_pb2_grpc import OaasRegistryStub

from oaas_grpc.server.find_ips import find_ips


class OaasGrpcServer(oaas.ServerMiddleware):
    def __init__(self, *, port=8999):
        self.port = port

    def serve(self) -> None:
        server_address: str = f"[::]:{self.port}"
        self.server = grpc.server(futures.ThreadPoolExecutor())

        # we add the types to the server and only after we start it we
        # notify the oaas registry about the new services
        for service_definition in registrations.services:
            print(
                f"Added service: {service_definition.gav} as {service_definition.code}"
            )
            service_definition.code.add_to_server(  # type: ignore
                service_definition.code(), self.server
            )

        port = self.server.add_insecure_port(server_address)

        locations = []
        for ip in find_ips():
            locations.append(f"{ip}:{self.port}")

        print(f"listening on {port}")
        self.server.start()

        # we register the services
        registry = oaas.get_client(OaasRegistryStub)

        for service_definition in registrations.services:
            registry.register_service(
                OaasServiceDefinition(
                    namespace=service_definition.namespace,
                    name=service_definition.name,
                    version=service_definition.version,
                    locations=locations,
                )
            )

    def join(self) -> None:
        self.server.wait_for_termination()

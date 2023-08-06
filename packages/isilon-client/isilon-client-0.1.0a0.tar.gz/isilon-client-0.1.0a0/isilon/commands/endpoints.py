import asyncio

from cleo import Command

from isilon import IsilonClient


class EndpointsCommand(Command):
    """
    Endpoints.

    endpoints
    """

    def handle(self):
        isi_client = IsilonClient()
        resp = asyncio.run(isi_client.endpoints())
        self.line(f"{resp}")

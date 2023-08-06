import asyncio
import json

from cleo import Command

from isilon import IsilonClient


class DiscoverabilityCommand(Command):
    """
    Discoverability.

    discoverability
    """

    def handle(self):
        isi_client = IsilonClient()
        resp = asyncio.run(isi_client.discoverability.info())
        self.line(f"{json.dumps(resp, indent=4, sort_keys=True)}")

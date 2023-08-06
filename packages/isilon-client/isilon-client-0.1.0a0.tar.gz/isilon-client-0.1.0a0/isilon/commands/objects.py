import asyncio

from cleo import Command

from isilon import IsilonClient


class ObjectsCommand(Command):
    """
    Objects.

    objects
        {container : Container name.}
        {object : Object name.}
        {--headers=* : HTTP headers.}
        {--data=? : Object data.}
        {--c|create : Create or replace object.}
        {--m|metadata : Show object metadata.}
        {--u|update : Create or update object metadata.}
        {--d|delete : Delete object.}
    """

    def handle(self):
        isi_client = IsilonClient()
        container_name = str(self.argument("container"))
        object_name = str(self.argument("object"))
        if self.option("create"):
            data = self.option("data")
            if data:
                asyncio.run(
                    isi_client.objects.create_large(container_name, object_name, data)
                )
                self.line(f"<options=bold><comment>{object_name}</comment> created.</>")
            else:
                self.line("<error>Please, provides a valid object data.</>")
        elif self.option("metadata"):
            resp = asyncio.run(
                isi_client.objects.show_metadata(container_name, object_name)
            )
            for meta_key, meta_value in resp.items():
                self.line(f"<options=bold>{meta_key}</>: {meta_value}")
        elif self.option("update"):
            pass
        elif self.option("delete"):
            asyncio.run(isi_client.objects.delete(container_name, object_name))
            self.line(f"<options=bold><comment>{object_name}</comment> deleted.</>")
        else:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                isi_client.objects.get_large(container_name, object_name, object_name)
            )
            self.line(f"<options=bold><comment>{object_name}</comment> saved.</>")

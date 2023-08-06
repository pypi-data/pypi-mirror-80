import attr
from aiohttp import ClientSession

@attr.s
class Http:
    session_args = attr.ib(
        type=tuple, factory=tuple, validator=attr.validators.instance_of(tuple)
    )
    session_kwargs = attr.ib(
        type=dict, factory=dict, validator=attr.validators.instance_of(dict)
    )

    async def get(self, url, *args, **kwargs):
        async with ClientSession(*self.session_args, **self.session_kwargs) as session:
            response = await session.get(url, *args, **kwargs)
        return response

    async def get_large_object(self, url, filename, chunk_size=50, *args, **kwargs):
        async with ClientSession(*self.session_args, **self.session_kwargs) as session:
            response = await session.get(url, *args, **kwargs)
            with open(filename, "wb") as f:
                while True:
                    chunk = await response.content.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
        return response

    async def post(self, *args, **kwargs):
        async with ClientSession(*self.session_args, **self.session_kwargs) as session:
            response = await session.post(*args, **kwargs)
        return response

    async def send_large_object(self, url, filename, *args, **kwargs):
        with open(filename, "rb") as f:
            response = await self.put(url, data=f, *args, **kwargs)
        return response

    async def put(self, *args, **kwargs):
        async with ClientSession(*self.session_args, **self.session_kwargs) as session:
            response = await session.put(*args, **kwargs)
        return response

    async def delete(self, *args, **kwargs):
        async with ClientSession(*self.session_args, **self.session_kwargs) as session:
            response = await session.delete(*args, **kwargs)
        return response

    async def head(self, *args, **kwargs):
        async with ClientSession(*self.session_args, **self.session_kwargs) as session:
            response = await session.head(*args, **kwargs)
        return response

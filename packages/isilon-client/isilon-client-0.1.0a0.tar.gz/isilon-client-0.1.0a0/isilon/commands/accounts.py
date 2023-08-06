import asyncio

from cleo import Command

from isilon import IsilonClient


class AccountsCommand(Command):
    """
    Accounts.

    accounts
        {account : Account name.}
        {--headers=* : HTTP headers.}
        {--s|show : Create or replace object.}
        {--u|update : Create, update or delete account metadata.}
        {--m|metadata : Show account metadata.}
    """

    def handle(self):
        isi_client = IsilonClient()
        account_name = str(self.argument("account"))
        if self.option("show"):
            resp = asyncio.run(isi_client.accounts.show(account_name))
            self.line(f"{resp}")
        elif self.option("update"):
            resp = asyncio.run(isi_client.accounts.update(account_name))
            self.line(f"{resp.status}")
        elif self.option("metadata"):
            resp = asyncio.run(isi_client.accounts.metadata(account_name))
            for meta_key, meta_value in resp.items():
                self.line(f"<options=bold>{meta_key}</>: {meta_value}")

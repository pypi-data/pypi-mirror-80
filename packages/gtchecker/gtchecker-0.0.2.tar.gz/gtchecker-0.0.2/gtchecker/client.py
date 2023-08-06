from __future__ import print_function
from aiohttp import ClientSession
from asyncio import get_event_loop, AbstractEventLoop
from json import loads

from . import errors

class Client:
    """
    API client for gtchecker.com
    """
    def __init__(self, token: str = None, *, loop:AbstractEventLoop=None):
        self.token = token
        self.session = ClientSession(loop=loop if loop else get_event_loop())

    async def get_gamertag(self, gamertag: str):
        """
        :param gamertag: Request chosen Gamertag
        """
        headers = {'Authorization': self.token}
        if not self.token:
            raise errors.InvalidTokenError("No token was supplied")
        r = await self.session.post("https://gtchecker.com/api/v1/xbox?gamertag={}".format(gamertag), headers=headers)

        if r.status != 200:
            raise errors.InvalidTokenError("Invalid token was supplied")
            
    async def get_psn(self, psn: str):
        """
        :param psn: Request chosen Gamertag
        """
        headers = {'Authorization': self.token}
        if not self.token:
            raise errors.InvalidTokenError("No token was supplied")
        r = await self.session.post("https://gtchecker.com/api/v1/psn?psn={}".format(psn), headers=headers)

        if r.status != 200:
            raise errors.InvalidTokenError("Invalid token was supplied")


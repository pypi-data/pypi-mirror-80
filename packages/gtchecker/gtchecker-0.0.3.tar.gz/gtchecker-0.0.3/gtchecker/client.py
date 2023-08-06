from __future__ import print_function
import requests
from asyncio import get_event_loop, AbstractEventLoop
from json import loads

from . import errors

class Client:
    """
    API client for gtchecker.com
    """
    def __init__(self, token: str = None, *):
        self.token = token
        

    async def get_gamertag(self, gamertag: str):
        """
        :param gamertag: Request chosen Gamertag
        """
        headers = {'Authorization': self.token}
        if not self.token:
            raise errors.InvalidTokenError("No token was supplied")
        r = await request.post("https://gtchecker.com/api/v1/xbox?gamertag={}".format(gamertag), headers=headers)
        data = loads(await r.text())
        return data
        if r.status != 200:
            raise errors.InvalidTokenError("Invalid token was supplied")
            
    async def get_psn(self, psn: str):
        """
        :param psn: Request chosen Gamertag
        """
        headers = {'Authorization': self.token}
        if not self.token:
            raise errors.InvalidTokenError("No token was supplied")
        r = await request.post("https://gtchecker.com/api/v1/psn?psn={}".format(psn), headers=headers)
        data = loads(await r.text())
        return data
        if r.status != 200:
            raise errors.InvalidTokenError("Invalid token was supplied")


from __future__ import print_function
import requests
from json import loads
from . import errors

class Client:
    """
    API client for gtchecker.com
    """
    def __init__(self, token: str = None, *, baseurl: str = "https://gtchecker.com/api/v1/"):
        self.token = token
        self.baseurl = baseurl
        

    async def get_gamertag(self, gamertag: str):
        """
        :param gamertag: Request chosen Gamertag
        """
        headers = {'Authorization': self.token}
        if not self.token:
            raise errors.InvalidTokenError("No token was supplied")
        r = requests.post(self.baseurl+"xbox?gamertag={}".format(gamertag), headers=headers)
        data = r.json()
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
        r = requests.post(self.baseurl+"psn?psn={}".format(gamertag), headers=headers)
        data = r.json()
        return data
        if r.status != 200:
            raise errors.InvalidTokenError("Invalid token was supplied")


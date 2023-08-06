"""A library that provides a Python interface to Nightscout"""
import hashlib
from typing import Any, Callable, Optional

from aiohttp import ClientSession, ClientTimeout
from .models import SGV, ProfileDefinitionSet, ServerStatus, Treatment


class Api(object):
    """A python interface into Nightscout

    Example usage:
      To create an instance of the nightscout.Api class, with no authentication:
        >>> import nightscout
        >>> api = nightscout.Api('https://yournightscoutsite.herokuapp.com')
      To use authentication, instantiate the nightscout.Api class with your
      api secret:
        >>> api = nightscout.Api('https://yournightscoutsite.herokuapp.com', api_secret='your api secret')
      To fetch recent sensor glucose values (SGVs):
        >>> entries = api.get_sgvs()
        >>> print([entry.sgv for entry in entries])
    """

    def __init__(
        self,
        server_url: str,
        api_secret: Optional[str] = None,
        session: Optional[ClientSession] = None,
        timeout: Optional[ClientTimeout] = None,
    ):
        """Instantiate a new Api object."""
        self.server_url = server_url.strip("/")
        self._api_kwargs = {"headers": self.request_headers(api_secret)}
        if timeout:
            self._api_kwargs["timeout"] = timeout
        self._session = session

    def request_headers(self, api_secret: Optional[str] = None):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if api_secret:
            headers["api-secret"] = hashlib.sha1(api_secret.encode("utf-8")).hexdigest()
        return headers

    async def get_sgvs(self, params={}) -> [SGV]:
        """Fetch sensor glucose values
        Args:
          params:
            Mongodb style query params. For example, you can do things like:
                get_sgvs({'count':0, 'find[dateString][$gte]': '2017-03-07T01:10:26.000Z'})
        Returns:
          A list of SGV objects
        """
        json = await self.__get("/api/v1/entries/sgv.json")

        return [SGV.new_from_json_dict(x) for x in json]

    async def get_server_status(self, params={}) -> ServerStatus:
        """Fetch server status
        Returns:
          The current server status
        """
        json = await self.__get("/api/v1/status.json")

        return ServerStatus.new_from_json_dict(json)

    async def get_treatments(self, params={}) -> [Treatment]:
        """Fetch treatments
        Args:
          params:
            Mongodb style query params. For example, you can do things like:
                get_treatments({'count':0, 'find[timestamp][$gte]': '2017-03-07T01:10:26.000Z'})
        Returns:
          A list of Treatments
        """

        json = await self.__get("/api/v1/treatments.json")

        return [Treatment.new_from_json_dict(x) for x in json]

    async def get_profiles(self, params={}) -> [ProfileDefinitionSet]:
        """Fetch profiles
        Args:
          params:
            Mongodb style query params. For example, you can do things like:
                get_profiles({'count':0, 'find[startDate][$gte]': '2017-03-07T01:10:26.000Z'})
        Returns:
          ProfileDefinitionSet
        """
        json = await self.__get("/api/v1/profile.json")
        return ProfileDefinitionSet.new_from_json_array(json)

    async def __get(self, path):
        async def get(session: ClientSession):
            async with session.get(
                f"{self.server_url}{path}", **self._api_kwargs
            ) as response:
                response.raise_for_status()
                return await response.json()

        return await self.__call(get)

    async def __call(self, handler: Callable[[ClientSession], Any]):
        if not self._session:
            async with ClientSession() as request_session:
                return await handler(request_session)
        else:
            return await handler(self._session)

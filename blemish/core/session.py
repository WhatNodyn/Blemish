# encoding: utf-8
# Blemish, an alternative client to Epitech's repository management tool
# Copyright (C) 2018 Neil Cecchini
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from blemish.core import __version__
from blemish.core.exc import AuthenticationError, ProtocolError
from blemish.core.repository import RepositoryDict
from blemish.core.message import make_message
import asyncio as aio
import aiohttp as http
import json
import typing as tp
import urllib.parse as urllib

INDEX = 'https://blih.epitech.eu/'
AGENT = 'blemish-{}'.format(__version__)

class BaseSession:
    def __init__(self, index: str=INDEX, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers'].setdefault('Content-Type', 'application/json')
        kwargs['headers'].setdefault('User-Agent', AGENT)
        self._client = http.ClientSession(**kwargs)

        self._index = index
        self._login = None
        self._token = None

    async def close(self):
        if not self._client.closed:
            await self._client.close()

    async def authenticate(self, login: str, token: str):
        if self._login is not None:
            raise AuthenticationError('Already authenticated', self._login)

        self._login, self._token = login, token
        try:
            result = await self.request('GET', 'whoami')
            if result.get('message', None) != self._login:
                raise ProtocolError('Authentication failed')
        except ProtocolError:
            self.deauthenticate()
            raise AuthenticationError('Authentication failed') from None

    async def request(self, method: str, url: str, *, raw: bool=False,
                      data: tp.Any=None, **kwargs):
        if self._login is None:
            raise AuthenticationError('Not authenticated')

        url = urllib.urljoin(self._index, url) if not raw else url
        message = make_message(data, self._login, self._token)
        async with self._client.request(method, url, data=message) as response:
            result = await response.json()
            if 'error' in result:
                raise ProtocolError(result['error'] or 'Unknown error')
            return result

    async def get(self, url: str, **kwargs):
        result = await self.request('GET', url, **kwargs)
        return result

    async def post(self, url: str, **kwargs):
        result = await self.request('POST', url, **kwargs)
        return result

    async def put(self, url: str, **kwargs):
        result = await self.request('PUT', url, **kwargs)
        return result

    async def delete(self, url: str, **kwargs):
        result = await self.request('DELETE', url, **kwargs)
        return result

    async def patch(self, url: str, **kwargs):
        result = await self.request('PATCH', url, **kwargs)
        return result

    def deauthenticate(self):
        if self._login is None:
            raise AuthenticationError('Not authenticated')

        self._login, self._token = None, None

    @property
    def login(self):
        return self._login

class Session(BaseSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._repositories = None

    async def authenticate(self, *args, **kwargs):
        await super().authenticate(*args, **kwargs)
        self._repositories = await RepositoryDict.fetch(self)

    @property
    def repositories(self):
        return self._repositories
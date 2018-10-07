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

from blemish.core.exc import ProtocolError, NotFoundError
from collections import UserDict
from aiohttp.client_exceptions import ContentTypeError
import time
import uuid

# NOTE: We ditch the `url` field (deemed useless, since it can be built from `name`)
# NOTE: Deleting a repository does not invalidate related objects
# TODO: Handle ACL
class Repository:
    def __init__(self, session: 'blemish.core.Session', name: str):
        self._name, self._session = name, session

    @classmethod
    async def fetch(cls, session: 'blemish.core.Session', name: str, message=None) -> 'Repository':
        obj = Repository(session, name)
        await obj.refresh(message)
        return obj

    async def refresh(self, message=None):
        if message is None:
            try:
                message = await self._session.get('repository/{}'.format(self.name))
            except ProtocolError:
                raise NotFoundError(repr(self.name)) from None
            message = message.get('message', {})

        self._creation_time = time.gmtime(int(message.get('creation_time', 0)))
        self._uuid = uuid.UUID(message['uuid'])
        self._public = message.get('public', 'False') == 'True'
        self._description = message.get('description', None)
        if self._description == 'None':
            self._description = None

    @classmethod
    async def create(cls, session: 'blemish.core.Session', name: str,
                     kind: str='git', description: str=None) -> 'Repository':
        data = {'name': name, 'type': kind}
        if description is not None:
            data['description'] = description

        await session.post('repositories', data=data)

    async def delete(self):
        await self._session.delete('repository/{}'.format(self._name))

    def __getattr__(self, key: str):
        if not key.startswith('_') and hasattr(self, '_{}'.format(key)):
            return getattr(self, '_{}'.format(key))
        raise AttributeError("'{}' object has no attribute '{}'"
            .format(type(self).__name__, key))

    def __str__(self):
        return '<{}Repository {}>' \
            .format('Public ' if self.public else '', self.name)

class RepositoryDict(UserDict):
    create = Repository.create

    def __init__(self, session: 'blemish.core.Session', *args, **kwargs):
        super().__init__(args)
        self._session = session

    @classmethod
    async def fetch(cls, session: 'blemish.core.Session') -> 'RepositoryDict':
        obj = RepositoryDict(session)
        await obj.refresh()
        return obj

    async def refresh(self):
        message = (await self._session.get('repositories')).get('repositories', {})
        for repository in self:
            if repository not in message:
                del self[repository]

        for repository in message:
            if repository not in self.data:
                self[repository] = await Repository.fetch(self._session, repository, message[repository])

    async def __getitem__(self, key):
        if key in self:
            repo = self.data[key]
            await repo.refresh()
            return repo
        raise KeyError(repr(key))

    def __str__(self):
        return '<RepositoryDict for {}>'.format(self._session.login)
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

from hashlib import sha512
from typing import Any
import hmac
import json

encoder = json.JSONEncoder(sort_keys=True, indent=4, separators=(',', ': '))

def make_token(password: str) -> str:
    return sha512(password.encode('utf-8')).hexdigest()

def make_message(data: Any, user: str, token: str) -> str:
    signature = hmac.new(token.encode('utf-8'), user.encode('utf-8'), sha512)
    if data is not None:
        signature.update(encoder.encode(data).encode('utf-8'))

    message = {'user': user, 'data': data, 'signature': signature.hexdigest()}
    return encoder.encode(message)

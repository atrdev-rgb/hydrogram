#  Hydrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2023-present Hydrogram <https://hydrogram.org>
#
#  This file is part of Hydrogram.
#
#  Hydrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Hydrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Hydrogram.  If not, see <http://www.gnu.org/licenses/>.

import logging

import hydrogram
from hydrogram import raw, types

log = logging.getLogger(__name__)


class GetSessions:
    async def get_sessions(
        self: "hydrogram.Client",
    ) -> list["types.Session"]:
        """Get your info data by other sessions .

        Returns:
            List[:obj:`~hydrogram.types.Session`]: List of active sessions.
        """

        authorizations = await self.invoke(raw.functions.account.GetAuthorizations())
        return [types.Session._parse(auth) for auth in authorizations.authorizations]

#  Hydrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2023 Dan <https://github.com/delivrance>
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

from __future__ import annotations

from typing import TYPE_CHECKING

import hydrogram
from hydrogram import raw, types, utils

if TYPE_CHECKING:
    from datetime import datetime


class RestrictChatMember:
    async def restrict_chat_member(
        self: hydrogram.Client,
        chat_id: int | str,
        user_id: int | str,
        permissions: types.ChatPermissions,
        until_date: datetime = utils.zero_datetime(),
    ) -> types.Chat:
        """Restrict a user in a supergroup.

        You must be an administrator in the supergroup for this to work and must have the appropriate admin rights.
        Pass True for all permissions to lift restrictions from a user.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            permissions (:obj:`~hydrogram.types.ChatPermissions`):
                New user permissions.

            until_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the user will be unbanned.
                If user is banned for more than 366 days or less than 30 seconds from the current time they are
                considered to be banned forever. Defaults to epoch (ban forever).

        Returns:
            :obj:`~hydrogram.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                from datetime import datetime, timedelta
                from hydrogram.types import ChatPermissions

                # Completely restrict chat member (mute) forever
                await app.restrict_chat_member(chat_id, user_id, ChatPermissions())

                # Chat member muted for 24h
                await app.restrict_chat_member(
                    chat_id, user_id, ChatPermissions(), datetime.now() + timedelta(days=1)
                )

                # Chat member can only send text messages
                await app.restrict_chat_member(
                    chat_id, user_id, ChatPermissions(can_send_messages=True)
                )
        """
        r = await self.invoke(
            raw.functions.channels.EditBanned(
                channel=await self.resolve_peer(chat_id),
                participant=await self.resolve_peer(user_id),
                banned_rights=raw.types.ChatBannedRights(
                    until_date=utils.datetime_to_timestamp(until_date),
                    send_messages=not permissions.can_send_messages,
                    send_media=not permissions.can_send_media_messages,
                    send_stickers=not permissions.can_send_other_messages,
                    send_gifs=not permissions.can_send_other_messages,
                    send_games=not permissions.can_send_other_messages,
                    send_inline=not permissions.can_send_other_messages,
                    embed_links=not permissions.can_add_web_page_previews,
                    send_polls=not permissions.can_send_polls,
                    change_info=not permissions.can_change_info,
                    invite_users=not permissions.can_invite_users,
                    pin_messages=not permissions.can_pin_messages,
                    manage_topics=not permissions.can_manage_topics,
                ),
            )
        )

        return types.Chat._parse_chat(self, r.chats[0])

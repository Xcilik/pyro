#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional, List

import pyrogram
from pyrogram import raw, types, utils, enums
from .inline_query_result import InlineQueryResult
from ...file_id import FileId


class InlineQueryResultCachedAudio(InlineQueryResult):
    def __init__(
        self,
        audio_file_id: str,
        title: str,  # ⬅️ Tambahkan title di sini
        id: str = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None
    ):
        super().__init__("audio", id, input_message_content, reply_markup)

        self.audio_file_id = audio_file_id
        self.title = title  # ⬅️ Simpan ke instance
        self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    async def write(self, client: "pyrogram.Client"):
        message, entities = (await utils.parse_text_entities(
            client, self.caption, self.parse_mode, self.caption_entities
        )).values()

        file_id = FileId.decode(self.audio_file_id)

        return raw.types.InputBotInlineResultAudio(
            id=self.id,
            type=self.type,
            title=self.title,  # ⬅️ Injeksi ke raw API
            document=raw.types.InputDocument(
                id=file_id.media_id,
                access_hash=file_id.access_hash,
                file_reference=file_id.file_reference,
            ),
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=await self.reply_markup.write(client) if self.reply_markup else None,
                    message=message,
                    entities=entities
                )
            )
        )

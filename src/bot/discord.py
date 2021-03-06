#!/usr/bin/python3
# vim: ts=4 expandtab

"""The Discord bot"""

from __future__ import annotations

from typing import List

from discord import Client, Message  # type: ignore

from bot.basebot import BaseBot
from bot.commands import Command, MessageContext


class DiscordBot(Client, BaseBot):
    """The Discord bot"""

    def __init__(self: DiscordBot, commands: List[Command]):
        BaseBot.__init__(self, commands)
        Client.__init__(self)

    async def on_ready(self: DiscordBot) -> None:
        """When the bot connects."""
        print(f"{self.user} has connected to Discord!")

    async def on_message(self: DiscordBot, message: Message) -> None:
        """When a message is received."""
        if message.author == self.user:
            return

        await self.process(DiscordMessageContext(message), message.content)


class DiscordMessageContext(MessageContext):
    """Discord message context."""

    _message: Message

    def __init__(self, message: Message):
        self._message = message

    async def reply_direct(self, message: str) -> None:
        """Reply directly to the user who sent this message."""
        await self._message.author.send(message)

    async def reply_all(self, message: str) -> None:
        """Reply to the channel this message was received in"""
        await self._message.channel.send(message)

    async def react(self) -> None:
        """React to the message, indicating successful processing."""
        await self._message.add_reaction("\U0001F44D")

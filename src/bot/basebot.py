#!/usr/bin/python3
# vim: ts=4 expandtab

"""Abstract bot, with command processing."""

from __future__ import annotations

from typing import List

import abc

from bot.commands import Command, MessageContext


class BaseBot(abc.ABC):
    """Abstract bot, with command processing."""

    _commands: List[Command]

    def __init__(self: BaseBot, commands: List[Command]):
        self._commands = commands

    async def process(self: BaseBot, ctx: MessageContext, message: str) -> None:
        """Process an incoming message"""

        for command in self._commands:
            if command.matches(message):
                if await command.process(ctx, message):
                    return

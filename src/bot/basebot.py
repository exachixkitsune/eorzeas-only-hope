#!/usr/bin/python3
# vim: ts=4 expandtab

from __future__ import annotations

from typing import Any, Optional

import abc
import re

from storage import DataStore
from prosegen import ProseGen


class BaseBot(abc.ABC):
    storage: DataStore
    pattern: re.Pattern  # type: ignore
    prose: Optional[ProseGen]

    def __init__(self: BaseBot, storage: DataStore, prose: Optional[ProseGen]):
        super().__init__()

        self.storage = storage
        self.prose = prose
        self.pattern = re.compile(
            " you[^ ]*( are)? [^ ]+zea'?s only hope", re.IGNORECASE
        )

    async def process(self: BaseBot, message: str, ctx: Any) -> None:
        name: str = ""

        if message == "!onlyhope":
            name = self.storage.random()

            await self.reply_all(ctx, "**%s**, you're Eorzea's Only Hope!" % name)
            return

        if message == "!thought":
            if self.prose:
                thought = self.prose.make_statement()
                await self.reply_all(ctx, thought)

            return

        if self.prose and not message.startswith("!"):
            self.prose.add_knowledge(message)

        for line in message.split("\n"):
            if self.pattern.search(line):
                [name, _] = message.split(" you", 1)
            elif message.startswith("!onlyhope"):
                name = message[9:]

            # TODO: remove all punctuation etc?
            name = name.strip()

            if not name:
                return

            print("[%s] Adding %s" % (self.__class__.__name__, name))

            if self.storage.add(name):
                await self.react(ctx)

    @abc.abstractmethod
    async def reply_all(self: BaseBot, ctx: Any, message: str) -> None:
        pass

    @abc.abstractmethod
    async def react(self: BaseBot, ctx: Any) -> None:
        pass

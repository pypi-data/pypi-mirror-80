from __future__ import annotations
__package__ = "aurflux.command"
import typing as ty

if ty.TYPE_CHECKING:
   from . import MessageContext
import aurcore as aur
import typing as ty
import asyncio as aio
import discord
from .. import utils
import datetime


class Response(aur.util.AutoRepr):
   __iter_done = False
   message: ty.Optional[discord.Message]

   def __init__(
         self,
         # ctx: Context,
         content: ty.Optional[str] = None,
         embed: ty.Optional[discord.Embed] = None,
         delete_after: ty.Optional[ty.Union[float, datetime.timedelta]] = None,
         reaction: ty.Optional[ty.Iterable[ty.Union[discord.Emoji, str]]] = None,
         errored: bool = False,
         ping: bool = False,
         post_process: ty.Optional[ty.Callable[[MessageContext, discord.Message], ty.Coroutine]] = None,
         trashable: bool = False
         # reaction: str = ""  # todo: white check mark
   ):
      self.content = content
      self.embed = embed
      self.delete_after: ty.Optional[datetime.timedelta] = delete_after if (isinstance(delete_after, datetime.timedelta) or not delete_after) else datetime.timedelta(seconds=delete_after)
      self.errored = errored
      self.reactions = reaction or (("❌",) if self.errored else ("✅",))
      self.ping = ping
      self.post_process = post_process or (lambda *_: aio.sleep(0))
      self.trashable = trashable

   async def execute(self, ctx: MessageContext):
      if self.content or self.embed:
         content = self.content if self.content else "" + (ctx.author.mention if self.ping else "")
         if len(content) > 1900:
            async with ctx.flux.aiohttp_session.post("https://h.ze.ax/documents", data=content) as resp:
               content = (await resp.json(content_type=None))["key"]
         message = await ctx.channel.send(
            content=content,
            embed=self.embed,
            delete_after=self.delete_after.seconds if self.delete_after else None  # todo: check if seconds,

         )
         self.message = message

         await self.post_process(ctx, message)
      try:
         for reaction in self.reactions:
            await ctx.message.add_reaction(reaction)

         if self.trashable:
            await self.message.add_reaction(utils.EMOJIS["trashcan"])
            try:
               await ctx.flux.router.wait_for(":reaction_add", check=lambda ev: ev.args[0].message.id == self.message.id and ev.args[1] == ctx.message.author, timeout=15)
               await self.message.delete()
            except aio.exceptions.TimeoutError:
               await self.message.remove_reaction(emoji=utils.EMOJIS["trashcan"], member=ctx.guild.me)
      except (discord.errors.NotFound, discord.errors.Forbidden) as e:
         pass
   # def __aiter__(self):
   #     async def gen():
   #         yield self
   #     return gen()

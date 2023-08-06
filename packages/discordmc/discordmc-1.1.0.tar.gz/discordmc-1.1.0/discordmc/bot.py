from discord.ext.commands import command, Cog, Bot
import requests
import threading
import json
from mcserverapi import Parser


def format_mc_msg(player, text):
    return '"§o§1[Discord] §r§l§f<{}> §r§f{}"'.format(player, text)


class DiscordMCParser(Parser):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    def on_ready(self, ctx):
        self.bot.from_minecraft('Server', 'Server is Online!')

    def on_player_message(self, ctx):
        player, message = ctx
        self.bot.from_minecraft(player, message)


class MCBot(Bot):
    def __init__(self, mc_channel_id, mcserver, *args, **kwargs):
        self.target_channel_id = mc_channel_id
        self.target_channel = None
        self.server = mcserver
        self.url = None
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        self.target_channel = self.get_channel(self.target_channel_id)
        webhooks = await self.target_channel.webhooks()
        try:
            self.url = webhooks[0].url
        except IndexError:
            self.url = await self.target_channel.create_webhook(name='MC Server Addons')
            self.url = self.url.url

        print('Discord Pipeline Online as', self.user)

    async def on_disconnect(self):
        self.from_minecraft('Server', 'Server is Offline Now.')
    def from_minecraft(self, player, message):
        message_json = {
            "content": message,
            "username": player
        }
        threading.Thread(target=requests.post, args=[self.url], kwargs={'data': message_json}).start()


class MC(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='mc')
    async def mc(self, ctx, cmd, *params):
        self.bot.server.run_cmd('tellraw', '@a', format_mc_msg(ctx.author.nick, ctx.content))
        self.bot.server.run_cmd(cmd, *params)

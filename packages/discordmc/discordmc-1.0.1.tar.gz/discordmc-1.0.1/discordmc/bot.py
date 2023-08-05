from discord.ext.commands import command, Cog, Bot
import requests
import threading
from mcserverapi import Parser


class DiscordMCParser(Parser):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    def on_ready(self, ctx):
        self.bot.from_minecraft('Server', 'Server is Online!')

    def on_player_message(self, ctx):
        player, message = ctx
        self.bot.from_minecraft(player, message)

import discord
class MCBot(Bot):
    queue = []

    def __init__(self, mc_channel_id, url, server, *args, **kwargs):
        self.target_channel = mc_channel_id
        self.server = server
        self.url = url
        super().__init__(*args, **kwargs)

    async def on_message(self, message):
        if not message.author.bot:
            if not message.content.startswith(self.command_prefix):
                if message.channel.id == self.target_channel:
                    message_content = '§9[Discord] §f§o{} §r> {}'.format(str(message.author).split('#')[0], message.content)
                    self.server.run_cmd('tellraw', '@a', '"' + message_content + '"')
            else:
                await self.process_commands(message)

    async def on_ready(self):
        print('Discord Pipeline Online as', self.user)

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
        self.bot.server.run_cmd('tellraw', '@a', '"§l' + ' '.join([cmd, *params]) + '"')
        self.bot.server.run_cmd(cmd, *params)

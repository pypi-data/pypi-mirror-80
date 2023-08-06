from discordmc.bot import MC, DiscordMCParser, MCBot
from mcserverapi import Server
import threading
import json
import sys


server = Server(sys.argv[-1])

with open('token.json', 'r') as file:
    token, channel_id, *_ = json.load(file).values()


bot = MCBot(
    channel_id,
    server,
    '$'
)

parser = DiscordMCParser(bot, server, debug=True)
threading.Thread(target=parser.watch_for_events).start()

server.start()
bot.add_cog(MC(bot))
bot.run(token)

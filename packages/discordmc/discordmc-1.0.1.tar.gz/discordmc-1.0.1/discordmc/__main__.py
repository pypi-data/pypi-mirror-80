from discordmc.bot import MC, DiscordMCParser, MCBot
from mcserverapi import Server
import threading
import json


server = Server('server.jar')

creds = {
  "token": "NTk3MTgxOTgxNzkyNDAzNDc3.XSEXDw.WlK-x4nReOj2n78BS_2PxJ7Swx8",
  "channel_id": 684408460057641002,
  "url": "https://discordapp.com/api/webhooks/756898639766618173/jbxvExSqUsWxJAbgj1zOWQVz2eQgti9iTARR3_1hRkffwF1bY6YeauEJSGn52g1VEu1n",
  "dev-url": "https://discordapp.com/api/webhooks/756893676969656390/9UGDqN5VOndp5Dvd5HYqEDk4GOMrZjxEGL9h1YVabDGplOmSxLcB-TTgGPP15lgCIJkr"
}
token, channel_id, url, dev_url = creds.values()


bot = MCBot(
    channel_id,
    url,
    server,
    'm!'
)

parser = DiscordMCParser(bot, server, debug=True)
threading.Thread(target=parser.watch_for_events).start()

server.start()
bot.add_cog(MC(bot))
bot.run(token)

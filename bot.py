import discord
import os
import time
import random
from dotenv import load_dotenv

load_dotenv()

random.seed(time.time())

# Common Replies

async def EmojiReact(message):
    emojis = ["🤓","😴","🙄","😡","🖕"]
    # React with a random emoji from the emojis table
    await message.add_reaction(emojis[random.randint(0,len(emojis)-1)])

# Rare Replies

async def NerdMessage(message):
    reply = ""
    i = 0
    for x in message.content:
        # Make every other character uppercase
        reply += x.lower() if i % 2 == 0 else x.upper()
        i += 1
    await message.channel.send('"'+reply+'" - :nerd: :nerd: :nerd:')


commonReplies = [EmojiReact]
rareReplies = [NerdMessage]

class BotClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content},"🙄"')
        # Avoid replying to own messages
        if message.author == self.user:
            return

        # Choose what the reply will be
        common = random.randint(1,10) # change pls (maybe)
        rare = random.randint(1,100)

        if common == 1:
            # Choose random reply from the common replies table
            await commonReplies[random.randint(0,len(commonReplies)-1)](message)

        if rare == 1:
            # Choose random reply from the rare replies table
            await rareReplies[random.randint(0,len(rareReplies)-1)](message)



intents = discord.Intents.default()
intents.message_content = True

client = BotClient(intents=intents)
TOKEN = os.getenv("TOKEN")
client.run(TOKEN)
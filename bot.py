import discord
import os
import time
import random
import requests
import shutil
from nltk.chat.rude import rude_chatbot as rudebot

from PIL import Image
from dotenv import load_dotenv

load_dotenv()

random.seed(time.time())

# Common Replies

async def EmojiReact(message):
    emojis = ["🤓","😴","🙄","😡","🖕"]
    # React with a random emoji from the emojis table
    await message.add_reaction(emojis[random.randint(0,len(emojis)-1)])

# Uncommon Replies

async def RudeMessage(message):
    print("Rude Messange")
    await message.channel.send(rudebot.respond(message.content))

# Rare Replies

async def NerdMessage(message):
    reply = ""
    i = 0
    for x in message.content:
        # Make every other character uppercase
        reply += x.lower() if i % 2 == 0 else x.upper()
        i += 1
    await message.channel.send('"'+reply+'" - :nerd: :nerd: :nerd:')

async def FemboyFurryEdit(message):
        # Download user pfp
        r = requests.get(message.author.avatar.url, stream = True)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open("pfp.png","wb") as f:
                shutil.copyfileobj(r.raw, f)

        background = Image.open("images/furryfemboy.png")
        width, height = background.size
        
        pfp = Image.open("pfp.png")
        pfp.resize((256,256))
        pfpWidth, pfpHeight = pfp.size

        background.paste(pfp, (int(width/2-pfpWidth/2), 0))
        background.save("real.png")

        await message.channel.send(file=discord.File("real.png"))

        os.remove("pfp.png")
        os.remove("real.png")

commonReplies = [EmojiReact]
uncommonReplies = [RudeMessage]
rareReplies = [NerdMessage, FemboyFurryEdit]

class BotClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content},"🙄"')
        # Avoid replying to own messages
        if message.author == self.user:
            return

        # Choose what the reply will be
        common =    random.randint(1,10)
        uncommon =  random.randint(1,50)
        rare =      random.randint(1,100)

        if common == 1:
            # Choose random reply from the common replies table
            await commonReplies[random.randint(0,len(commonReplies)-1)](message)

        if uncommon == 1:
            # Choose random reply from the uncommon replies table
            await uncommonReplies[random.randint(0,len(uncommonReplies)-1)](message)

        if rare == 1:
            # Choose random reply from the rare replies table
            await rareReplies[random.randint(0,len(rareReplies)-1)](message)



intents = discord.Intents.default()
intents.message_content = True

client = BotClient(intents=intents)
TOKEN = os.getenv("TOKEN")
client.run(TOKEN)
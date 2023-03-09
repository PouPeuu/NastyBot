import discord
import os
import time
import random
import requests
import shutil
import textwrap
from nltk.chat.rude import rude_chatbot as rudebot

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from dotenv import load_dotenv

load_dotenv()

random.seed(time.time())

async def getPFP(user):
    # Download user pfp
    r = requests.get(user.avatar.url, stream = True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open("pfp.png","wb") as f:
            shutil.copyfileobj(r.raw, f)

# Common Replies

async def EmojiReact(message):
    emojis = ["🤓","😴","🙄","😡","🖕"]
    # React with a random emoji from the emojis table
    await message.add_reaction(emojis[random.randint(0,len(emojis)-1)])

# Uncommon Replies

async def RudeMessage(message):
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
        await getPFP(message.author)

        background = Image.open("images/furryfemboy.png")
        width, height = background.size
        
        pfp = Image.open("pfp.png")
        pfp = pfp.resize((256,256))
        pfpWidth, pfpHeight = pfp.size

        background.paste(pfp, (int(width/2-pfpWidth/2), 0))
        background.save("real.png")

        await message.channel.send(file=discord.File("real.png"))

        os.remove("pfp.png")
        os.remove("real.png")

async def SpeechBubbleEdit(message):
    await getPFP(message.author)

    background = Image.open("images/speechbubble.png")
    width, height = background.size
    
    pfp = Image.open("pfp.png")
    pfp = pfp.resize((512,512))
    pfpWidth, pfpHeight = pfp.size

    background.paste(pfp, (int(width/2-pfpWidth/2)+50, int(height/2-pfpHeight/2)+50))

    draw = ImageDraw.Draw(background)

    font = ImageFont.truetype("fonts/ggsans-Normal.ttf",50)

    text = ""
    i = 0
    for x in message.content:
        # Make every other character uppercase
        text += x.lower() if i % 2 == 0 else x.upper()
        i += 1

    margin = offset = 0
    for line in textwrap.wrap(text, width=47):
        draw.text((margin,offset), line, font=font, fill=(255,127,127,255))
        offset+= font.getbbox(line)[3]

    background.save("real.png")

    await message.channel.send(file=discord.File("real.png"))

    os.remove("pfp.png")
    os.remove("real.png")

async def HitlerEdit(message):
        await getPFP(message.author)

        background = Image.open("images/adolf-hitler.png")
        width, height = background.size
        
        pfp = Image.open("pfp.png")
        pfp = pfp.resize((256,256))
        pfpWidth, pfpHeight = pfp.size

        background.paste(pfp, (int(width/2-pfpWidth/2)+300, 0))
        background.save("real.png")

        await message.channel.send(file=discord.File("real.png"))

        os.remove("pfp.png")
        os.remove("real.png")

async def TrashEdit(message):
        await getPFP(message.author)

        background = Image.open("images/trash-background.png")
        width, height = background.size
        
        pfp = Image.open("pfp.png").convert("RGBA")
        pfp = pfp.resize((250,250))
        pfpWidth, pfpHeight = pfp.size

        pfp = pfp.rotate(15, expand=True)

        background.paste(pfp, (int(width/2-pfpWidth/2)-25, 0),pfp)
        foreground = Image.open("images/trash-foreground.png")
        background.paste(foreground, (0,0), foreground)
        background.save("real.png")

        await message.channel.send(file=discord.File("real.png"))

        os.remove("pfp.png")
        os.remove("real.png")


commonReplies = [EmojiReact]
uncommonReplies = [RudeMessage,NerdMessage]
rareReplies = [FemboyFurryEdit, SpeechBubbleEdit, HitlerEdit, TrashEdit]

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
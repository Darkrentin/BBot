import discord
from discord.ext import commands
import random as r
import json
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.dm_messages = True   
bot = commands.Bot(command_prefix='!', intents=intents)
prank_active = True

data = {}

with open("data.json", 'r',encoding='utf-8') as f:
    data = json.load(f)

@bot.event
async def on_ready():
    
    print(f'{bot.user} connected')
    print('-------------------------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    global prank_active
    rand = r.randrange(10)
    print(rand)
    if prank_active and message.guild and rand==1:
            try:
                msg = data[str(ctx.author.id)]["werid"][r.randrange(len(data[str(ctx.author.id)]["werid"]))]
                await message.channel.send(f"coucou {msg}")
                await bot.process_commands(message)
            except:
                print("error")


@bot.command()
async def toggle(ctx):
    if ctx.author.id == ADMIN_ID and isinstance(ctx.channel, discord.DMChannel):
        global prank_active
        prank_active = not prank_active
        status = "Enable" if prank_active else "Disable"
        await ctx.send(f'**Toggle {status}**')
        
    elif ctx.author.id == TON_PROPRE_ID:
                await ctx.send('send only in dm')


try:
    bot.run(TOKEN)
except discord.LoginFailure:
    print("ERREUR: Le token du bot est invalide. Vérifie-le !")

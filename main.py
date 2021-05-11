import os
import discord
import json
import requests
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
token = os.getenv("DISCORD_TOKEN")
#fonction pour loader le token
#def load_token():
#    with open("token.txt" , "r") as f:
#        lines = f.readlines()
#       return lines[0].strip()

@bot.event
async def on_ready():
    channel = bot.get_channel(840631684961796146)
    await channel.send('ScryFallBot Radis')

@bot.command()
async def carte(ctx, *cardname):
    nom_carte = '+'.join(cardname)
    apiurl = f'https://api.scryfall.com/cards/named?fuzzy={nom_carte}'
    data =  requests.get(apiurl).json()
    if 'code' in data:
        details = data['details']
        await ctx.send(f'Une erreur s\'est produite :{details}')
    else:
        name = data['name']
        mana_cost = data['mana_cost']
        url = data['scryfall_uri']
        oracle_text = data['oracle_text']
        image = data['image_uris']['normal']

        embed = discord.Embed(title = name, url= url, description = mana_cost)
        embed.add_field(name= "Texte Oracle", value= oracle_text)
        embed.set_thumbnail(url=image)

        await ctx.send (embed=embed)

#token = load_token()
if __name__ == "__main__":
    bot.run(token)

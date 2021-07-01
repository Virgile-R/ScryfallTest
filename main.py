import os
import discord
import json
import requests
from bs4 import BeautifulSoup
import urllib.request
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
token = os.getenv("DISCORD_TOKEN")
channel_id = os.getenv("CHANNEL_ID")
#fonction pour loader le token
#def load_token():
#    with open("token.txt" , "r") as f:
#        lines = f.readlines()
#        return lines[0].strip()

@bot.event
async def on_ready():
    channel = bot.get_channel(channel_id)
    # await channel.send('ScryFallBot Radis')

@bot.command()
async def carte(ctx, *cardname):
    nom_carte = '+'.join(cardname)
    apiurl = f'https://api.scryfall.com/cards/named?fuzzy={nom_carte}'
    data =  requests.get(apiurl).json()
    if 'code' in data:
        details = data['details']
        await ctx.send(f'Une erreur s\'est produite :{details}')
    
    if 'card_faces' in data:
        name = data['name']             
        mana_cost = data['card_faces'][0]['mana_cost']
        url = data['scryfall_uri']
        oracle_text = data['card_faces'][0]['oracle_text'] + " \n // \n" + data['card_faces'][1]['oracle_text'] 
        image = data['card_faces'][0]['image_uris']['normal']  
    else:
        name = data['name']             
        mana_cost = data['mana_cost']
        url = data['scryfall_uri']
        oracle_text = data['oracle_text']
        image = data['image_uris']['normal']

    embed = discord.Embed(title = name, url= url, description = mana_cost)
    if oracle_text:
        embed.add_field(name= "Texte Oracle", value= oracle_text)
    embed.set_thumbnail(url=image)

    await ctx.send (embed=embed)

@bot.command()
async def meta(ctx, *format):
    nomformat = '+'.join(format)
    url = f'https://www.mtggoldfish.com/metagame/{nomformat}#paper'

    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    deckcard = soup.find('div', attrs={'class': 'archetype-tile-container'})
    decks = deckcard.find_all('span', attrs={'class':'deck-price-paper'})


    results = {}
    for deck in decks:
        nom = deck.get_text().strip('\n')
        deckurl = 'https://www.mtggoldfish.com' + deck.find('a').get('href')
        results[nom] = deckurl
   
    json.dumps(results)

    meta = json.load(results)
    meta_embed = discord.Embed.from_dict(meta)
    embed = discord.Embed()
    embed.description = f'La meta du {format} selon [MTGGoldfish]({url}:{meta_embed}' 
    await ctx.send (embed=embed)

#token = load_token()
if __name__ == "__main__":
    bot.run(token)

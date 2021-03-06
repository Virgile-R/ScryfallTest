import os
import subprocess
import sys
import discord
import json
import time
from discord.message import Message
import requests
from bs4 import BeautifulSoup
import urllib.request
from discord.ext import commands
from discord import Client
import random
import numpy as np
from dnd import generate_monster_block, Monster
from dotenv import load_dotenv
load_dotenv()
bot = commands.Bot(command_prefix="!")

intents = discord.Intents.default()
intents.members = True
client = Client(intents=intents)
token = os.getenv("DISCORD_TOKEN")
channel_id = os.getenv("CHANNEL_ID")


def get_commander_dataset():
    commander = list()
    apiurl = 'https://api.scryfall.com/cards/search?q=is%3Acommander+legal%3Acommander'
    while apiurl:
        # la request
        datacommander = requests.get(apiurl).json()
        #  les datas
        commanderprov = [(card['name'], card['related_uris']['edhrec'])
                         for card in datacommander["data"]]
        commander = commander + commanderprov
        if datacommander["has_more"]:
            apiurl = datacommander["next_page"]
        else:
            apiurl = None
    return commander


class random_commander_generator():
    def __init__(self):
        self.database = get_commander_dataset()

    def generate_excluding_commander(self, n_players):
        random.shuffle(self.database)
        return self.database[:n_players]


def random_commander():
    apiurl = 'https://api.scryfall.com/cards/search?q=is%3Acommander+legal%3Acommander'

    result = dict()
    # commanderprov = dict()
    commander = list()
    while apiurl:
        # la request
        datacommander = requests.get(apiurl).json()
        #  les datas
        commanderprov = [(card['name'], card['related_uris']['edhrec'])
                         for card in datacommander["data"]]
        commander = commander + commanderprov
        if datacommander["has_more"]:
            apiurl = datacommander["next_page"]
        else:
            apiurl = None

    # print(len(commander))
    random_index = random.randint(0, len(commander)-1)
    cmdname = commander[random_index]
    cmdurl = commander[random_index]['related_uris']['edhrec']
    result[cmdname] = cmdurl
    return result


def arrange_dataset_per_rarity(cards_list):
    # rarity = ['common', 'uncommon', 'rare', 'mythic']
    rarity_dict = {'common': [], 'uncommon': [], 'rare': [], 'mythic': []}
    for card in cards_list:
        card_type = card['type_line']
        if card_type.find("Basic Land") == -1:
            rarity_dict[card['rarity']].append(card)
    return rarity_dict


class random_sealed_booster_generator():
    def __init__(self, set):
        apiurl = 'https://api.scryfall.com/sets/' + set
        result = list()
        dataset_info = requests.get(apiurl).json()
        apiurl = dataset_info['search_uri']
        dataset_card = requests.get(apiurl).json()
        cards = dataset_card['data']
        while bool(dataset_card['has_more']):
            apiurl = dataset_card['next_page']
            dataset_card = requests.get(apiurl).json()
            cards += dataset_card['data']
        self.dictionary = arrange_dataset_per_rarity(cards_list=cards)
        self.n_common = len(self.dictionary['common'])
        self.n_uncommon = len(self.dictionary['uncommon'])
        self.n_rare = len(self.dictionary['rare'])
        self.n_mythic = len(self.dictionary['mythic'])
        self.probability = 0.9

    def get_a_booster(self):
        booster = list()

        random.shuffle(self.dictionary['common'])
        random.shuffle(self.dictionary['uncommon'])
        random.shuffle(self.dictionary['rare'])
        random.shuffle(self.dictionary['mythic'])
        coin = np.random.binomial(2, self.probability)

        booster = booster + self.dictionary['common'][:10]
        booster = booster + self.dictionary['uncommon'][:3]
        if coin == 1:
            booster = booster + self.dictionary['mythic'][:1]
        else:
            booster = booster + self.dictionary['rare'][:1]
        return booster


@bot.command()
async def dndmonster(ctx, *nom_monstre):
    monster_name = '-'.join(nom_monstre).lower()
    try:
        m = Monster(monster_name)
        output = generate_monster_block(m)

        embed = discord.Embed(title=m.name)
        file = discord.File(output, filename="image.png")
        embed.set_image(url=f"attachment://image.png")
        await ctx.send(file=file, embed=embed)
    except ValueError:
        await ctx.send("Pas de monstre avec ce nom dans le SRD!")


@bot.command()
async def carte(ctx, *cardname):
    nom_carte = '+'.join(cardname)

    apiurl = f'https://api.scryfall.com/cards/named?fuzzy={nom_carte}'
    data = requests.get(apiurl).json()
    if 'code' in data:
        details = data['details']
        await ctx.send(f'Une erreur s\'est produite :{details}')

    if 'card_faces' in data:
        name = data['name']
        mana_cost = data['card_faces'][0]['mana_cost']
        url = data['scryfall_uri']
        oracle_text = data['card_faces'][0]['oracle_text'] + \
            " \n // \n" + data['card_faces'][1]['oracle_text']
        image = data['card_faces'][0]['image_uris']['normal']
    else:
        name = data['name']
        mana_cost = data['mana_cost']
        url = data['scryfall_uri']
        oracle_text = data['oracle_text']
        image = data['image_uris']['normal']

    embed = discord.Embed(title=name, url=url, description=mana_cost)
    if oracle_text:
        embed.add_field(name="Texte Oracle", value=oracle_text)
    embed.set_thumbnail(url=image)

    await ctx.send(embed=embed)


@bot.command()
async def meta(ctx, *format):
    nomformat = '+'.join(format).lower()
    url = f'https://www.mtggoldfish.com/metagame/{nomformat}#paper'

    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    deckcard = soup.find('div', attrs={'class': 'archetype-tile-container'})
    decks = deckcard.find_all('span', attrs={'class': 'deck-price-paper'})

    results = {}
    for deck in decks:
        nom = deck.get_text().strip('\n')
        deckurl = 'https://www.mtggoldfish.com' + deck.find('a').get('href')
        results[nom] = deckurl

    nomformat = '+'.join(format).capitalize()
    embed = discord.Embed(
        title=f'La meta du {nomformat} selon MTGGoldfish', url=url)
    for key, value in results.items():
        embed.add_field(name=key, value=f'[decklist]({value})')
    await ctx.send(embed=embed)


@bot.command()
async def chaoscommander(ctx, *args):
    COMMANDER_GEN = None
    embed = discord.Embed(title='CHAOS REIGNS')
    if COMMANDER_GEN is None:
        COMMANDER_GEN = random_commander_generator()
    if not args:
        args_commander = COMMANDER_GEN.generate_excluding_commander(1)
        for key, arg in args_commander:
            embed.add_field(name='Commander au hasard',
                            value=f'[{key}]({arg})')
        await ctx.send(embed=embed)
    else:
        args_commander = COMMANDER_GEN.generate_excluding_commander(len(args))
        for k, tpl in enumerate(args):
            joueur = args[k]
            key, arg = args_commander[k]
            embed.add_field(name=joueur,
                            value=f'[{key}]({arg})')
        await ctx.send(embed=embed)
        await ctx.send("https://giphy.com/gifs/skdJmptBR4iic")


@bot.command()
async def sealed(ctx, *args):
    BOOSTER_GEN = None
    embed = discord.Embed(title='SEALED')
    await ctx.send(embed=embed)
    if not args:
        str_ = 'Il manque les noms des joueurs! Sale ragondin!'
        embed.add_field(name="Message d'insulte:", value=f'insulte({str_})')
        await ctx.send(embed=embed)
    else:
        if BOOSTER_GEN is None:
            BOOSTER_GEN = random_sealed_booster_generator('afr')
        for player_name in args:
            boosters = []
            for k in range(6):
                boosters = boosters + BOOSTER_GEN.get_a_booster()
            cards = [cards['name'] for cards in boosters]
            player_card_file = player_name + "cards.txt"
            with open(player_card_file, "wt") as file:
                for card in cards:
                    file.write(card + '\n')
            with open(player_card_file, "rb") as file:
                await ctx.send(player_name + "! Your file is:", file=discord.File(file, player_card_file))

        await ctx.send("https://media.giphy.com/media/oS8pRFxbD0d44/giphy.gif")


# TODO: Slash command et ping les users. Compteur de voix automatique et Dur??e du sondage
@bot.command()
async def calendrier(ctx):

    botUser = bot.user
    author = ctx.author

    guild = ctx.guild

    originChannel = ctx.channel
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        author: discord.PermissionOverwrite(read_messages=True),
        botUser: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_text_channel(f'Nouvelle s??ance pour {originChannel}', overwrites=overwrites)
    await channel.send('Premi??re ??tape: toi seul peut voir ce channel. Pour commencer donne moi entre deux et cinq dates, s??par??es par des virgules. tu peux aussi sp??cifier des utilisateurs que je pingerai.')

    def checkDate(msg):
        return msg.author == author and len(msg.content.split()) > 1 and len(msg.content.split()) <= 5

    msg = await bot.wait_for('message', check=checkDate)

    msgFormat = msg.content.split(',')
    await channel.send(f'Voici les dates que tu as choisi: {", ".join(msgFormat)}. Si tu veux ajouter des utilisateurs ?? mentionner pour le sondage, r??agis ?? ce message avec un ???. Si tu as fini, r??agis avec un ???')

    def checkReaction(reaction, msg):
        return msg == author and str(reaction) in ["???", "???"]

    reaction = await bot.wait_for('reaction_add', check=checkReaction)
    finalMessage = ""

    # Fonction pour changer un int vers un emoji
    def emojyzeNumber(x):
        match x:
            case 1:
                return "1??????"
            case 2:
                return "2??????"
            case 3:
                return "3??????"
            case 4:
                return "4??????"
            case 5:
                return "5??????"

    dateListWithIndex = [(emojyzeNumber(i+1), msgFormat[i])
                         for i in range(len(msgFormat))]
    dateListWithIndexAndEmojis = "\n".join(
        "%s: %s" % tup for tup in dateListWithIndex)
    if str(reaction[0].emoji) == "???":

        finalMessage = f'Voici les dates propos??es pour les prochaines parties: \n{dateListWithIndexAndEmojis}\nVotez en utilisant les emojis num??riques!'
        await channel.send(f'Ok, je vais envoyer le sondage suivant sur le channel {originChannel.name}:\n```{finalMessage}```\nSi cela te convient, confirme avec un emoji ??? pour envoyer le message. Sinon tu peux annuler la cr??ation en r??agissant avec un ???')

        finalReaction = await bot.wait_for('reaction_add', check=checkReaction)
        if str(finalReaction[0].emoji) == "???":
            await originChannel.send(f'```{finalMessage}```')
            await channel.send('Ce channel va maintenant s\'autod??truire. A plus.')
            time.sleep(15)
            await channel.delete()
        else:
            await channel.send('Op??ration annul??e. Tu peux recommencer en tapant !calendrier dans le channel que tu veux. Ce channel va maintenant s\'autod??truire. A plus.')
            time.sleep(15)
            await channel.delete()
    elif str(reaction[0]) == "???":
        await channel.send('donne moi les pseudos des gens que tu veux pinger!')
        nameList = await bot.wait_for('message')
        nameListFormat = nameList.content.split()

        # il faudrait un component selector mais je ne le trouve pas dans la doc de Discord Py...
        finalMessage = f'Hey {", ".join("@%s" % name for name in nameListFormat)}, Voici les dates propos??es pour les prochaines parties: \n{dateListWithIndexAndEmojis}\nVotez en utilisant les emojis num??riques!'
        await channel.send(f'Ok, je vais envoyer le sondage suivant sur le channel {originChannel.name}:\n```{finalMessage}```\nSi cela te convient, confirme avec un emoji ??? pour envoyer le message. Sinon tu peux annuler la cr??ation en r??agissant avec un ???')

        finalReaction = await bot.wait_for('reaction_add', check=checkReaction)
        if str(finalReaction[0].emoji) == "???":
            await originChannel.send(f'```{finalMessage}```')
            await channel.send('Ce channel va maintenant s\'autod??truire. A plus.')
            time.sleep(15)
            await channel.delete()
        else:
            await channel.send('Op??ration annul??e. Tu peux recommencer en tapant !calendrier dans le channel que tu veux. Ce channel va maintenant s\'autod??truire. A plus.')
            time.sleep(15)
            await channel.delete()

if __name__ == "__main__":
    bot.run(token)

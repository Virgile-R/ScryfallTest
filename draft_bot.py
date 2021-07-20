import os
from asyncio.tasks import sleep
import discord
import json
from discord import player
from discord.embeds import Embed
import requests
from bs4 import BeautifulSoup
import urllib.request
from discord.ext import commands
from discord import Client
import random
import numpy as np
import time
def arrange_dataset_per_rarity( cards_list ):
    # rarity = ['common', 'uncommon', 'rare', 'mythic']
    rarity_dict = {'common':[], 'uncommon':[], 'rare':[], 'mythic':[]}
    for card in cards_list:
        card_type = card['type_line'] 
        if  card_type.find("Basic Land") == -1:
            rarity_dict[card['rarity']].append(card)
    return rarity_dict


class random_sealed_booster_generator(  ):
    def __init__(self,set):
        apiurl = 'https://api.scryfall.com/sets/' + set
        result = list()
        dataset_info = requests.get(apiurl).json()
        apiurl = dataset_info['search_uri']
        dataset_card = requests.get(apiurl).json()
        cards = dataset_card['data']
        while bool( dataset_card['has_more'] ):
            apiurl = dataset_card['next_page']
            dataset_card = requests.get(apiurl).json()
            cards += dataset_card['data']
        self.dictionary = arrange_dataset_per_rarity(cards_list= cards)
        self.n_common = len( self.dictionary['common'])
        self.n_uncommon = len( self.dictionary['uncommon'])
        self.n_rare = len( self.dictionary['rare'])
        self.n_mythic = len( self.dictionary['mythic'])
        self.probability = 0.9
    
    def get_a_booster(self):
        booster = list()

        random.shuffle( self.dictionary['common']) 
        random.shuffle( self.dictionary['uncommon']) 
        random.shuffle( self.dictionary['rare']) 
        random.shuffle( self.dictionary['mythic']) 
        coin = np.random.binomial(2,self.probability)
        
        booster = booster + self.dictionary['common'][:10] 
        booster = booster +  self.dictionary['uncommon'] [:3]
        if coin == 1:
            booster = booster + self.dictionary['mythic'][:1]
        else :
            booster = booster +  self.dictionary['rare'] [:1]
        return booster


class draft_bot(commands.bot.Bot):
    def initialize_game(self,set):
        self.players = dict()
        self.players_next = dict()
        self.booster_gen = random_sealed_booster_generator(set)
        self.registration_open = False
        self.circulation = 'left' 
        self.available_boosters = dict()
        self.card_lists = dict()
    def prepare_possibilities(self, booster , embed  = None ):
        if embed is None:
            embed = discord.Embed(
            title = "Received Booster",
            description = "Booster are comming from the " + self.circulation
            )
        for k,card_tuple in enumerate( booster ):
            
            key,arg =card_tuple['name'], card_tuple['image_uris']['normal']
            embed.add_field(name= str(k) ,
                value= f'[{key}]({arg})') 
        return embed
    def player_draft_state_message(self,player):
        embed = discord.Embed(
        title = "Picking State ",
        description = "Booster are comming from the " + self.circulation + "!" +
        " You have " + str( len( self.available_boosters[player.name] ) ) + " booster(s) waiting your choice!" + 
        " you already picked " + str( len(self.card_lists[player.name] ) ) + " cards!"
        )
        if len( self.available_boosters[player.name]  ):
            self.prepare_possibilities( self.available_boosters[player.name] [0] , embed=embed )
        return embed

    def player_draft_order_message(self,player):
        curent_player_name = player.name
        token = " >> " if self.circulation == 'left' else " << "
        order  = curent_player_name + token
        for k in range ( len( self.players) - 1 ):
            curent_player_name = self.players_next[curent_player_name]
            order = order + curent_player_name + token

        embed = discord.Embed(
        title = "Draft Order for this round! ",
        description = order
        )
        return embed
    def check_internal_state(self):
        for key,booster_list in self.available_boosters.items():
            if len(booster_list):
                return False
        return True



bot = draft_bot(command_prefix="!")
token = os.getenv("DISCORD_TOKEN")
channel_id = os.getenv("CHANNEL_ID")

@bot.command()
async def help_play(ctx):
    comm_player = ctx.author
    embed = discord.Embed(
    title = "Draft Bot is here to help you! ",
    description = 'This is a message from your favorite bot'
    )
    embed.add_field(name= 'launch_draft'  ,
        value= 'initialise a new draft game!') 
    embed.add_field(name= 'register_to_draft'  ,
        value= 'register to the unique existing draft game!') 
    embed.add_field(name= 'unregister_to_draft'  ,
        value= 'quit to the unique existing draft game!') 
    embed.add_field(name= 'close_registration'  ,
        value= 'disable possibility of registration to the game!') 
    embed.add_field(name= 'launch_game'  ,
        value= 'disable possibility of registration to the game and launch the game!') 
    embed.add_field(name= 'pick'  ,
        value= 'send choice for the current choice you have to do! arg: the index of the card you picked') 
    await comm_player.send( embed=embed )

@bot.command()
async def launch_draft(ctx, *args):
    bot.initialize_game(args[0])
    bot.players[ctx.author.name] = ctx.author
    bot.registreation_open = True

@bot.command()
async def register(ctx, *args):
    bot.players[ctx.author.name] = ctx.author
    print( bot.players.keys() )

@bot.command()
async def unregister(ctx, *args):
    if bot.registration_open:
        del bot.player[ctx.author.name] 



@bot.command()
async def close_registration(ctx, *args):
    comm_player = ctx.author
    print( bot.players.keys() )
    if not comm_player.name in bot.players.keys():
        return
    else:
        bot.registration_open = False
    
    # players_next = list( bot.players.keys() )
    # random.shuffle( players_next )
    # for k,player_name in enumerate( bot.players.keys() ):
    #     bot.players_next[player_name] = players_next[k]

@bot.command()
async def draft(ctx, *args):
    comm_player = ctx.author
    if not comm_player.name in bot.players.keys() or not bot.check_internal_state():
        return
    else:
        list_of_players = bot.players.keys()
        random.shuffle( list_of_players )
        for k,player_name in enumerate( list_of_players ):
            bot.players_next[player_name] = list_of_players [ (k +1) % len( list_of_players )]
        for name,player in bot.players.items():
            booster = bot.booster_gen.get_a_booster()
            message = bot.prepare_possibilities( booster )
            bot.available_boosters[player.name] = [ booster ]
            bot.card_lists[player.name] = [  ]
            await player.send (  embed=message )
            end_of_turn = False
@bot.command()
async def pick(ctx, *args):
    comm_player = ctx.author
    if not comm_player.name in bot.players.keys():
        return
    else:
        if len( bot.available_boosters[comm_player.name] ) :
            booster = bot.available_boosters[comm_player.name][0]
            card_index = int(args[0])
            if card_index <0 or card_index > len(booster):
                comm_player.send(embed = 'invalid card index! try again you fool!')
                return
            bot.available_boosters[comm_player.name] = bot.available_boosters[comm_player.name][1:]
            picked_card =  booster.pop( card_index )
            bot.card_lists[comm_player.name].append( picked_card )
            random.shuffle(  booster )
            if len(booster):
                next_player_name = bot.players_next[comm_player.name]
                bot.available_boosters[next_player_name].append(booster)
                if len( bot.available_boosters[next_player_name ] ) == 1:
                    message_to_the_next_player = bot.prepare_possibilities( bot.available_boosters[next_player_name ][0] )
                    await bot.players[next_player_name].send( embed = message_to_the_next_player)

            message_to_the_picker = bot.player_draft_state_message( comm_player )
            await comm_player.send( embed=message_to_the_picker )

@bot.command()
async def update_player(ctx, *args):
    comm_player = ctx.author
    if not comm_player.name in bot.players.keys():
        return
    else:
        comm_player = ctx.author
        embed = bot.get_player_status(comm_player.name)
        await comm_player.send( embed=embed )


@bot.command()
async def get_picked_cards(ctx):
    comm_player = ctx.author
    if not comm_player.name in bot.players.keys():
        return
    else:
        player_card_file = comm_player.name + "cards.txt"
        with open(player_card_file, "wt") as file:
                for card in bot.card_lists[comm_player.name]: 
                    file.write(card['name'] + '\n')
        with open(player_card_file, "rb") as file:
            await comm_player.send(comm_player.name + "! Your file is:", file=discord.File(file,player_card_file))


if __name__ == "__main__":
    bot.run(token)
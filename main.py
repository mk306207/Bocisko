import discord
import requests
import json
import http.client
from klucze import *
from discord.ext import commands
from discord import FFmpegPCMAudio
import pandas as pd
from pandas import json_normalize
import requests
import time
import asyncio
from player import Player

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix = '$', intents=intents)

endpoints = ["/teams","/players","/fixtures","/leagues","/seasons","/standings"]

def get_teams():
    endpoint = f"{Base_URL}/teams"
    params = {
        "api_token": API_token,
    }
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        return response.json()  # Zwracamy dane w formacie JSON
    else:
        return {"error": response.text}

def print_all_players():
    endpoint = f"{Base_URL}/players"
    params = {
        "api_token": API_token,
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Błąd: {response.status_code}")
    
def print_all():
    for e in endpoints:
            endpoint = f"{Base_URL}"+e
            params = {
                "api_token": API_token,
            }
            response = requests.get(endpoint, params=params)
            if response.status_code == 200:
                data = response.json()
                print(data)
            else:
                print(f"Błąd: {response.status_code}")  
                             
async def take_endpoint(endpoint_ptr,ctx):
    temp_endpoint = endpoints[endpoint_ptr - 1]
    endpoint = f"{Base_URL}"+temp_endpoint
    params = {
        "api_token": API_token,
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        await decide(temp_endpoint,data,ctx)
    else:
        print(f"Błąd: {response.status_code}")
                
async def decide(endpoint,data,ctx):

    if endpoint == "/teams":
        if "error" in data:
            #await ctx.send(f"Błąd podczas pobierania danych: {data['error']}")
            return 3

        teams_list = []
        for team in data['data']:
            team_name = team['name']
            teams_list.append(f"{team_name}")
            
        i = 1
        
        for t in teams_list:
            await ctx.send(t)
            i+=1
        
    elif endpoint == "/players":
        if "error" in data:
            #await ctx.send(f"Błąd podczas pobierania danych: {data['error']}")
            return 3
        players_list = []
        for player in data['data']:
            player_id = player['id']
            player_name = player['name']
            temp = Player(player_id,player_name)
            players_list.append(temp)
            
        print("All players have been loaded...")
        
        for p in players_list:
            await ctx.send(p.showPlayer())
            
        print("players data")
    elif endpoint == "/fixtures":
        print("players data")
    elif endpoint == "/leagues":
        print("players data")
    elif endpoint == "/seasons":
        print("players data")
    elif endpoint == "/standings":
        print("players data")

@client.event
async def on_ready():
    channel = client.get_channel(kanal)
    await channel.send("Hello :)")
    print("Ready")
    print("------------------")
    
@client.event
async def on_member_join(member):
    channel = client.get_channel(kanal_powitalny)
    await channel.send("Hello "+ member)
    
@client.event
async def on_member_remove(member):
    channel = client.get_channel(kanal_powitalny)
    await channel.send("Goodbye :(")
    
@client.command()
async def hello(ctx):
    await ctx.send("Hi!")
 
@client.command()
async def shutdown(ctx):
    await ctx.send("Bye")
    await client.close()
    
@client.command()
async def test(ctx):
    channel = client.get_channel(kanal_powitalny)
    await channel.send("aha")
    
@client.command(pass_context = True)
async def join(ctx):
    if(ctx.author.voice):
        channel=ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('XD.mp3')
        player = voice.play(source)
    else:
        await ctx.send("Nie ma cie na kanale głosowym")

@client.command(pass_context = True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Wyszedlem")
    else:
        await ctx.send("Nie jestem na kanale")

@client.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()
    
@client.command(pass_context = True)
async def today_matches(ctx):
    await ctx.send(ctx)

@client.command(pass_context = True)
async def teams(ctx):
    #await ctx.send(ctx)
    data = get_teams()

    if "error" in data:
        await ctx.send(f"Błąd podczas pobierania danych: {data['error']}")
        return

    teams_list = []
    for team in data['data']:
        team_name = team['name']
        teams_list.append(f"{team_name}")
        
    i = 1
    
    for t in teams_list:
        await ctx.send(t)
        i+=1
    print("Finished")
    #print(data)

@client.command(pass_context = True)
async def dataTest(ctx):#debugging func
    print_all()
    
@client.command(pass_context = True)
async def data_pass(ctx):
    i = 1
    for e in endpoints:
        await ctx.send(str(i)+". "+e)
        i+=1
    await ctx.send("Choose what you want to display:")
    print("For loop has ended...")
    def check_endpoint_message(msg):   
        print(f"Checking message content... \n {msg.content}")
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content in ['1','2','3','4','5','6']
    
    try:
        msg = await client.wait_for('message',check = check_endpoint_message, timeout=5000.0)
        if msg.content == '1':
            await take_endpoint(1,ctx)
            print(endpoints[0])
        elif msg.content == '2':
            await take_endpoint(2,ctx)
            print(endpoints[1])
        elif msg.content == '3':
            await take_endpoint(3,ctx)
            print(endpoints[2])
        elif msg.content == '4':
            await take_endpoint(4,ctx)
            print(endpoints[3])
        elif msg.content == '5':
            await take_endpoint(5,ctx)
            print(endpoints[4])
        elif msg.content == '6':
            await take_endpoint(6,ctx)
            print(endpoints[5])
        else:
            await ctx.send("Wrong input data!!!")
    except:
        await ctx.send("TIMEOUT!!!!")

    

client.run(Klucz_bota)

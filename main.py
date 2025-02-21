import discord
import requests
import json
from klucze import *
from discord.ext import commands
from discord import FFmpegPCMAudio
import pandas as pd
from pandas import json_normalize
import requests

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

    #print(data)

@client.command(pass_context = True)
async def dataTest(ctx):#debugging func
    print_all()

client.run(Klucz_bota)

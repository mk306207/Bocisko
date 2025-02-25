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
from match import Match
from season import Season
from standing import Standing
import scraper
from team import Team

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix = '$', intents=intents)

endpoints = ["/teams","/players","/fixtures","/leagues","/seasons","/standings"]

def get_teams():
    endpoint = f"{Base_URL}/standings"
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
            return 3

        teams_list = []
        for team in data['data']:
            team_name = team['name']
            teams_list.append(f"{team_name}")
            
        i = 1
        
        for t in teams_list:
            await ctx.send(t)
            i+=1
        
        print("teams data")
    elif endpoint == "/players":
        if "error" in data:
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
        if "error" in data:
            return 3
        
        matches_list = []
        for match in data['data']:
            match_id = match['id']
            match_teams = match['name']
            match_score = match['result_info']
            temp = Match(match_id,match_teams,match_score)
            matches_list.append(temp) 
        
        print("All matches have been loaded...")
        for m in matches_list:
            await ctx.send(m.showMatch()) 
        
        print("matches data")
    
    elif endpoint == "/leagues":
        if "error" in data:
            return 3
        
        leagues_list = []
        for league in data['data']:
            league_name = league['name']
            leagues_list.append(league_name) 
        
        print("All leagues have been loaded...")
        for l in leagues_list:
            await ctx.send(l) 
        
        print("leagues data")
    
    elif endpoint == "/seasons":
        if "error" in data:
            return 3
        
        print("Method initializes...")
        
        seasons_list = []
        for season in data['data']:
            season_id = season['id']
            season_name = season['name']
            season_state = season['is_current']
            
            temp = Season(season_id,season_name,season_state)
            seasons_list.append(temp)
        
        
        print("All seasons have been loaded...")
        for s in seasons_list:
            await ctx.send(s.showSeason())
        
        print("seasons data")
        
    elif endpoint == "/standings":
        if "error" in data:
            return 3
        standings_list = []
        for standing in data['data']:
            standing_id = standing['id']
            standing_pId = standing['participant_id']
            standing_position = standing['position']
            temp = Standing(standing_id,standing_pId,standing_position)
            standings_list.append(temp)
        for s in standings_list:
            await ctx.send(s.show())
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
    r = get_teams()
    print(r)
    
@client.command(pass_context = True)
async def data_pass(ctx):
    i = 1
    for e in endpoints:
        if i==3:
            await ctx.send("3. /matches")
            i+=1
        else:
            await ctx.send(str(i)+". "+e)
            i+=1
    await ctx.send("Choose what you want to display:")
    print("For loop has ended...")
    def check_endpoint_message(msg):   
        print(f"Checking message content... \n {msg.content}")
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content in ['1','2','3','4','5','6']
    
    try:
        msg = await client.wait_for('message',check = check_endpoint_message, timeout=10000.0)
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
            await ctx.send("Merging data, it's gonna take a while...\nIf the team name isn't in the API only id will show up")
            await take_endpoint(6,ctx)
            print(endpoints[5])
        else:
            await ctx.send("Wrong input data!!!")
    except:
        await ctx.send("TIMEOUT!!!!")

@client.command(pass_context = True)
async def PLTable(ctx):
    data = scraper.PLData()
    table = []
    data2 = data['standings']
    if isinstance(data2, list):
        for standing in data2:
            if 'rows' in standing:
                for row in standing['rows']:
                    team_name = row['team']['name']
                    team_position = row['position']
                    team_wins = row['wins']
                    team_draws = row['draws']
                    team_loses = row['losses']
                    team_points = row['points']
                    temp = Team(team_name,team_position,team_wins,team_draws,team_loses,team_points)
                    table.append(temp)
            else:
                print("BAD ENDPOINTS")
    else:
        print("ERROR")
    
    for t in table:
        await ctx.send(t.show())

client.run(Klucz_bota)

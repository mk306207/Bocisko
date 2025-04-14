# BOCISKO - discord bot for football data + bonuses

## Important before you start:
There is additional file that isn't in this repository, it is called klucze.py and it contains various private data, that you must fill out yourself according to this guide:  
🔵 **Klucz_bota** - it contains your discord bot key, that is neccessary for it to connect to discord  
🟢 **kanal & kanal_powitalny** - these two contains channels id, which determines where you want to perform specific actions (kanal_powitalny = channel, where bot greets people | kanal = deafult channel)  
🟡 **API_token** - your private api token from sportmonks.com, in this project i use free version  
🟣 **Base_URL** - it contains sportmonks.com link, this one : https://api.sportmonks.com/v3/football   

## Classes 

### PLplayer  
Stands for basic data for players competing in Premier League and LaLiga. It contains info about:  
- player id,  
- player name,  
- g/a,  
- name of player's team.  

This class also have one method, show(). It's used just to help bot type info about certain player in proper formatting.  

### Player  
Almost same as PLplayer but it is used for sportmonks API. It contains less information, because I used the free version. Class fields:  
- player id,  
- player name.  

Again, one method for formating.  

### Match  
This class is helpful for storing data from sportmonks API. It contains info about:  
- match id,  
- teams names,  
- final score.  

Same as before it has one method (showMatch()), again only for proper text formatting.  

### Standing   
This class is quite different from the other ones. It has __init__() method, where we call for API data and initialize them into the created object. As argument it takes:  
- standing id,  
- standing participant id,  
- standing position.  


Again some kind od show() method.  

### Season  
Class for sportmonks API data, contains very basic info about seasons, it contains:  
- season id,  
- season name,  
- field that states if season is finished or not.  


Again some kind od show() method.  

### Team  
Class used for scraped data from Premier League and LaLiga. It contains:  
- team name,  
- team position in league,  
- team wins,  
- team draws,  
- team loses,  
- team points in league.  
Same as all above, one show() method.

### TODO
✅ **PL players statistics** - Make another API call from sofascore to get g/a and their average score per game.  
✅ **LaLiga statistics**  
⏳ **Unit tests**  
📌 **More QOL changes** - Bot is still pretty non-intuitive to use, fix that.  
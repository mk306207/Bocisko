# BOCISKO - discord bot for football data + bonuses

## Important before you start:
There is additional file that isn't in this repository, it is called klucze.py and it contains various private data, that you must fill out yourself according to this guide:  
🔵 **Klucz_bota** - it contains your discord bot key, that is neccessary for it to connect to discord  
🟢 **kanal & kanal_powitalny** - these two contains channels id, which determines where you want to perform specific actions (kanal_powitalny = channel, where bot greets people | kanal = deafult channel)  
🟡 **API_token** - your private api token from sportmonks.com, in this project i use free version  
🟣 **Base_URL** - it contains sportmonks.com link, this one : https://api.sportmonks.com/v3/football   

## Classes 
### PLplayer  
Stands for basic data for players competing in Premier League. It contains info about:  
- player id,  
- player name,  
- g/a,  
- name of player's team.  
This class also have one method, show(). It's used just to help bot type info about certain player in proper formatting.  
### Match  

### TODO
✅ **PL players statistics** - Make another API call from sofascore to get g/a and their average score per game.  
✅ **LaLiga statistics**  
⏳ **Unit tests**  
📌 **More QOL changes** - Bot is still pretty non-intuitive to use, fix that.  
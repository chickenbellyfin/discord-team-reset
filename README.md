# discord-team-reset-bot
Discord bot which moves all users to a specific voice channel when it gets a command. Used to reset teams.


### Example setup from Tribes community
Uses two bots (per team) to increase the number of players that can be moved before discord's rate limit. 

~/docker-compose.yaml: 
```
version: '3.6'

services:

 discord-team-reset-bot-ds:
   image: chickenbellyfin/discord-team-reset-bot
   container_name: discord-team-reset-bot-ds
   volumes:
     - './data/discord-team-reset-bot-ds:/data'
   restart: unless-stopped

 discord-team-reset-bot-be:
   image: chickenbellyfin/discord-team-reset-bot
   container_name: discord-team-reset-bot-be
   volumes:
     - './data/discord-team-reset-bot-be:/data'
   restart: unless-stopped
```


~/data/discord-team-reset-bot-be/config.yaml:
```
# copy to config.yaml
discord_bot_token: '<BE_DISCORD_BOT_TOKEN_HERE>'
bot_triggers: ['@team-reset', '/tr']
bot_channel_id: 853496607017795584 # #bots text channel
from_channels: ['[Bb]lood.*[Ee]agle', '[Bb][Ee]']
to_channel_id: 999517387319672852 # #Lobby voice channel
```

~/data/discord-team-reset-bot-ds/config.yaml:
```
discord_bot_token: '<DS_DISCORD_BOT_TOKEN_HERE>'
bot_channel_id: 853496607017795584 # #bots text channel
# listen for mentions of @team-reset
bot_triggers: ['@team-reset', '/tr']
from_channels: ['[Dd]iamond.*[Ss]word', '[Dd][Ss]']
to_channel_id: 999517387319672852 # #Lobby voice channel
```

Note that the BE & DS bot tokens must be two spearate bots.

Bot Setup:
  - Bot -> select server members intent
  - Bot -> select message content intent
  - Bot -> copy the token for  config.yaml
  - OAuth2 -> URL Generator
    1. click Scopes -> bot
    2. Bot Permissions:
      - Read messages/view channels
      - Add reactions
      - Move members
    3. Copy URL and paste into browser to add to server

After those 3 files are created, run `docker compose up -d`

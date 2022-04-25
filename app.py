import logging
import re
import yaml
import time
import sys
import os

import discord
from discord import VoiceChannel, Message

data_dir = ''
if len(sys.argv) > 1:
  data_dir = sys.argv[1]
  print(f'Using data dir {data_dir}')

logging.basicConfig(
  level=logging.DEBUG,
  format='%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s',
  handlers=[
    logging.FileHandler(os.path.join(data_dir, "team-reset.log")),
    logging.StreamHandler()
  ]
)
logging.getLogger('discord').setLevel(logging.ERROR)
logging.getLogger('asyncio').setLevel(logging.ERROR)

config_path = os.path.join(data_dir, 'config.yaml')
logging.info(f'Reading config from {config_path}')
with open(config_path) as config_file:
  config = yaml.safe_load(config_file)

discord_bot_token = config['discord_bot_token']
discord_bot_channel_id = int(config['bot_channel_id'])
discord_bot_triggers = config['bot_triggers']
from_channels = config['from_channels']
to_channel_id = int(config['to_channel_id'])

intents = discord.Intents.default()
intents.members = True
discord_client = discord.Client(guild_subscriptions=True, intents=intents)

def is_team_channel(channel):
  if type(channel) != VoiceChannel:
    return False

  if channel.id == to_channel_id:
    return False

  for pattern in from_channels:
    if re.match(pattern, channel.name):
      logging.debug(f'{channel.name} matches {pattern}')
      return True
  return False


async def do_reset_teams():    
  channels = discord_client.get_all_channels()
  members_to_move = set()
  for channel in channels:
    if is_team_channel(channel):
      members_to_move.update(set(channel.members))
    
  to_channel = discord_client.get_channel(to_channel_id)

  for member in members_to_move:
    logging.debug(f'Moving {member.name} to {to_channel_id}')
    try:
      await member.move_to(to_channel)
    except Exception as e:
      logging.error(e)
  return len(members_to_move)    


@discord_client.event
async def on_ready():
  logging.info(f'Connected to discord as {discord_client.user}')

@discord_client.event
async def on_message(message: Message):
  triggered = False
  for idx, trigger in enumerate(discord_bot_triggers):
    if message.clean_content.startswith(trigger):
      logging.info(f'Triggered by "{trigger}" in "{message.clean_content}" from @{message.author.display_name}')
      triggered = True
      break
  
  if not triggered:
    return
  
  if triggered and message.channel.id == discord_bot_channel_id:
    moved = await do_reset_teams()

    if moved > 0:
      await message.add_reaction('✅')
    else:
      await message.add_reaction('🤔')
    

discord_client.run(discord_bot_token)

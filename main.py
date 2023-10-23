import discord # for discord api
from discord.ui import Button, View # for buttons
from discord.ext import commands # for bot commands
import asyncio # for sleep
import os # for file handling
from dotenv import load_dotenv # for loading environment variables

load_dotenv() # load environment variables from .env file

# get environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD = os.getenv('DISCORD_GUILD')
NORGALAD_ID = os.getenv('NORGALAD_ID')
PEARL_ID = os.getenv('PEARL_ID')
ADAM_ID = os.getenv('ADAM_ID')

# test vs prod switch
test = False # set to True to run in test mode

# misc variables
muteTime = 20 if test else 180 # set mute time to 20 seconds if test, 3 minutes if prod
mutedUserID = ADAM_ID if test else NORGALAD_ID # set muted user to Adam if test, Norgalad if prod

# create intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# create bot
client = discord.Client(intents=intents)

# when bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}') # print bot name
    
    guild = client.get_guild(int(DISCORD_GUILD)) # get guild
    if guild: # if guild exists
        botChannel = discord.utils.get(guild.text_channels, name='bot-commands') # get bot-commands channel
        inGameChannel = discord.utils.get(guild.text_channels, name='in-game-memes') # get in-game channel
        if botChannel: # if bot-commands channel exists
            view = View() # create view
            button = Button(label='Mute Norgalad', style=discord.ButtonStyle.primary, custom_id='mute_norgalad') # create button
            view.add_item(button) # add button to view
            
            await botChannel.send('Mute Norgalad:', view=view) # send message with view to appear above button
            
            async def mute_callback(interaction): # mute callback
                member = discord.utils.get(guild.members, id=int(mutedUserID)) # get member
                if member: # if member exists
                    if member.voice: # if member is in a voice channel
                        await member.edit(mute=True) # mute member
                        await interaction.response.send_message(f'{member.name} has been muted for {muteTime/60} minutes.', ephemeral=True) # send message to bot-commands stating user has been muted
                        if not test: # if prod
                            await inGameChannel.send(f'{member.name} has committed crimes in Barovia and is in Trorgalad jail for {muteTime/60} minutes.') # send message to server stating user has been muted

                        await asyncio.sleep(muteTime)  # wait for set time

                        await member.edit(mute=False) # unmute member
                        await interaction.followup.send(f'{member.name} has been unmuted.', ephemeral=True) # send message stating user has been unmuted
                        if not test: # if prod
                            await inGameChannel.send(f'{member.name} has been released from jail, and is free once more.') # send message to server stating user has been unmuted
                    else: # if member is not in a voice channel
                        await interaction.response.send_message(f'{member.name} is not in a voice channel.', ephemeral=True) # send message stating user is not in a voice channel
                else: # if member does not exist
                    await interaction.response.send_message('Member not found in this server.', ephemeral=True) # send message stating member was not found in this server

            button.callback = mute_callback # set button callback

client.run(DISCORD_TOKEN)

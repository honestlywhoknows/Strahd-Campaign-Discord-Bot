import discord # for discord api
from discord.ui import Button, View # for buttons
from discord.ext import commands # for bot commands
import asyncio # for sleep
import os # for file handling
from dotenv import load_dotenv # for loading environment variables
from help import HelpCommand # for help command
from errors import handle_error # for error handling
from on_message_actions import MessageActions # for on message actions
import json # for json handling
import random # for random choice

load_dotenv() # load environment variables from .env file
with open("phrases.json", "r") as f: # load phrases from phrases.json
    phrases = json.load(f)

# get environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD = os.getenv('DISCORD_GUILD')
NORGALAD_ID = os.getenv('NORGALAD_ID')
PEARL_ID = os.getenv('PEARL_ID')
ADAM_ID = os.getenv('ADAM_ID')

# !!! IMPORTANT !!!
# test vs prod switch
test = True # set to True to run in test mode

# create intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# create bot
client = commands.Bot(command_prefix='!', intents=intents) # set command prefix and intents
client.help_command = HelpCommand() # set help command

# when bot is ready
@client.event
async def on_ready():
    await set_variables()
    if test:
        await print_test_info()
    await validate()
    print(f'We have logged in as {client.user}') # print bot name
    await mute_button()
    client.loop.create_task(background_button_check())

# misc variables
async def set_variables():
    global muteTime, mutedUserID, guild, botChannel, inGameMemesChannel # TODO: Refactor to remove globals
    muteTime = 20 if test else 180 # set mute time to 20 seconds if test, 3 minutes if prod
    mutedUserID = ADAM_ID if test else NORGALAD_ID # set muted user to Adam if test, Norgalad if prod
    print(f'Muted user: {mutedUserID}')
    guild = client.get_guild(int(DISCORD_GUILD)) # get guild
    print(f'Guild: {guild}')
    print(DISCORD_GUILD)
    botChannel = discord.utils.get(guild.text_channels, name='bot-commands') # get bot-commands channel
    inGameMemesChannel = discord.utils.get(guild.text_channels, name='in-game-memes') # get in-game channel

# print test info
async def print_test_info():
    print(DISCORD_GUILD)
    print(guild)
    print(mutedUserID)
    print(botChannel)
    print(inGameMemesChannel)
    
# validation
async def validate():
    if not DISCORD_TOKEN: # if discord token is not set
        raise Exception('Discord token not set.')
    if not DISCORD_GUILD: # if discord guild is not set
        raise Exception('Discord guild not set.')
    if not guild: # if guild does not exist
        raise Exception('Guild not found.')
    if not botChannel: # if bot-commands channel does not exist
        raise Exception('bot-commands channel not found.')
    if not inGameMemesChannel: # if in-game-memes channel does not exist
        raise Exception('in-game-memes channel not found.')

# background task to resend mute button if it is not visible on screen (aka if it is not within the last 20 messages)
async def background_button_check():
    await client.wait_until_ready() # wait until bot is ready
    while not client.is_closed(): # while bot is running
        found = False # set found to false
        async for message in botChannel.history(limit=20):  # Check last 20 messages
            if message.author == client.user and message.content == "Mute Norgalad:": # If message is from bot and is mute message
                found = True # set found to true
                break
        if not found: # if mute message was not found, resend mute button
            await mute_button()
        await asyncio.sleep(600)  # check every 10 minutes

# mute button
async def mute_button():
    view = View() # create view
    button = Button(label='Mute Norgalad', style=discord.ButtonStyle.red, emoji="🔇", custom_id='mute_norgalad') # create button
    button.callback = mute_callback # set button callback
    view.add_item(button) # add button to view   
    await botChannel.send('Mute Norgalad:', view=view) # send message with view to appear above button    
    
# mute callback
async def mute_callback(interaction): # mute callback
    member = discord.utils.get(guild.members, id=int(mutedUserID)) # get member
    if member: # if member exists
        if member.voice: # if member is in a voice channel
            await member.edit(mute=True) # mute member
            await interaction.response.send_message(f'{member.name} has been muted for {muteTime/60} minutes.', ephemeral=True) # send message to bot-commands stating user has been muted
            if not test: # if prod
                await inGameMemesChannel.send(f'{member.name} has committed crimes in Barovia and is in Trorgalad jail for {muteTime/60} minutes.') # send message to server stating user has been muted

            await asyncio.sleep(muteTime)  # wait for set time

            await member.edit(mute=False) # unmute member
            await interaction.followup.send(f'{member.name} has been unmuted.', ephemeral=True) # send message stating user has been unmuted
            if not test: # if prod
                await inGameMemesChannel.send(f'{member.name} has been released from jail, and is free once more.') # send message to server stating user has been unmuted
        else: # if member is not in a voice channel
            await interaction.response.send_message(f'{member.name} is not in a voice channel.', ephemeral=True) # send message stating user is not in a voice channel
    else: # if member does not exist
        await interaction.response.send_message('Member not found in this server.', ephemeral=True) # send message stating member was not found in this server

# manually resend mute button
@client.command(name='resend', help='The !resend command resends the mute button manually. Obviously.')
async def resend_mute_button(ctx):
    await botChannel.send('Why are you manually resending the mute button? This should have been done automatically. If my servants have failed to do so, report their insolence at once.')
    await mute_button()

# stupid ass deez command
@client.command(name='deez', aliases=['dez', 'deeznuts','deeznutz'], help='Why are you asking about this? What would a !deez command even do?')
async def deez(ctx):
    deez_response = random.choice(phrases["deez_responses"])
    await ctx.send(deez_response)

@commands.Cog.listener()
async def on_message(self, message):
    # prevent bot from responding to its own messages
    if message.author == self.bot.user:
        return
    # Check if the message is a DM. If it is a suggestion, post it in the suggestion channel. If it is a confession, post it in the confession channel
    if isinstance(message.channel, discord.DMChannel):
        if message.content.startswith('!suggestion'):
            await self.suggestion_box(message)
        elif message.content.startswith('!confession'):
            await self.confession_box(message)

# run bot
client.run(DISCORD_TOKEN)

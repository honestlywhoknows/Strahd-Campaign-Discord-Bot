import discord # for discord api
from discord.ui import Button, View # for buttons
from discord.ext import commands # for bot commands
import asyncio # for sleep
import os # for file handling
from help import HelpCommand # for help command
from errors import handle_error # for error handling
from on_message_actions import MessageActions # for on message actions
import json # for json handling
import random # for random choice
from config import Config # for config
from logger import setup_logger # for logging

# test vs prod switch
config = Config()
test = config.is_test_mode()

# set up logger
logger = setup_logger(test)

# create intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.dm_messages = True
intents.dm_reactions = True
intents.guild_messages = True
intents.guild_reactions = True
intents.messages = True

# create bot
bot = commands.Bot(command_prefix='!', intents=intents) # set command prefix and intents
bot.help_command = HelpCommand() # set help command

# when bot is ready
@bot.event
async def on_ready():  
    bot.config = Config()  # Attach config to bot instance 
    logger.info(f"Bot is running in {'test' if bot.config.is_test_mode() else 'production'} mode.")
    await set_variables()
    if test:
        await log_test_info()
    await validate()
    logger.info(f'We have logged in as {bot.user}')
    await mute_button()
    bot.loop.create_task(background_button_check())


async def main():
    await bot.add_cog(MessageActions(bot))
    await bot.start(config.discord_token)


# misc variables
async def set_variables():
    bot.guild = bot.get_guild(int(bot.config.discord_guild))
    bot.bot_channel = discord.utils.get(bot.guild.text_channels, name='bot-commands')
    bot.in_game_memes_channel = discord.utils.get(bot.guild.text_channels, name='in-game-memes') 
    #global config.mute_time, config.muted_user_id, guild, bot.bot_channel, bot.in_game_memes_channel # TODO: Refactor to remove globals
    logger.info(f'Muted user: {config.muted_user_id}')
    logger.debug(f'Guild: {bot.guild}')
    logger.debug(config.discord_guild)
    bot.bot_channel = discord.utils.get(bot.guild.text_channels, name='bot-commands') # get bot-commands channel
    bot.in_game_memes_channel = discord.utils.get(bot.guild.text_channels, name='in-game-memes') # get in-game channel

# log test info
async def log_test_info():
    logger.debug(config.discord_guild)
    logger.debug(bot.guild)
    logger.debug(config.muted_user_id)
    logger.debug(bot.bot_channel)
    logger.debug(bot.in_game_memes_channel)
    
# validation
async def validate():
    if not config.discord_token: # if discord token is not set
        raise Exception('Discord token not set.')
    if not config.discord_guild: # if discord guild is not set
        raise Exception('Discord guild not set.')
    if not bot.guild: # if guild does not exist
        raise Exception('Guild not found.')
    if not bot.bot_channel: # if bot-commands channel does not exist
        raise Exception('bot-commands channel not found.')
    if not bot.in_game_memes_channel: # if in-game-memes channel does not exist
        raise Exception('in-game-memes channel not found.')

# background task to resend mute button if it is not visible on screen (aka if it is not within the last 20 messages)
async def background_button_check():
    await bot.wait_until_ready() # wait until bot is ready
    while not bot.is_closed(): # while bot is running
        found = False # set found to false
        async for message in bot.bot_channel.history(limit=20):  # Check last 20 messages
            if message.author == bot.user and message.content == "Mute Norgalad:": # If message is from bot and is mute message
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
    await bot.bot_channel.send('Mute Norgalad:', view=view) # send message with view to appear above button    
    
# mute callback
async def mute_callback(interaction): # mute callback
    member = discord.utils.get(bot.guild.members, id=int(config.muted_user_id)) # get member
    if member: # if member exists
        if member.voice: # if member is in a voice channel
            await member.edit(mute=True) # mute member
            await interaction.response.send_message(f'{member.name} has been muted for {config.mute_time/60} minutes.', ephemeral=True) # send message to bot-commands stating user has been muted
            if not test: # if prod
                await bot.in_game_memes_channel.send(f'{member.name} has committed crimes in Barovia and is in Trorgalad jail for {config.mute_time/60} minutes.') # send message to server stating user has been muted

            await asyncio.sleep(config.mute_time)  # wait for set time

            await member.edit(mute=False) # unmute member
            await interaction.followup.send(f'{member.name} has been unmuted.', ephemeral=True) # send message stating user has been unmuted
            if not test: # if prod
                await bot.in_game_memes_channel.send(f'{member.name} has been released from jail, and is free once more.') # send message to server stating user has been unmuted
        else: # if member is not in a voice channel
            await interaction.response.send_message(f'{member.name} is not in a voice channel.', ephemeral=True) # send message stating user is not in a voice channel
    else: # if member does not exist
        await interaction.response.send_message('Member not found in this server.', ephemeral=True) # send message stating member was not found in this server

# manually resend mute button
@bot.command(name='resend', help='The !resend command resends the mute button manually. Obviously.')
async def resend_mute_button(ctx):
    await bot.bot_channel.send('Why are you manually resending the mute button? This should have been done automatically. If my servants have failed to do so, report their insolence at once.')
    await mute_button()

# stupid ass deez command
@bot.command(name='deez', aliases=['dez', 'deeznuts','deeznutz'], help='Why are you asking about this? What would a !deez command even do?')
async def deez(ctx):
    deez_response = random.choice(config.phrases["deez_responses"])
    await ctx.send(deez_response)

# run bot
if __name__ == '__main__':
    asyncio.run(main())

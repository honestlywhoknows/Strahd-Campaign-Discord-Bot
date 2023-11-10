import discord # for discord api
from discord.ext import commands # for bot commands
from Utility.config import Config # for config
import asyncio # for sleep
from Utility.help import HelpCommand # for help command
from Utility.errors import handle_error # for error handling
from on_message_actions import MessageActions # for on message actions
from Utility.logger import setup_logger # for logging
from fun import FunCog # for fun cog
from background import BackgroundCog
from Utility.bot_utilities import BotUtilityCog
import tracemalloc

# start memory tracing
tracemalloc.start()

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

fun = FunCog(bot)

# when bot is ready
@bot.event
async def on_ready():  
    bot.config = config  # Attach config to bot instance 
    logger.info(f"Bot is running in {'test' if config.is_test_mode() else 'production'} mode.")
    await set_variables()
    if test:
        await log_test_info()
    await validate()
    logger.info(f'We have logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="lording over my domain")) # set bot status
    bot_channel = bot.get_channel(int(config.bot_channel_id))
    await bot_channel.send('Fear not, the Count has returned to Castle Ravenloft. I trust you have not been causing trouble in my absence.')
    await fun.mute_button()
    bot.loop.create_task(BackgroundCog.background_button_check(bot))

async def main():
    await bot.add_cog(MessageActions(bot)) # add message actions cog
    await bot.add_cog(FunCog(bot)) # add fun cog
    await bot.add_cog(BackgroundCog(bot)) # add background cog
    await bot.add_cog(BotUtilityCog(bot)) # add bot utility cog
    await bot.start(config.discord_token)

# misc variables
async def set_variables():
    bot.guild = bot.get_guild(int(config.discord_guild))
    bot.bot_channel = bot.get_channel(int(config.bot_channel_id))
    bot.in_game_memes_channel = bot.get_channel(int(config.in_game_memes_channel_id))
    logger.info(f'Muted user: {config.muted_user_id}')
    logger.debug(f'Guild: {bot.guild}')
    logger.debug(config.discord_guild)

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

# run bot
if __name__ == '__main__':
    asyncio.run(main())

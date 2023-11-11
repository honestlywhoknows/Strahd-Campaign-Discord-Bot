import discord
from discord.ext import commands
import asyncio
from Utility.logger import logger
from fun import FunCog
from Utility.config import Config
from on_message_actions import MessageActions
from strahd_gpt import StrahdAICog

config = Config()

class BackgroundCog(commands.Cog, name="Background"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # background task to resend mute button if it is not visible on screen (aka if it is not within the last 20 messages)
    async def background_button_check(self):
        await self.wait_until_ready() # wait until bot is ready
        while not self.is_closed(): # while bot is running
            found = False # set found to false
            async for message in self.bot_channel.history(limit=20):  # Check last 20 messages
                if message.author == self.user and message.content == "Mute Norgalad:": # If message is from bot and is mute message
                    found = True # set found to true
                    break
            if not found: # if mute message was not found, resend mute button
                await FunCog.mute_button()
            await asyncio.sleep(600)  # check every 10 minutes
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        print(f'Message: {message.content}, Channel Type: {str(message.channel.type)}')
        logger.debug('I see a message')
        # prevent bot from responding to its own messages
        print (message.author)
        if str(message.author) == ('StrahdBotZarovich#0494'):
            logger.debug('This is me')
            return
        # Check if the message is a DM. If it is a suggestion, post it in the suggestion channel. If it is a confession, post it in the confession channel
        if str(message.channel.type) == 'private':
            logger.info('Received a DM')
            if message.content.lower().startswith('?suggest'):
                logger.debug('This is a suggestion')
                await MessageActions.suggestion_box(self, message.content, int(config.suggestion_channel_id))
            elif message.content.lower().startswith('?confess'):
                logger.debug('This is a confession')
                await MessageActions.confession_box(self, message.content, int(config.confession_channel_id))
            elif message.content.lower().startswith('?test-suggest'):
                logger.debug('This is a test suggestion')
                await MessageActions.suggestion_box(self, message.content, int(config.bot_playground_channel_id))
            elif message.content.lower().startswith('?test-confess'):
                logger.debug('This is a test confession')
                await MessageActions.confession_box(self, message.content, int(config.bot_playground_channel_id))
            else:
                strahd_response = await self.get_strahd_response(message.content)
                logger.debug('GPT DEBUG: Strahd response: ' + strahd_response)
                await message.channel.send(strahd_response)
        else:
            logger.debug('This is not a DM')

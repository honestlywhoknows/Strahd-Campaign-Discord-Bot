import discord
from discord.ext import commands
import random
import json
from dotenv import load_dotenv
import os
from Utility.config import Config
from Utility.logger import logger

config = Config()

test = config.is_test_mode()

class MessageActions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    async def suggestion_box(self, suggestion, channel, help='If you are so bold as to have a suggestion for the Count about his own domain, send it directly to my chambers with the command !suggestion.'):
        # Check if the suggestion is empty
        if suggestion == '':
            response = random.choice(config.phrases["no_suggestion_responses"])
            await suggestion.send(response)
            return
        # Pick a random intro
        intro = random.choice(config.phrases["suggestion_phrases"])
        # Send the suggestion to a specific channel
        target_channel = self.bot.get_channel(channel)
        suggestioncontent = suggestion.replace('?suggest ', '').replace('?Suggest ', '').replace('?SUGGEST ', '').replace('?sug ', '').replace('?Sug ', '').replace('?SUG ', '').replace('?suggestion ', '').replace('?Suggestion ', '').replace('?SUGGESTION ', '').replace('?suggestion ', '').replace('?Suggestion ', '').replace('?SUGGESTION ', '')
        suggestioncontent = suggestioncontent.replace('?test-suggest ','').replace('?Test-suggest ','').replace('?TEST-SUGGEST ','').replace('?test-sug ','').replace('?Test-sug ','').replace('?TEST-SUG ','').replace('?test-suggestion ','').replace('?Test-suggestion ','').replace('?TEST-SUGGESTION ','').replace('?test-suggestion ','').replace('?Test-suggestion ','').replace('?TEST-SUGGESTION ','')
        await target_channel.send(f'{intro}\n > _{suggestioncontent}_')

    async def confession_box(self, confession, channel, help='If you are bold enough to bear your sins anonymously, send it directly to my chambers with the command !confession.'):
        # Check if the confession is empty
        logger.debug('Checking if confession is empty')
        if confession == '':
            logger.debug('Confession is empty')
            response = random.choice(config.phrases["no_confession_responses"])
            await confession.send(response)
            return
        # Pick a random intro
        logger.debug('Picking a random intro')
        try:
            intro = random.choice(config.phrases["confession_box_phrases"])
        except KeyError:
            print("The key 'confession_phrases' does not exist in the 'phrases' dictionary.")
        except IndexError:
            print("The list associated with 'confession_phrases' is empty.")
        logger.debug('Intro: ' + intro)
        # Send the confession to a specific channel
        try:
            target_channel = self.bot.get_channel(channel)
        except KeyError:
            print("The channel ID does not exist.")
        except IndexError:
            print("The channel ID is empty.")
        except AttributeError:
            print(f'Channel ID: {channel}')
            print(f'Channel: {target_channel}')
            print("The channel ID is not an integer.")
        except TypeError:
            print(f'Channel ID: {channel}')
            print(f'Channel: {target_channel}')
            print("The channel ID is not an integer.")
        logger.debug('Sending confession to channel')
        confessioncontent = confession.replace('?confess ', '').replace('?Confess ', '').replace('?CONFESS ', '').replace('?conf ', '').replace('?Conf ', '').replace('?CONF ', '').replace('?confession ', '').replace('?Confession ', '').replace('?CONFESSION ', '').replace('?confession ', '').replace('?Confession ', '').replace('?CONFESSION ', '')
        confessioncontent = confessioncontent.replace('?test-confess ','').replace('?Test-confess ','').replace('?TEST-CONFESS ','').replace('?test-conf ','').replace('?Test-conf ','').replace('?TEST-CONF ','').replace('?test-confession ','').replace('?Test-confession ','').replace('?TEST-CONFESSION ','').replace('?test-confession ','').replace('?Test-confession ','').replace('?TEST-CONFESS ','')
        await target_channel.send(f'{intro}\n > _{confessioncontent}_')
        # send the confession formatted as a quote to the confession channel
        logger.debug('Sending confession as quote to channel')

async def setup(bot):
    await bot.add_cog(MessageActions(bot))
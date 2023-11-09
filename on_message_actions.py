import discord
from discord.ext import commands
import random
import json
from dotenv import load_dotenv
import os

with open("phrases.json", "r") as f:
    phrases = json.load(f)

load_dotenv()
SUGGESTIONS_CHANNEL_ID = int(os.getenv('SUGGESTIONS_CHANNEL_ID'))
CONFESSIONS_CHANNEL_ID = int(os.getenv('CONFESSIONS_CHANNEL_ID'))
test = True

class MessageActions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    async def suggestion_box(self, suggestion, channel, help='If you are so bold as to have a suggestion for the Count about his own domain, send it directly to my chambers with the command !suggestion.'):
        # Check if the suggestion is empty
        if suggestion == '':
            response = random.choice(phrases["no_suggestion_responses"])
            await suggestion.send(response)
            return
        # Pick a random intro
        intro = random.choice(phrases["suggestion_phrases"])
        # Send the suggestion to a specific channel
        target_channel = self.bot.get_channel(channel)
        suggestioncontent = suggestion.replace('?suggest ', '').replace('?Suggest ', '').replace('?SUGGEST ', '').replace('?sug ', '').replace('?Sug ', '').replace('?SUG ', '').replace('?suggestion ', '').replace('?Suggestion ', '').replace('?SUGGESTION ', '').replace('?suggestion ', '').replace('?Suggestion ', '').replace('?SUGGESTION ', '')
        await target_channel.send(f'{intro}\n------------------\n{suggestioncontent}')

    async def confession_box(self, confession, channel, help='If you are bold enough to bear your sins anonymously, send it directly to my chambers with the command !confession.'):
        # Check if the confession is empty
        if test: print('Checking if confession is empty')
        if confession == '':
            if test: print('Confession is empty')
            response = random.choice(phrases["no_confession_responses"])
            await confession.send(response)
            return
        # Pick a random intro
        if test: print('Picking a random intro')
        try:
            intro = random.choice(phrases["confession_box_phrases"])
        except KeyError:
            print("The key 'confession_phrases' does not exist in the 'phrases' dictionary.")
        except IndexError:
            print("The list associated with 'confession_phrases' is empty.")
        if test: print('Intro: ' + intro)
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
        if test: print('Sending confession to channel')
        confessioncontent = confession.replace('?confess ', '').replace('?Confess ', '').replace('?CONFESS ', '').replace('?conf ', '').replace('?Conf ', '').replace('?CONF ', '').replace('?confession ', '').replace('?Confession ', '').replace('?CONFESSION ', '').replace('?confession ', '').replace('?Confession ', '').replace('?CONFESSION ', '')
        await target_channel.send(f'{intro}\n------------------\n{confessioncontent}')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        print(f'Message: {message.content}, Channel Type: {str(message.channel.type)}')
        if test: print('I see a message')
        # prevent bot from responding to its own messages
        print (message.author)
        if str(message.author) == ('StrahdBotZarovich#0494'):
            if test: print('This is me')
            return
        # Check if the message is a DM. If it is a suggestion, post it in the suggestion channel. If it is a confession, post it in the confession channel
        #if isinstance(message.channel, discord.channel.DMChannel):
        if str(message.channel.type) == 'private':
            if test: print('Received a DM')
            if message.content.lower().startswith('?suggest'):
                if test: print('This is a suggestion')
                await self.suggestion_box(message.content, int(SUGGESTIONS_CHANNEL_ID))
            elif message.content.lower().startswith('?confess'):
                if test: print('This is a confession')
                await self.confession_box(message.content, int(CONFESSIONS_CHANNEL_ID))
        else:
            print('This is not a DM')
        #await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(MessageActions(bot))
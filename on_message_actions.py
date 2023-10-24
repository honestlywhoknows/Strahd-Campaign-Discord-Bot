import discord
from discord.ext import commands
import random
import json

with open("phrases.json", "r") as f:
    phrases = json.load(f)

class MessageActions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def setup(bot):
        bot.add_cog(MessageActions(bot))

    async def suggestion_box(self, suggestion, channel, help='If you are so bold as to have a suggestion for the Count about his own domain, send it directly to my chambers with the command !suggestion.'):
        # Check if the suggestion is empty
        if suggestion == '':
            response = random.choice(phrases["no_suggestion_responses"])
            await suggestion.send(response)
            return
        # Pick a random intro
        intro = random.choice(phrases["suggestion_intros"])
        # Send the suggestion to a specific channel
        target_channel = self.bot.get_channel(channel)
        await target_channel.send(f'{intro}')
        await target_channel.send('------------------')
        await target_channel.send(f'{suggestion}')

    async def confession_box(self, confession, channel, help='If you are bold enough to bear your sins anonymously, send it directly to my chambers with the command !confession.'):
        # Check if the confession is empty
        if confession == '':
            response = random.choice(phrases["no_confession_responses"])
            await confession.send(response)
            return
        # Pick a random intro
        intro = random.choice(phrases["confession_intros"])
        # Send the confession to a specific channel
        target_channel = self.bot.get_channel(channel)
        await target_channel.send(f'{intro}')
        await target_channel.send('------------------')
        await target_channel.send(f'{confession}')
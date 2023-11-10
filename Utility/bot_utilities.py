import discord
from discord.ext import commands
import asyncio
from Utility.logger import logger
import requests # for http requests
from Utility.config import Config # for config
from Utility.errors import handle_error # for error handling
import aiohttp # for async http requests

config = Config()

class BotUtilityCog(commands.Cog, name = "BotUtility"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # send bug report to github issues
    async def send_bug_report(self,title: str, bug: str, user: str):
        url = f'https://api.github.com/repos/{config.github_repo_owner}/{config.github_repo_name}/issues'
        headers = {'Authorization': f'token {config.github_token}'}
        data = {'title': f'Discord Bug Report - {user} {title} . . .', 'body': bug}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                response_text = await response.text()
                logger.info(f'BUGREPORT: Sent bug report to GitHub issues. Response: {response.status}')
                logger.debug(response_text)
                return response.status, response_text
        #response = requests.post(url, headers=headers, json=data)
        #logger.info(f'BUGREPORT: Sent bug report to github issues. Response: {response}')

    # bug report command
    @commands.command(name='bug', help='Use !bug to report any disorder in my domain. I will deal with it accordingly.')
    async def bug(self, ctx, *, bug: str):
        logger.info(f'BUGREPORT: User {ctx.author} has reported a bug: {bug}')
        spaces = bug.count(' ')
        words = bug.split(' ')
        title = ''.join(words[:5]) if len(words) > 5 else bug
        response = await self.send_bug_report(title, bug, str(ctx.author))
        if response[0] == 201 or response[0] == 200:
            await ctx.send("Your report has been filed into the Castle's records.")
        else:
            await ctx.send("Your report could not be filed into the Castle's records. Please alert your Dungeon Master.")


    # maintenance command
    @commands.command(name='maintenance', help='For official use by the Count or those under his direct command.')
    async def maintenance(self, ctx):
        if ctx.author.id == int(config.adam_id):
            bot_channel = self.bot.get_channel(int(config.bot_channel_id))
            await bot_channel.send('I have a pressing matter to attend to. I shall take my leave for now.')
            await self.bot.change_presence(activity=discord.Game(name="travelling the lands of Barovia"))
            await self.bot.close()
        else:
            await ctx.send('You think you are worthy of dismissing the Lord of Barovia? Begone.')
import discord
from discord.ext import commands
import asyncio
from Utility.logger import logger
from discord.ui import Button, View # for buttons
from Utility.config import Config # for config
import random

config = Config()
test = config.is_test_mode()

class FunCog(commands.Cog, name="Fun"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # mute button
    async def mute_button(self):
        view = View() # create view
        button = Button(label='Mute Norgalad', style=discord.ButtonStyle.red, emoji="🔇", custom_id='mute_norgalad') # create button
        button.callback = self.mute_callback # set button callback
        view.add_item(button) # add button to view   
        await self.bot.bot_channel.send('Mute Norgalad:', view=view) # send message with view to appear above button    
        
    # mute callback
    async def mute_callback(self, interaction): # mute callback
        member = discord.utils.get(self.bot.guild.members, id=int(config.muted_user_id)) # get member
        if member: # if member exists
            if member.voice: # if member is in a voice channel
                await member.edit(mute=True) # mute member
                await interaction.response.send_message(f'{member.name} has been muted for {config.mute_time/60} minutes.', ephemeral=True) # send message to bot-commands stating user has been muted
                if not test: # if prod
                    await self.bot.in_game_memes_channel.send(f'{member.name} has committed crimes in Barovia and is in Trorgalad jail for {config.mute_time/60} minutes.') # send message to server stating user has been muted

                await asyncio.sleep(config.mute_time)  # wait for set time

                await member.edit(mute=False) # unmute member
                await interaction.followup.send(f'{member.name} has been unmuted.', ephemeral=True) # send message stating user has been unmuted
                if not test: # if prod
                    await self.bot.in_game_memes_channel.send(f'{member.name} has been released from jail, and is free once more.') # send message to server stating user has been unmuted
            else: # if member is not in a voice channel
                await interaction.response.send_message(f'{member.name} is not in a voice channel.', ephemeral=True) # send message stating user is not in a voice channel
        else: # if member does not exist
            await interaction.response.send_message('Member not found in this server.', ephemeral=True) # send message stating member was not found in this server

    # manually resend mute button
    @commands.command(name='resend', help='The !resend command resends the mute button to the Dungeon Master manually. Obviously.')
    async def resend_mute_button(self, ctx):
        await self.bot.bot_channel.send('Why are you manually resending the mute button? This should have been done automatically. If my servants have failed to do so, report their insolence at once.')
        await self.mute_button()

    # stupid ass deez command
    @commands.command(name='deez', aliases=['dez', 'deeznuts','deeznutz'], help='Why are you asking about this? What would a !deez command even do?')
    async def deez(self, ctx):
        deez_response = random.choice(config.phrases["deez_responses"])
        await ctx.send(deez_response)
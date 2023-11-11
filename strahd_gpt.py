import discord
from discord.ext import commands
import openai
from Utility.config import Config
from Utility.logger import logger

config = Config()


class StrahdAICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conversation_history = []
        openai.api_key = config.open_ai_token  # Replace with your OpenAI API key

    def update_conversation_history(self, player_message, strahd_response):
        self.conversation_history.append(f"Player: {player_message}")
        self.conversation_history.append(f"Strahd: {strahd_response}")

        # Keep only the last few exchanges (e.g., the last 4 messages)
        if len(self.conversation_history) > 8:
            self.conversation_history.pop(0)
            self.conversation_history.pop(0)

    async def get_strahd_response(self, player_message):
        # Character and story context
        strahd_character_context = (
            "Strahd von Zarovich is a cunning and charismatic vampire, known for his manipulative and menacing demeanor. "
            "He speaks in a confident, calculated manner, often with a sense of dark humor."
        )
        current_story_context = (
            "The tiefling warlock of the group, Mordecai, has just married a hag in the city of Vallaki."
            "The officiant disappeared and chaos erupted as the vampire spawn they failed to kill two days ago start attacking the crowd."
        )
        prompt = "\n".join(self.conversation_history) + "\n"
        prompt += f"Player: {player_message}\nStrahd: "

        response = openai.Completion.create(
            engine="text-davinci-003",  # or the latest available engine
            prompt=prompt,
            max_tokens=150,  # Adjust as needed
            temperature=0.7  # Adjust for creativity level
        )

        strahd_response = response.choices[0].text.strip()
        self.update_conversation_history(player_message, strahd_response)
        return strahd_response

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return

        # Example check: respond only to specific channel or condition
        if message.channel.name == 'strahd-channel':  # Replace with your specific condition
            strahd_response = await self.get_strahd_response(message.content)
            await message.channel.send(strahd_response)

def setup(bot):
    bot.add_cog(StrahdAICog(bot))

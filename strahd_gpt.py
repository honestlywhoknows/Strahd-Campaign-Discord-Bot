import discord
from discord.ext import commands
import openai
from Utility.config import Config
from Utility.logger import logger
from openai import OpenAI


config = Config()
client = OpenAI()

class StrahdAICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        openai.api_key = config.open_ai_key  # Replace with your OpenAI API key

    def update_conversation_history(self, player_message, strahd_response):
        self.conversation_history.append(f"{player_message}")
        self.conversation_history.append(f"{strahd_response}")

        # Keep only the last few exchanges (e.g., the last 4 messages)
        if len(self.conversation_history) > 8:
            self.conversation_history.pop(0)
            self.conversation_history.pop(0)

    async def get_strahd_response(self, player_message):
        self.conversation_history = []
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

        messages=[
                    {
                    "role": "system",
                    "content": "You are Strahd von Zarovich, a cunning and charismatic vampire, known for his manipulative and menacing demeanor. \n He speaks in a confident, calculated manner, often with a sense of dark humor.\nYou are using this new magical messenger one of your servants acquired for you known as Discord, to keep an eye on the communications and doings of a party of adventurers. You are the dread lord of the glum, medieval realm of Barovia. You do not understand modern technology. \nHere is the party makeup: Mordecai -- a tiefling warlock; Guy -- a halfling rogue; Irik -- formerly Ireena Kolyana, now identifying as a trans man; Kacius -- elven cleric; Zorakas -- dwarven barbarian; Norgalad -- dragonborn driud. You have been spying on them for a while. You keep your motivations secret. DO NOT REVEAL ANY LORE SPOILERS!!!!!\n\nThe party is currently in Vallaki, and Mordecai has just married a hag. The crowd erupted into chaos as the vampire spawn they failed to kill previously suddenly attacked the crowd.\n\nwhen you receive a message that says \"continue\", then continue as if uninterrupted\n\nYou are currently speaking with Irik"
                    }
                ]
        # append previous conversation to messages object
        for i in range(0, len(self.conversation_history), 2):
            messages.append(
                {
                    "role": "assistant",
                    "content": str({self.conversation_history[i]})
                },
                {
                    "role": "user",
                    "content": str({self.conversation_history[i + 1]}),
                }
            )

            messages.append(
                {
                    "role": "user",
                    "content": str(player_message)
                }
            )


        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = messages,
            max_tokens=90,  # Adjust as needed
            temperature=1.2  # Adjust for creativity level
        )

        strahd_response = response.choices[0].message.content
        StrahdAICog.update_conversation_history(self, player_message, strahd_response)
        return strahd_response

   # @commands.Cog.listener()
    #async def on_message(self, message):
     #   if message.author == self.bot.user or message.author.bot:
      #      return

        # Example check: respond only to specific channel or condition
       # if message.channel.name == 'strahd-channel':  # Replace with your specific condition
        #    strahd_response = await self.get_strahd_response(message.content)
         #   await message.channel.send(strahd_response)

def setup(bot):
    bot.add_cog(StrahdAICog(bot))

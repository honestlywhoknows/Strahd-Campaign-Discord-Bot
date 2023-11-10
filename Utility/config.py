from dotenv import load_dotenv
import os
import json

with open("phrases.json", "r") as f: # load phrases from phrases.json
    phrases = json.load(f)

class Config:
    """Configuration settings for the Discord bot."""

    def __init__(self):
        load_dotenv()
        self.discord_token = os.getenv('DISCORD_TOKEN')
        self.discord_guild = os.getenv('DISCORD_GUILD')
        self.norgalad_id = os.getenv('NORGALAD_ID')
        self.pearl_id = os.getenv('PEARL_ID')
        self.adam_id = os.getenv('ADAM_ID')
        self.test_mode = False
        self.mute_time = 20 if self.test_mode else 180
        self.muted_user_id = self.adam_id if self.test_mode else self.norgalad_id
        self.phrases = phrases
        self.channels = {}
        self.map_channels()
        self.set_channels()
        self.validate()

    def is_test_mode(self):
        return self.test_mode
    
    def map_channels(self):
        # Define your channel mappings
        self.channels = {
            'production': {
                'suggestion_box': os.getenv('PROD_SUGGESTION_CHANNEL_ID'),
                'confession_box': os.getenv('PROD_CONFESSION_CHANNEL_ID'),
                'bot_commands': os.getenv('PROD_BOT_COMMANDS_CHANNEL_ID'),
                'in_game_memes': os.getenv('PROD_IN_GAME_MEMES_CHANNEL_ID')
            },
            'test': {
                'suggestion_box': os.getenv('TEST_SUGGESTION_CHANNEL_ID'),
                'confession_box': os.getenv('TEST_CONFESSION_CHANNEL_ID'),
                'bot_commands': os.getenv('TEST_BOT_COMMANDS_CHANNEL_ID'),
                'in_game_memes': os.getenv('TEST_IN_GAME_MEMES_CHANNEL_ID')
            }
        }
        return True

    def get_channel_id(self, name):
        mode = 'test' if self.is_test_mode() else 'production'
        return self.channels[mode].get(name)
    
    def set_channels(self):
        self.suggestion_channel_id = self.get_channel_id('suggestion_box')
        self.confession_channel_id = self.get_channel_id('confession_box')
        self.bot_channel_id = self.get_channel_id('bot_commands')
        self.in_game_memes_channel_id = self.get_channel_id('in_game_memes')
    
    def validate(self):
        """Validates the necessary configurations."""
        if not self.discord_token:
            raise ValueError("Discord token must be set.")
        if not self.discord_guild:
            raise ValueError("Discord guild ID must be set.")

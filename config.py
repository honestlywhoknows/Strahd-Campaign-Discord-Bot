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
        self.test_mode = True
        self.mute_time = 20 if self.test_mode else 180
        self.muted_user_id = self.adam_id if self.test_mode else self.norgalad_id
        self.phrases = phrases
        self.validate()

    def is_test_mode(self):
        return self.test_mode
    
    def validate(self):
        """Validates the necessary configurations."""
        if not self.discord_token:
            raise ValueError("Discord token must be set.")
        if not self.discord_guild:
            raise ValueError("Discord guild ID must be set.")

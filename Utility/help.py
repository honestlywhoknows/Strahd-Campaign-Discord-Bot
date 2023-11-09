# help.py
from discord.ext import commands

class HelpCommand(commands.DefaultHelpCommand):
    def __init__(self, **options):
        super().__init__(**options)

    async def send_bot_help(self, mapping):
        # bot greeting in the tone of Strahd von Zarovich
        await self.context.send("Welcome to the world of Barovia. I am Count Strahd von Zarovich, your host. I understand that you seek knowledge of me. I will share with you all that I know.")

        # check if there are any commands
        all_commands = []
        for cog, commands in mapping.items():
            all_commands.extend(commands)

        if not all_commands:
            await self.context.send('You fool. There are no commands to display. You have wasted my time.')
            await self.context.send('(This is a bug, please report)')
        else:
            await self.context.send('Here is a list of commands:')
            for command in all_commands:
                if not command.hidden and command.enabled:
                    await self.context.send(command.name)
            await self.context.send('Type !help <command> if you can\'t figure out for yourself what a command does.')
            await self.context.send('You may also send me a direct message with your ?suggestions or ?confessions. My servants will forward them along.')

    async def send_command_help(self, command):
        if command.name == 'help':
            await self.context.send('You absolute fool. You are already in the help menu, are you not?')
        else:
            await self.context.send(command.help)

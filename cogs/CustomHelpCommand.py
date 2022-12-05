import discord
from discord.ext import commands 

# [DEBUG]
class CustomHelpCommand(commands.HelpCommand):
    
    def __init__(self):
        super().__init__()
        
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", color=0x9146ff)
        for cog in mapping:
            embed.add_field(name = cog.qualified_name, value = [command.name for command in mapping[cog]])
        self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=cog.qualified_name, color=0x9146ff, description=cog.description)
        for command_name in cog.get_commands():
            embed.add_field(name = command_name)
        self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=command.name, color=0x9146ff, description=command.brief)
        embed.add_field(name = command.qualified_name, value=command.help)
        self.get_destination().send(embed=embed)




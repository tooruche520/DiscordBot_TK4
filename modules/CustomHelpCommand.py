import discord
from discord.ext import commands 

class CustomHelpCommand(commands.HelpCommand):
    
    def __init__(self):
        super().__init__()
        
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", color=0xFC7B0A, description="小幫手來幫你啦!\n現在可以攝影棚可以用這些指令")
        for cog in mapping:
            if cog is not None:
                command_list = [command.name for command in mapping[cog]]
                if not command_list:
                    command_list_data = "No command!!"
                else:
                    command_list_data = ", ".join(command_list)
                    embed.add_field(name = cog.qualified_name, value = command_list_data)
                # print (command_list)
                # print("================================================")
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=cog.qualified_name, color=0xFC7B0A, description=cog.description)
        for command in cog.get_commands():
            if command is not None: 
                # print(command)
                embed.add_field(name = command.qualified_name, value=command.brief)
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=command.name, color=0xFC7B0A, description=command.brief)
        embed.add_field(name = "使用方法", value=command.help)
        await self.get_destination().send(embed=embed)



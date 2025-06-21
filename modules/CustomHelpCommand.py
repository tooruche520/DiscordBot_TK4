import discord
from discord.ext import commands 
import logging as log

class HelpPaginator(discord.ui.View):
    def __init__(self, embeds: list[discord.Embed]):
        super().__init__(timeout=120)
        self.embeds = embeds
        self.current_page = 0
        self._update_buttons()

    def _update_buttons(self):
        # Previous button
        self.children[0].disabled = self.current_page == 0
        # Next button
        self.children[1].disabled = self.current_page == len(self.embeds) - 1

    async def update_message(self, interaction: discord.Interaction):
        self._update_buttons()
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

    @discord.ui.button(label="上一頁", style=discord.ButtonStyle.blurple, emoji="⬅️")
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        await self.update_message(interaction)

    @discord.ui.button(label="下一頁", style=discord.ButtonStyle.blurple, emoji="➡️")
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        await self.update_message(interaction)


class CustomHelpCommand(commands.HelpCommand):
    
    def __init__(self):
        super().__init__()
        
    async def send_bot_help(self, mapping):
        # Collect all commands first
        all_commands = []
        debug_commands = []
        debug_cog = None

        for cog, commands_list in mapping.items():
            if cog is not None and cog.qualified_name == "DebugCommand":
                debug_cog = cog
                continue
            
            filtered = await self.filter_commands(commands_list, sort=True)
            all_commands.extend(filtered)

        # Handle debug commands separately to add them at the end
        if debug_cog:
            filtered_debug = await self.filter_commands(mapping[debug_cog], sort=True)
            all_commands.extend(filtered_debug)

        # Create pages
        commands_per_page = 10  # Safe number of fields per embed
        pages = [all_commands[i:i + commands_per_page] for i in range(0, len(all_commands), commands_per_page)]

        if not pages:
            await self.get_destination().send("沒有可以顯示的指令。")
            return

        embeds = []
        for i, page_commands in enumerate(pages):
            embed = discord.Embed(
                title=f"幫助指令 (第 {i+1}/{len(pages)} 頁)",
                description="小幫手來幫你啦!\n現在攝影棚可以用這些指令",
                color=0xFC7B0A
            )
            for command in page_commands:
                brief = command.brief if command.brief else f"發送\"{command.name}\"的回應"
                embed.add_field(name=f'!{command.name}', value=brief, inline=False)
            embeds.append(embed)

        # Create paginator and send the first page
        paginator = HelpPaginator(embeds)
        await self.get_destination().send(embed=paginator.embeds[0], view=paginator)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=cog.qualified_name, color=0xFC7B0A, description=cog.description)
        for command in await self.filter_commands(cog.get_commands(), sort=True):
            if command is not None: 
                brief = command.brief if command.brief else "No description available"
                embed.add_field(name=command.qualified_name, value=brief)
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=command.name, color=0xFC7B0A, description=command.brief)
        embed.add_field(name="使用方法", value=command.help)
        await self.get_destination().send(embed=embed)

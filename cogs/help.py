from __main__ import ErrorParser

from typing import Optional
from discord.ext import commands
from discord import Embed, Colour
# manabot.utilities/handling.py


class HelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return f"{self.clean_prefix}{command.qualifed_name} {command.signature}"

    async def command_not_found(self, cmd: str) -> str:
        return f"Couldn't find command ``{cmd}``, did you misspell?"
        
    async def send_error_message(self, err: str) -> str:
        await self.get_destination().send(embed=ErrorParser(description=err, colour=Colour.red()))
        
    async def help_embed(self, title: str, description: Optional[str] = None, mapping: Optional[dict] = None, 
    command_set: Optional[list] = None):
        embed = Embed(title=title)
        embed.colour = Colour.blue()
        
        if description:
            embed.description = description
        if command_set:
            filtered = await self.filter_commands(command_set, sort=True)
            if filtered != None:
                name="Commands"
                value = ""
                for cmd in filtered:
                    value = value + f"``{cmd.qualified_name}`` "
                
                embed.add_field(name=name, value=value)
        if mapping: # called with cogs/commands
            print(type(mapping))
            for cog, cmd_list in mapping.items():
                filtered = await self.filter_commands(cmd_list, sort=True)
                if filtered == None:
                    # No commands were filtered
                    continue 
                
                cmds = "\u2002".join(f'{cmd.name}' for cmd in filtered)
                
                name = cog.qualified_name if cog != None else "Uncategorized"
                value = (
                    f'{cog.description}\n``{cmds}``' if cog and cog.description else
                    f'No description.``\n{cmds}``' if cmds else
                    f'No description or commands.'
                )
                embed.add_field(name=name, value=value, inline=True)    
            
        return embed

    async def send_bot_help(self, mapping: dict) -> dict:
        embed = await self.help_embed(
            title="mana, help me!",
            description=f"""
            a full list of commands available to the public, current prefix is ``{self.clean_prefix}``
            ``<>`` are required arguments, ``[]`` are optional arguments.
            """,
            mapping=mapping
        )
        await self.get_destination().send(embed=embed)
        
    async def send_command_help(self, command: commands.Command) -> commands.Command:
        embed = Embed(title=command.qualified_name)
        embed.description = command.help if command.help else 'No description'
        embed.colour = Colour.blue()
        # Aliases
        embed.add_field(name="Aliases", value=f"``{', '.join(command.aliases)}``" if command.aliases else "``No aliases``")
        embed.add_field(name="Syntax", value=f"``{command.usage}``")
        await self.get_destination().send(embed=embed)
        
    async def send_cog_help(self, cog: commands.Cog) -> commands.Cog:
        embed = await self.help_embed(
            title=f"mana, i need help with the {cog.qualified_name.lower()} cog!",
            description=f"{cog.description}\n\ndo ``{self.clean_prefix}help [command]`` for more information on any command",
            command_set=cog.get_commands()
        )
        await self.get_destination().send(embed=embed)

class Help(commands.Cog, name="Support"):
    """
    all support related commands
    """
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = HelpCommand()
        bot.help_command.cog = self
        
    
        
def setup(bot):
    bot.add_cog(Help(bot))
       

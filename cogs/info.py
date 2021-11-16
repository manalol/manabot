import discord
import logging
import json
from discord.ext import commands

class Information(commands.Cog, name="Info"):
    """
    find extra information related to the bot, server and more
    """
    def __init__(self, bot):
        self.bot = bot
        self.logs = logging.getLogger('discord')
        
    @commands.command(name="ping", aliases=["latency"])
    @commands.cooldown(rate=3, per=4.0)
    async def ping(self, ctx):
        """
        Query the current latency of the bot
        """
        message = await ctx.send("Determining latency. :brain: ")
        time = round(self.bot.latency, 2)
        
        if 3 < time:
            await message.edit(content=f":red_circle: Pinged in {time} seconds! Woah there, it seems like the server is taking a while to respond.")
            self.logs.critical(f"Woah there, the server is taking a noticeable amount of time to respond: {time}")
        elif 1 < time < 3:
            await message.edit(content=f":yellow_circle: Pinged in {time} seconds! The server is moderately slow.")
            self.logs.warning(f"The server took {time} seconds to respond, moderately slow.")
        if time < 1:
            await message.edit(content=f":green_circle: Pinged in {time} seconds! The server is responding quickly!")
       
    @commands.command(name="about")
    async def about(self, ctx):
        """
        Information about the bot
        """
        embed = discord.Embed(title="About manabot")
        embed.colour = discord.Colour.green()
        
        embed.description = f"""
        Manabot is a multi-functional discord bot owned and maintained by ``{await self.bot.fetch_user(self.bot.settings['owner_id'])}``
        This bot is designed for the sole purpose of allowing myself to experiment and get used to the discord.py library.
        """
        value = f"""
        Guilds: ``{len(self.bot.guilds)}``
        Commands: ``{len(self.bot.commands)}``
        Version: ``{self.bot.settings['version']}``
        """
        embed.add_field(name="Status", value=value)
        embed.add_field(name="Changelog", value=f"{self.bot.settings['changelog']}")
            
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Information(bot))
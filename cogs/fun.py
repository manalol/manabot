import discord
from discord.ext import commands

class Fun(commands.Cog, name="Fun"):
    """
    in the mood to feel a little goofy? mess around with some commands
    """
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="isrole", usage="isrole <role>")
    async def isrole(self, ctx, *, role: discord.Role) -> discord.Role:
        """
        Checks if the caller has a role
        """
        roles = ctx.author.roles
        if role in roles:
            await ctx.send("You do have that role!")
        else:
            await ctx.send("You dont have that role!")
        
 
def setup(bot):
    bot.add_cog(Fun(bot))
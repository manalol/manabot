from discord.ext import commands
from discord.ext.commands import ExtensionNotFound, ExtensionFailed, NoEntryPointError
from utilities.handling import ErrorParser

import discord
import logging
import glob
import time
import json



class Manabot(commands.Bot):
    def __init__(self, prefix: str, *args, **kwargs):
        self.logs = logging.getLogger('discord')
        with open("settings.json", "r") as s:
            settings = json.load(s)
            self.settings = settings
            self.owner_id = settings['owner_id']
            self.prefix = prefix
            super().__init__(prefix, *args, **kwargs)



    async def on_ready(self):
        """
        Load the extensions for the bot and handle
        any other startup functions.
        """
        self.logs.info("Manabot launched succesfully")
        length = time.time()
        count = 0
        try:
            for file in glob.glob("cogs/*.py"):
                self.logs.info(f"Attempting to load the {file[5:-3]} extension")
                self.load_extension(f"cogs.{file[5:-3]}")
        except ExtensionNotFound as err:
            self.logs.error(f"{err.name} could not be located, extension not found")
        except (ExtensionFailed, NoEntryPointError) as err:
            self.logs.error(f"{err.name} failed with its setup function: {err}")
        finally:
            self.logs.info(f"Loaded {len(self.cogs)} extension(s) in {time.time() - length} seconds")


    async def on_message(self, ctx):
        """
        Processes all incoming messages.
        """
        if ctx.author != self.user:
            await self.process_commands(ctx)

    async def on_command_error(self, ctx, excep):
        if isinstance(excep, commands.ArgumentParsingError):
            await ctx.send(embed=ErrorParser(description=excep))
        elif isinstance(excep, commands.CommandNotFound):
            pass
        elif isinstance(excep, commands.CommandInvokeError):
            await ctx.send(excep.original)
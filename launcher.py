import discord
import logging
import json

from utilities.handling import ErrorParser
from manabot import Manabot

# TODO
# Get the bot up and running
# Load cogs


def run_logging():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='logs.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)


def run_bot():
    """
    Runs the bot with logging
    """
    
    run_logging()
    with open("settings.json", "r") as s:
        settings = json.load(s)
        bot = Manabot(settings['prefix'])
        token = settings['token']
        bot.run(token)
        
        
if __name__ == "__main__":
    run_bot()
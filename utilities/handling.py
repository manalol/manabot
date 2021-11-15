from discord import Embed, Colour

def ErrorParser(**kwargs):
    embed = Embed(title="An error occured")
    embed.colour = Colour.red()
    
    for kwarg, value in kwargs.items():
        setattr(embed, kwarg, value)
        
    return embed
    

        
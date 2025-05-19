from redbot.core import commands


class CTF(commands.Cog, name="ctfcogs.CTF"):
    """
    Commands that combine multiple cogs features together
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

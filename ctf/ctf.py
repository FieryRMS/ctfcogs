from redbot.core import commands


class CTF(commands.Cog, name="ctfcogs.CTF"):
    """
    Commands that streamline common flows by combining multiple cogs together
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

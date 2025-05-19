from redbot.core import commands


class CTFd(commands.Cog, name="ctfcogs.CTFd"):
    """A cog that manages CTFd contests"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

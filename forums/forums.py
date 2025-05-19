from redbot.core import commands


class Forums(commands.Cog, name="ctfcogs.Forums"):
    """A cog for creating and managing CTF channels and forums."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

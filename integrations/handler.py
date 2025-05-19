from redbot.core import commands


class Integrations(commands.Cog, name="ctfcogs.Integrations"):
    """
    Commands that combine multiple cogs features together
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

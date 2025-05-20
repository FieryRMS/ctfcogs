from redbot.core import commands

from .forums import Forums


async def setup(bot: commands.Bot):
    await bot.add_cog(Forums(bot))

from redbot.core import commands

from .forum import Forum


async def setup(bot: commands.Bot):
    await bot.add_cog(Forum(bot))

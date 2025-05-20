from platform.platform import Platform

from redbot.core import commands


async def setup(bot: commands.Bot):
    await bot.add_cog(Platform(bot))

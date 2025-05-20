from redbot.core import commands

from .ctf import CTF


async def setup(bot: commands.Bot):
    await bot.add_cog(CTF(bot))

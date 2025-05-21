from redbot.core import Config, commands


class CTF(commands.Cog, name="ctfcogs.CTF"):
    """
    Commands that streamline common flows by combining multiple cogs together
    """

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(self, 3646819334)

    @commands.hybrid_group()
    async def ctf(self, ctx: commands.Context):
        """
        All in one command to manage CTFs.
        """
        pass

    @ctf.command()
    async def create(self, ctx: commands.Context, url: str, uname: str, pwd: str) -> None:
        """
        Login, fetch and create a new CTF channel and forum with challenges.

        Parameters
        ----------
        url: str
            The URL of the CTF to create a channel and forum for.
        uname: str
            The username to login with.
        pwd: str
            The password to login with.
        """
        raise NotImplementedError()

    @ctf.command()
    async def solve(self, ctx: commands.Context, flag: str) -> None:
        """
        Closes and solves the current challenge.

        Parameters
        ----------
        flag: str
            The flag to submit for the challenge.
        """
        raise NotImplementedError()

    @ctf.command()
    async def delete(self, ctx: commands.Context) -> None:
        """
        Deletes the current CTF channel, forums and platform resources.
        """
        raise NotImplementedError()

    @ctf.command()
    async def archive(self, ctx: commands.Context) -> None:
        """
        Archives the current CTF channel and forum and logs out of sessions.
        """
        raise NotImplementedError()

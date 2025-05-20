from redbot.core import commands
from typing_extensions import Literal, Optional, overload

from .BaseAPI import BaseAPI

OptStr = Optional[str]


class Platform(commands.Cog, name="ctfcogs.Platform"):
    """A cog that manages interaction with CTF Platforms"""

    APIS: list[type[BaseAPI]] = []

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @commands.group()
    async def platform(self, ctx: commands.Context):
        """
        Manage CTF Platforms

        | Commands automatically identify the platform type if not already done.
        | It will also attempt to login if no session is found.
        | Credentials are bound and retrived by key=(url, channel).
        | Sessions are bound and retrived by key=(url, channel).
        """
        pass

    @platform.command()
    async def list(self, ctx: commands.Context) -> None:
        """
        List all available platforms
        """
        raise NotImplementedError()

    @platform.command()
    async def identify(self, ctx: commands.Context, url: str) -> None:
        """
        Identify and save the platform type of a given URL

        Parameters
        ----------
        url: str
            The URL to identify the platform for
        """
        raise NotImplementedError()

    @platform.command()
    async def url(self, ctx: commands.Context, url: str) -> None:
        """
        Identify and set the default URL of the platform for the current channel

        Parameters
        ----------
        url: str
            The URL to save
        """
        raise NotImplementedError()

    @overload
    async def creds(
        self, ctx: commands.Context, *, uname: str, pwd: str, url: OptStr = None
    ) -> None: ...

    @overload
    async def creds(self, ctx: commands.Context, *, token: str, url: OptStr = None) -> None: ...

    @platform.command()
    async def creds(
        self,
        ctx: commands.Context,
        *,
        uname: OptStr = None,
        pwd: OptStr = None,
        token: OptStr = None,
        url: OptStr = None,
    ) -> None:
        """
        Save credentials for a given platform

        Parameters
        ----------
        uname: str
            The username to save
        pwd: str
            The password to save
        token: str
            The token to save
        url: str, optional
            The URL of the platform to save credentials for
        """
        raise NotImplementedError()

    @overload
    async def login(
        self, ctx: commands.Context, *, uname: str, pwd: str, url: OptStr = None
    ) -> None: ...

    @overload
    async def login(self, ctx: commands.Context, *, token: str, url: OptStr = None) -> None: ...

    @overload
    async def login(self, ctx: commands.Context, *, url: OptStr = None) -> None: ...

    @platform.command()
    async def login(
        self,
        ctx: commands.Context,
        *,
        uname: OptStr = None,
        pwd: OptStr = None,
        token: OptStr = None,
        url: OptStr = None,
    ) -> None:
        """
        Login to the platform and save the session

        If parameters are misssing, saved credentials will be used

        Parameters
        ----------
        uname: str
            The username to login with
        pwd: str
            The password to login with
        token: str
            The token to login with
        url: str, optional
            The URL of the platform to login to
        """
        raise NotImplementedError()

    @platform.command()
    async def logout(self, ctx: commands.Context, *, url: OptStr = None) -> None:
        """
        Logout of the platform and delete the session

        Parameters
        ----------
        url: str, optional
            The URL of the platform to logout of
        """
        raise NotImplementedError()

    @platform.command()
    async def delete(self, ctx: commands.Context, *, url: OptStr = None) -> None:
        """
        Delete the platform and all associated data

        Parameters
        ----------
        url: str, optional
            The URL of the platform to delete
        """
        raise NotImplementedError()

    @platform.command()
    async def challenges(
        self,
        ctx: commands.Context,
        show: Literal["all", "solved", "unsolved"] = "unsolved",
        sort: Literal["asc", "desc", "none"] = "desc",
        sortby: Literal["name", "points", "solves"] = "solves",
        *,
        url: OptStr = None,
    ) -> None:
        r"""
        List and save challenges for a given platform

        Challenge data is saved by the same key as the session

        Parameters
        ----------
        show: {'all', 'solved', 'unsolved'}, default='unsolved'
            Specifies which challenges to display:
            - 'all': Show all challenges.
            - 'solved': Show only solved challenges.
            - 'unsolved': Show only unsolved challenges.

        sort: {'asc', 'desc'}, default='desc'
            Determines the sort order of the challenges:
            - 'asc': Sort in ascending order.
            - 'desc': Sort in descending order.
            - 'none': No sorting applied.

        sortby: {'name', 'points', 'solves'}, default='solves'
            Not used if sort='none'

            Field to sort the challenges by:
            - 'name': Sort by challenge name.
            - 'points': Sort by challenge points.
            - 'solves': Sort by number of solves.

        url: str, optional
            The URL of the platform to list challenges for.
        """
        # do not overwrite the flag field
        raise NotImplementedError()

    @platform.command()
    async def solve(
        self,
        ctx: commands.Context,
        id: str,
        flag: str,
        *,
        url: OptStr = None,
    ) -> None:
        """
        Submit a flag for a given challenge

        Challenges are retrived if not already saved

        Parameters
        ----------
        id: str
            The ID of the challenge to solve.

        flag: str
            The flag to submit for the challenge.

        url: str, optional
            The URL of the platform to submit the flag to.
        """
        raise NotImplementedError()

    @platform.command()
    async def submit(self, ctx: commands.Context, *, url: OptStr = None) -> None:
        """
        Submit any saved flags for a given platform

        This command is only usedful if hoarding flags

        Parameters
        ----------
        url: str, optional
            The URL of the platform to submit the flag to.
        """
        raise NotImplementedError()

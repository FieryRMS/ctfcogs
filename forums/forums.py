from discord import Member, Role
from redbot.core import commands


class Forums(commands.Cog, name="ctfcogs.Forums"):
    """A cog for creating and managing CTF channels and forums."""

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @commands.group()
    async def forums(self, ctx: commands.Context):
        """Manage CTF forums and channels."""
        pass

    @forums.command()
    async def create(self, ctx: commands.Context, contest: str) -> None:
        """
        Create a new CTF channel and forum.

        Parameters
        ----------
        contest: str
            The name of the contest to create a channel and forum for.
        """
        raise NotImplementedError()

    @forums.command()
    async def archive(self, ctx: commands.Context) -> None:
        """
        Archive the current CTF channel and forum.
        This command should be run in the channel that you want to archive.
        """
        raise NotImplementedError()

    @forums.command()
    async def add(self, ctx: commands.Context, chall: str) -> None:
        """
        Add a challenge to the current CTF.
        This command should be run in the general channel of the CTF.

        Parameters
        ----------
        chall: str
            The name of the challenge to add to the channel and forum.
        """
        raise NotImplementedError()

    @forums.command()
    async def solve(self, ctx: commands.Context) -> None:
        """
        Mark the current challenge as solved.
        This command should be run in the channel of the challenge.
        """
        raise NotImplementedError()

    @forums.command()
    async def delete(
        self,
        ctx: commands.Context,
    ) -> None:
        """
        Delete the current challenge. If run in the general channel, it will delete the entire CTF.
        This command should be run in the channel that you want to delete.
        """
        raise NotImplementedError()

    @forums.command()
    async def join(self, ctx: commands.Context, entity: Member | Role) -> None:
        """
        Add member(s) to a CTF channel or forum.
        This command should be run in the channel that you want to add members to.

        Parameters
        ----------
        entity: Member | Role
            The entity to join. This can be a member or a role.
        """
        raise NotImplementedError()

    @forums.command()
    async def leave(self, ctx: commands.Context, entity: Member | Role | None = None) -> None:
        """
        Leave a CTF channel or forum.
        This command should be run in the general channel of the CTF.

        Parameters
        ----------
        entity: Entity
            The entity to leave. This can be a member or a role. Defaults to the current user.
        """
        raise NotImplementedError()

    @forums.command()
    async def where(self, ctx: commands.Context, chall: str) -> None:
        """
        Get the channel of a challenge.
        This command should be run in the general channel of the CTF.

        Parameters
        ----------
        chall: str
            The name of the challenge to get the channel for.
        """
        raise NotImplementedError()

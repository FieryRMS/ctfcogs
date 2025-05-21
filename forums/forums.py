import discord
from discord import Guild, Member, Role
from pydantic import BaseModel
from redbot.core import Config, commands
from typing_extensions import Literal


class ForumGuildConfig(BaseModel):
    ctf_divider: str = "============= CTF ============="
    archive_divider: str = "=========== ARCHIVE ==========="
    ctf_divider_id: int | None = None
    archive_divider_id: int | None = None
    use_only_threads: bool = False


class Forums(commands.Cog, name="ctfcogs.Forums"):
    """A cog for creating and managing CTF channels and forums."""

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(self, 614565206, force_registration=True)
        self.config.register_guild(**ForumGuildConfig().model_dump())

    @commands.guild_only()
    @commands.hybrid_group()
    async def forums(self, ctx: commands.Context):
        """Manage CTF forums and channels."""
        pass

    async def get_divider(self, guild: Guild, divider: Literal["ctf", "archive"]):
        """
        Get the divider for the given type. Will create the divider if it doesn't exist.

        Parameters
        ----------
        divider: {"ctf", "archive"}
            The type of divider to get.
        """
        id = await self.config.guild(guild).get_attr(f"{divider}_divider_id")()

        if id is None or (category := guild.get_channel(id)) is None:
            position = discord.utils.MISSING

            if divider == "ctf":
                archive_divider = await self.get_divider(guild, "archive")
                position = archive_divider.position - 1

            name = await self.config.guild(guild).get_attr(f"{divider}_divider")()
            category = await guild.create_category(name=name, position=position)
            await self.config.guild(guild).get_attr(f"{divider}_divider_id").set(category.id)

        return category

    async def create_ctf(self, guild: Guild, contest: str):
        """
        Create the forums for the given contest.

        Parameters
        ----------
        contest: str
            The name of the contest to create forums for.
        """
        ctf_divider = await self.get_divider(guild, "ctf")
        category = await guild.create_category(name=contest, position=ctf_divider.position)
        general = await category.create_text_channel(name="general")

        use_only_threads = await self.config.guild(guild).use_only_threads()
        if use_only_threads or "COMMUNITY" not in guild.features:
            return category, general, None

        forum = await category.create_forum(name="discussion", position=general.position)

        return category, general, forum

    @forums.command()
    async def new(self, ctx: commands.GuildContext, contest: str) -> None:
        """
        Create a new CTF channel and forum.

        Parameters
        ----------
        contest: str
            The name of the contest to create a channel and forum for.
        """
        await self.create_ctf(ctx.guild, contest)
        if ctx.interaction:
            await ctx.send(f"Created CTF channel and forum for {contest}.", ephemeral=True)
        else:
            await ctx.message.add_reaction("✅")

    @forums.command()
    async def archive(self, ctx: commands.GuildContext) -> None:
        """
        Archive the current CTF channel and forum.
        This command should be run in the channel that you want to archive.
        """
        raise NotImplementedError()

    @forums.command()
    async def add(self, ctx: commands.GuildContext, chall: str) -> None:
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
    async def solve(self, ctx: commands.GuildContext) -> None:
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
    async def join(self, ctx: commands.GuildContext, entity: Member | Role) -> None:
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
    async def leave(self, ctx: commands.GuildContext, entity: Member | Role | None = None) -> None:
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
    async def where(self, ctx: commands.GuildContext, chall: str) -> None:
        """
        Get the channel of a challenge.
        This command should be run in the general channel of the CTF.

        Parameters
        ----------
        chall: str
            The name of the challenge to get the channel for.
        """
        raise NotImplementedError()

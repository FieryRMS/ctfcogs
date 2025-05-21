import asyncio

import discord
from discord import Guild, Interaction, Member, Role
from discord.ui import Button, View
from pydantic import BaseModel
from redbot.core import Config, commands
from typing_extensions import Literal


class ForumGuildConfig(BaseModel):
    ctf_divider: str = "============= CTF ============="
    archive_divider: str = "=========== ARCHIVE ==========="
    ctf_divider_id: int | None = None
    archive_divider_id: int | None = None
    use_only_threads: bool = False


class ForumChannelConfig(BaseModel):
    is_ctf: bool = False
    category_id: int | None = None
    general_id: int | None = None
    forum_id: int | None = None
    is_thread: bool = False


class Forum(commands.Cog, name="ctfcogs.Forum"):
    """A cog for creating and managing CTF channels and forums."""

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(self, 614565206, force_registration=True)
        self.config.register_guild(**ForumGuildConfig().model_dump())
        self.config.register_channel(**ForumChannelConfig().model_dump())

    @commands.guild_only()
    @commands.hybrid_group()
    async def forum(self, ctx: commands.Context):
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
        id: int | None = await self.config.guild(guild).get_attr(f"{divider}_divider_id")()

        if id is None or (category := guild.get_channel(id)) is None:
            position = discord.utils.MISSING

            if divider == "ctf":
                archive_divider = await self.get_divider(guild, "archive")
                position = archive_divider.position - 1

            name: str = await self.config.guild(guild).get_attr(f"{divider}_divider")()
            category = await guild.create_category(name=name, position=position)
            await self.config.guild(guild).set_raw(f"{divider}_divider_id", value=category.id)

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

        forum = None
        if not use_only_threads and "COMMUNITY" in guild.features:
            forum = await category.create_forum(name="discussion", position=general.position)

        config = ForumChannelConfig(
            is_ctf=True,
            category_id=category.id,
            general_id=general.id,
            forum_id=forum.id if forum else None,
            is_thread=forum is None,
        ).model_dump()

        await asyncio.gather(
            *[
                self.config.channel(channel).set(config)
                for channel in (category, general, forum)
                if channel is not None
            ]
        )

        return category, general, forum

    @forum.command()
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

    @forum.command()
    async def archive(self, ctx: commands.GuildContext) -> None:
        """
        Archive the current CTF channel and forum.
        This command should be run in the channel that you want to archive.
        """
        raise NotImplementedError()

    @forum.command()
    async def add(self, ctx: commands.GuildContext, chall: str) -> None:
        """
        Add a challenge to the current CTF.
        This command should be run in the general channel of the CTF.

        Parameters
        ----------
        chall: str
            The name of the challenge to add to the CTF forums.
        """
        raise NotImplementedError()

    @forum.command()
    async def solve(self, ctx: commands.GuildContext) -> None:
        """
        Mark the current challenge as solved.
        This command should be run in the channel of the challenge.
        """
        raise NotImplementedError()

    async def delete_channel_id(self, id: int):
        """
        Delete a channel by its ID.

        Parameters
        ----------
        id: int
            The ID of the channel to delete.
        """
        channel = self.bot.get_channel(id)
        if channel and not isinstance(channel, discord.abc.PrivateChannel):
            await channel.delete()
        await self.config.channel_from_id(id).clear()

    async def delete_ctf(self, config: ForumChannelConfig):
        """
        Delete all the category, channels, forums that is part of the CTF.

        Parameters
        ----------
        channel: discord.abc.GuildChannel
            The channel of the CTF to delete.
        """

        if config.is_ctf:
            asyncio.gather(
                *[
                    self.delete_channel_id(id)
                    for id in (config.category_id, config.general_id, config.forum_id)
                    if id is not None
                ]
            )

    @forum.command()
    async def delete(
        self,
        ctx: commands.GuildContext,
    ) -> None:
        """
        Delete the current challenge. If run in the general channel, it will delete the entire CTF.
        This command should be run in the channel that you want to delete.
        """

        config = ForumChannelConfig.model_validate(await self.config.channel(ctx.channel).all())

        if not config.is_ctf:
            await ctx.send("This command can only be run in a CTF channel.", ephemeral=True)
            return

        if config.general_id != ctx.channel.id:
            await ctx.send(
                "This command can only be run in the general channel of the CTF.", ephemeral=True
            )
            return

        async def yes_callback(interaction: Interaction):
            nonlocal self, config
            await self.delete_ctf(config)

            await interaction.response.edit_message(
                content="CTF deleted.",
                view=None,
            )

        async def no_callback(interaction: Interaction):
            await interaction.response.edit_message(
                content="CTF not deleted.",
                view=None,
            )

        Yes: Button[View] = Button(
            label="Yes",
            style=discord.ButtonStyle.danger,
        )
        No: Button[View] = Button(
            label="No",
            style=discord.ButtonStyle.success,
        )

        Yes.callback = yes_callback
        No.callback = no_callback
        view = discord.ui.View(timeout=10)
        view.add_item(Yes)
        view.add_item(No)
        await ctx.send(
            "Are you sure you want to delete this CTF? This action cannot be undone.",
            view=view,
            ephemeral=True,
        )

    @forum.command()
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

    @forum.command()
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

    @forum.command()
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

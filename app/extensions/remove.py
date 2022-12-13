import hikari
import lightbulb
import asyncio
from app import *



@lightbulb.command(
    "remove",
    "Use this command to remove (\"auto_translation\", \"role_translation\")"
)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def removing(ctx: lightbulb.Context): 
    await ctx.respond("...")



@removing.child
@lightbulb.add_cooldown(50, 1, lightbulb.GuildBucket)
@lightbulb.add_checks(
    blacklist_check,
    guild_blacklist_check,
    lightbulb.guild_only,
    lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
)
@lightbulb.command(
    "all",
    "Use this command to remove all the (\"auto_translation\", \"role_translation\")"
)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def all(ctx: lightbulb.Context):
    if not auto_translation_base.find_one({"guild_id": f"{ctx.guild_id}"}) and not role_translation_base.find_one({"guild_id": f"{ctx.guild_id}"}):
        return await ctx.respond("There is nothing to remove")
    
    auto_translation_base.delete_many({"guild_id": f"{ctx.guild_id}"})
    role_translation_base.delete_many({"guild_id": f"{ctx.guild_id}"})
    await ctx.respond("All roles and channels are removed!")



@removing.child
@lightbulb.add_cooldown(50, 1, lightbulb.GuildBucket)
@lightbulb.add_checks(
    blacklist_check,
    guild_blacklist_check,
    lightbulb.guild_only,
    lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
)
@lightbulb.option(
    "channel",
    "Choose the channel that you want to remove it",
    hikari.GuildChannel
)
@lightbulb.command(
    "auto_translation",
    "Use this command to remove the (\"auto_translation\")"
)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def auto_translation(ctx: lightbulb.Context):
    channel = await ctx.bot.rest.fetch_channel(ctx.options.channel)

    if not auto_translation_base.find_one({"channel_id": f"{channel.id}"}):
        return await ctx.respond("This channel is not an auto translation channel")
    
    auto_translation_base.delete_one({"channel_id": f"{channel.id}"})
    await ctx.respond("Channel removed!")



@removing.child
@lightbulb.add_cooldown(50, 1, lightbulb.GuildBucket)
@lightbulb.add_checks(
    blacklist_check,
    guild_blacklist_check,
    lightbulb.guild_only,
    lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
)
@lightbulb.option(
    "role",
    "Choose the role that you want to remove it",
    hikari.Role
)
@lightbulb.command(
    "role_translation",
    "Use this command to remove the (\"role_translation\")"
)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def role_translation(ctx: lightbulb.Context):
    role = ctx.get_guild().get_role(ctx.options.role)

    if not role_translation_base.find_one({"role_id": f"{role.id}"}):
        return await ctx.respond("This role is not a role translation")
    
    role_translation_base.delete_one({"role_id": f"{role.id}"})
    await ctx.respond("Role removed!")


def load(bot: Bot):
    bot.command(removing)
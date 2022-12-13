import hikari
import lightbulb
from app import *



@lightbulb.command(
    "set",
    "Use this command to set (\"auto_translation\", \"role_translation\")"
)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def setting(ctx: lightbulb.Context): 
    await ctx.respond("...")



@setting.child
@lightbulb.add_cooldown(50, 1, lightbulb.GuildBucket)
@lightbulb.add_checks(
    blacklist_check,
    guild_blacklist_check,
    lightbulb.guild_only,
    lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
)
@lightbulb.option(
    "language2",
    "Type the second language if you want to set a multi translation channel",
    required=False
)
@lightbulb.option(
    "language",
    "Type the language(s) code that you want to use (with comma between)"
)
@lightbulb.option(
    "channel",
    "Pick a channel to set it for auto translation",
    hikari.GuildChannel
)
@lightbulb.command(
    "auto_translation",
    "Use this command to set a channel for auto translation"
)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def auto_translation(ctx: lightbulb.Context):
    channel = await ctx.bot.rest.fetch_channel(ctx.options.channel)

    if (server_settings := settings.find_one({"guild": f"{ctx.guild_id}"})) is None:
        data = {
            "guild": f"{ctx.guild_id}",
            "engine": DEFAULT_ENGINE
        }
        settings.insert_one(data)

    if isinstance(channel, hikari.GuildVoiceChannel):
        return await ctx.respond(f"You cannot set a voice channel as an auto translation channel", flags=hikari.MessageFlag.EPHEMERAL)
    if isinstance(channel, hikari.GuildCategory):
        return await ctx.respond(f"You cannot set a category as an auto translation channel", flags=hikari.MessageFlag.EPHEMERAL)

    if not ctx.options.language2:
        data = {
            "what": "auto_translation",
            "guild_id": f"{ctx.guild_id}",
            "channel_id": f"{channel.id}"
        }

        for num, lang in enumerate(ctx.options.language.split(",")):
            data[f"lang{num+1}"] = f"{lang}"

        if auto_translation_base.find_one({"channel_id": f"{channel.id}"}):
            return await ctx.respond(f"<#{channel.id}>, It is already an auto translation channel", flags=hikari.MessageFlag.EPHEMERAL)
        auto_translation_base.insert_one(data)
    else:
        data = {
            "what": "multi_translation",
            "guild_id": f"{ctx.guild_id}",
            "channel_id": f"{channel.id}"
        }

        if (len(ctx.options.language.split(",")) or len(ctx.options.language2.split(","))) > 1:
            return await ctx.respond("You can't set more than 2 languages for multi translation", flags=hikari.MessageFlag.EPHEMERAL)
        
        data["lang1"], data["lang2"] = f"{ctx.options.language}", f"{ctx.options.language2}"

        if auto_translation_base.find_one({'channel_id': f'{channel.id}'}):
            return await ctx.respond(f"<#{channel.id}>, It is already an multi translation channel", flags=hikari.MessageFlag.EPHEMERAL)
        auto_translation_base.insert_one(data)
    await ctx.respond(f"<#{channel.id}>, It is now an auto translation channel")



@setting.child
@lightbulb.add_cooldown(50, 1, lightbulb.GuildBucket)
@lightbulb.add_checks(
    blacklist_check,
    guild_blacklist_check,
    lightbulb.guild_only,
    lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
)
@lightbulb.option(
    "language",
    "Type the language code that you want to use"
)
@lightbulb.option(
    "role",
    "Pick a role to set it for auto translation",
    hikari.Role
)
@lightbulb.command(
    "role_translation",
    "Use this command to set a channel for auto translation"
)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def role_translation(ctx: lightbulb.Context):
    role = ctx.get_guild().get_role(ctx.options.role)

    if len(langs := ctx.options.language.split(",")) > 1:
        return await ctx.respond("You can one language only", flags=hikari.MessageFlag.EPHEMERAL)

    data = {
        "guild_id": f"{ctx.guild_id}",
        "role_id": f"{role.id}",
        "lang": f"{ctx.options.language}"
    }

    if role_lang := role_translation_base.find_one({'role_id': f'{role.id}'}):
        return await ctx.respond(f"{role.mention}, It is already with (`{role_lang['lang']}`) language", flags=hikari.MessageFlag.EPHEMERAL)
    role_translation_base.insert_one(data)

    await ctx.respond(f"`{role.name}`, It is now a role translation")



@setting.child
@lightbulb.add_cooldown(50, 1, lightbulb.GuildBucket)
@lightbulb.add_checks(
    blacklist_check,
    guild_blacklist_check,
    lightbulb.guild_only,
    lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
)
@lightbulb.option(
    "engine",
    "Use the translate engine that you want to use",
    choices=[
        "googletranslate",
        "libretranslate"
    ]
)
@lightbulb.command(
    "engine",
    "Use this command to change the translate engine"
)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def engine(ctx: lightbulb.Context):
    data = {
        "guild": f"{ctx.get_guild().id}",
        "engine": ctx.options.engine
    }
    
    if guild_engine := settings.find_one({"guild": f"{data['guild']}"}):
        if guild_engine["engine"] == ctx.options.engine:
            return await ctx.respond("This is your current engine for this server!")
        else:
            settings.find_one_and_update({"guild": f"{data['guild']}"}, {"$set": data})
            return await ctx.respond(f"Engine updated to `{data['engine']}`!")
    else:
        settings.insert_one(data)
        return await ctx.respond(f"`{data['engine']}`, Your new egnine!")


def load(bot: Bot):
    bot.command(setting)
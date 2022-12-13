import hikari
import lightbulb
from app import *



@lightbulb.add_cooldown(50, 1, lightbulb.UserBucket)
@lightbulb.add_checks(
    blacklist_check,
    guild_blacklist_check,
    lightbulb.guild_only
)
@lightbulb.command(
    "languages",
    "Use this command to show the languages and their codes"
)
@lightbulb.implements(lightbulb.SlashCommand)
async def languages(ctx: lightbulb.Context):
    server_settings = settings.find_one({"guild": f"{ctx.get_guild().id}"})
    message = ""
    if server_settings["engine"] == "libretranslate":
        for i in get_languages(server_settings["engine"]):
            message += f"`{i['code']}` : {i['name']}\n"
    elif server_settings["engine"] == "googletranslate":
        langs = get_languages(server_settings["engine"])
        values = [lang for lang in langs.values()]
        keys = [lang for lang in langs.keys()]
        for i, value in enumerate(values):
            message += f"`{value}` : {keys[i].title()}\n"
    embed = hikari.Embed(color=0x2C3434, description=message)
    return await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


def load(bot: Bot):
    bot.command(languages)
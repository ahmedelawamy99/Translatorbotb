import hikari
import lightbulb
from app import *


on_command_error = lightbulb.Plugin("on_command_error")


@on_command_error.listener(lightbulb.SlashCommandErrorEvent)
async def error_handler(event: lightbulb.SlashCommandErrorEvent):
    
    try:
        if (server_settings := settings.find_one({"guild": f"{event.context.guild_id}"})) is None:
            data = {
                "guild": f"{event.context.guild_id}",
                "engine": DEFAULT_ENGINE
            } # return await event.context.respond("You have no engine been setten! Use `/set engine`")
        languages = get_languages(server_settings["engine"])
        if server_settings["engine"] == "libretranslate":
            languages = [lang["code"] for lang in languages]
        elif server_settings["engine"] == "googletranslate":
            languages = [lang for lang in languages.values()]

        if isinstance(event.exception, lightbulb.CommandIsOnCooldown):
            after = event.exception.retry_after
            after *= 100
            after //= 1
            after /= 100
            return await event.context.respond(f"You are on cooldown (`{after}s`)")
        elif isinstance(event.exception, lightbulb.errors.MissingRequiredPermission):
            return await event.context.respond(f"You need this permission(s) to run this command ({event.exception.missing_perms})")
        elif isinstance(event.exception, lightbulb.OnlyInGuild):
            return
        elif isinstance(event.exception, lightbulb.errors.CommandInvocationError):
            if isinstance(event.exception.original, hikari.ForbiddenError):
                if event.exception.original.code == 50_007:
                    await event.context.respond("Your DM is closed")
                elif event.exception.original.code == 50_001:
                    await event.context.respond("I have no access to this channel")
                elif event.exception.original.code == 50_013:
                    pass
    
        if event.context.options.language:
            if len(langs := event.context.options.language.split(",")) > 1:
                if len(langs) > 3:
                    return await event.context.respond("You cannot add more than 3 languages")
                for lang in langs:
                    if lang not in languages:
                        return await event.context.respond(f"I have no language with this code: (`{lang}`)", flags=hikari.MessageFlag.EPHEMERAL)
            elif event.context.options.language not in languages:
                return await event.context.respond(f"I have no language with this code: (`{event.context.options.language}`)", flags=hikari.MessageFlag.EPHEMERAL)
            # elif event.context.options.language2 not in languages:
            #     return await event.context.respond(f"I have no language with this code: (`{event.context.options.language}`)", flags=hikari.MessageFlag.EPHEMERAL)
    except Exception as e:
        except_error(e)


def load(bot: Bot):
    bot.add_plugin(on_command_error)
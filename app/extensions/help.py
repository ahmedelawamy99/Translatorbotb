import hikari
import lightbulb
from app import *



@lightbulb.add_cooldown(10, 1, lightbulb.UserBucket)
@lightbulb.add_checks(
    blacklist_check,
    guild_blacklist_check,
    lightbulb.guild_only
)
# @lightbulb.option(
#     "command",
#     "Command to get help for",
#     required=False
# )
@lightbulb.command(
    "help",
    f"Get help information about me"
)
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx: lightbulb.Context):
    message = ""
    # if not ctx.options.command:
    #     message = "**Slash commands:**\n"
    #     for ext in ctx.bot.slash_commands:
    #         command = ctx.bot.get_slash_command(ext)
    #         message += f"\t**`{command.name}`**: {command.description}\n"
    #     embed = hikari.Embed(color=0x2C3434, description=message)
    #     embed.set_footer("Use: /help [command] to get more information")
    # elif ctx.options.command not in ctx.bot.slash_commands:
    #     return await ctx.respond("There is no command with that name", flags=hikari.MessageFlag.EPHEMERAL)
    # else:
    #     command = ctx.bot.get_slash_command(ctx.options.command.lower())
    #     message = f"**Command: `{command.name}`**\n**Description:**\n\t{command.description}\n**Usage:**\n\t/{command.name} "
    #     for option in command.options:
    #         message += f"[{option}] "
    #     embed = hikari.Embed(color=0x2C3434, description=message)
    # embed.set_author(name=ctx.bot.get_me().username, icon=ctx.bot.get_me().avatar_url, url="https://discord.gg/XKH8BkZJXN")
    # await ctx.respond(embed)

    await ctx.respond(hikari.Embed(color=0x2C3434, description="https://discord.gg/XKH8BkZJXN"), flags=hikari.MessageFlag.EPHEMERAL)


def load(bot: Bot):
    bot.command(help)
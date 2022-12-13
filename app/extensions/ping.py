import lightbulb
from datetime import datetime as dt
from app import *



@lightbulb.add_cooldown(10, 1, lightbulb.ChannelBucket)
@lightbulb.add_checks(
    blacklist_check,
    guild_blacklist_check,
    lightbulb.guild_only
)
@lightbulb.command(
    "ping",
    "Shows bot\'s latency"
)
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context):
    start = dt.timestamp(dt.now())
    await ctx.respond("...")
    await ctx.edit_last_response(
        f"> Discord API: (`{ctx.bot.heartbeat_latency * 1_000:,.0f}`ms)\n> Latency: (`{round((dt.timestamp(dt.now()) - start) * 1_000)}`ms)"
    )


def load(bot: Bot):
    bot.command(ping)
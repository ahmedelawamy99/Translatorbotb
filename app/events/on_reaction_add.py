import hikari
import lightbulb
from countryinfo import CountryInfo
import pycountry
from app import *



on_reaction_add = lightbulb.Plugin('on_reaction_add')



@on_reaction_add.listener(hikari.ReactionAddEvent)
async def reaction_add(event: hikari.ReactionAddEvent):
    try:
        if not (coun := pycountry.countries.get(flag=event.emoji_name)):
            return
        else:
            lang = CountryInfo(coun.alpha_2).info()['languages'][0]
            lang = "zh-CN" if lang == "zh" else lang
            if lang not in (langs := get_languages_with_names("googletranslate")).keys():
                return
            else:
                msg: hikari.Message = await event.app.rest.fetch_message(event.channel_id, event.message_id)
                text = get_translate("googletranslate", msg.content, lang)
                translated_text = f"**{text}**\n"
                languages = [f"{langs[lang].title()} ({lang})"]

                embed = msg_layout(
                    translated_text,
                    event.member.get_top_role().color,
                    event.member.display_name,
                    event.member.default_avatar_url if not event.member.avatar_url else event.member.avatar_url,
                    languages
                )

                await msg.respond(embed, reply=True)
    except Exception as e:
        except_error(e)


def load(bot: Bot):
    bot.add_plugin(on_reaction_add)

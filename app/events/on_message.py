import hikari
import lightbulb
import emoji
import re
from app import *



on_message = lightbulb.Plugin("on_message")



@on_message.listener(hikari.MessageCreateEvent)
async def message_handler(event: hikari.MessageCreateEvent):
    if event.message.author.is_bot or isinstance(await event.message.fetch_channel(), hikari.DMChannel):
        return
    if blacklist.find_one({"guild_id": f"{event.message.guild_id}"}) or blacklist.find_one({"user_id": f"{event.author_id}"}):
        return
    if settings.find_one({"guild": f"{event.message.guild_id}"}) is None:
        data = {
            "guild": f"{event.message.guild_id}",
            "engine": DEFAULT_ENGINE
        }
        
        settings.insert_one(data)
    server_settings = settings.find_one({"guild": f"{event.message.guild_id}"})
    

    try:
        if channel := auto_translation_base.find_one({"channel_id": f"{event.channel_id}"}):

            replaced_text   = event.content
            text_language   = get_language(server_settings["engine"], replaced_text) # ["language"]
            channel_langs   = len(channel) - 3
            translated_text = ""

            if channel_langs == 2 and text_language == channel["lang1"]:
                return

            if channel["what"] == "multi_translation" and text_language not in (channel["lang1"], channel["lang2"]):
                return
            if channel["what"] == "multi_translation" and text_language in (channel["lang1"], channel["lang2"]):
                to_lang = channel["lang2"] if text_language == channel["lang1"] else channel["lang1"]
                if server_settings["engine"] == "libretranslate" and to_lang in ("zh-CN", "zh-TW"):
                    to_lang = "zh"
                elif server_settings["engine"] == "googletranslate" and to_lang == "zh":
                    to_lang = "zh-CN"

            mention_check    = r"<(#|@|@&|@!)[0-9]+>"
            emoji_check      = r"<a?:\w+:\w+>"
            url_check        = r"https?:\/\/(\w\.)*\w+\.\w+\/[a-zA-Z0-9_\.\/\+=%\$&#@!\?\-]*"
            re_mention_check = r"(<(#|@|@&|@!)[0-9]+>)+"
            re_emoji_check   = r"(<a?:\w+:\w+>)+"
            re_url_check     = r"(https?:\/\/(\w\.)*\w+\.\w+\/[a-zA-Z0-9_\.\/\+=%\$&#@!\?\-]*)+"
            mention_checker  = True
            emoji_checker    = True
            url_checker      = True

            if re.fullmatch(re_mention_check, replaced_text) or re.fullmatch(re_emoji_check, replaced_text) or re.fullmatch(re_url_check, replaced_text):
                return
            
            replaced_text = emoji.replace_emoji(replaced_text, "")
            
            while mention_checker:
                mention_found = re.search(mention_check, replaced_text)
                if mention_found:
                    this = replaced_text.split(mention_found.group())
                    replaced_text = "".join(this)
                else:
                    mention_checker = False
            
            while emoji_checker:
                emoji_found = re.search(emoji_check, replaced_text)
                if emoji_found:
                    this = replaced_text.split(emoji_found.group())
                    replaced_text = "".join(this)
                else:
                    emoji_checker = False
            
            while url_checker:
                url_found = re.search(url_check, replaced_text)
                if url_found:
                    this = replaced_text.split(url_found.group())
                    replaced_text = "".join(this)
                else:
                    url_checker = False

            if len(replaced_text.strip()) == 0:
                return
            
            langs = []
            if channel["what"] == "auto_translation":
                for num in range(1, channel_langs):
                    if channel[f"lang{num}"] != text_language:
                        text = get_translate(server_settings["engine"], replaced_text, channel[f"lang{num}"])
                        translated_text += f"> **{channel[f'lang{num}']}** ↴\n**{text}**\n"
                        langs.append(f"{get_languages_with_names(server_settings['engine'])[channel[f'lang{num}']].title()} ({channel[f'lang{num}']})")
            
            elif channel["what"] == "multi_translation":
                text = get_translate(server_settings["engine"], replaced_text, to_lang)
                translated_text = f"**{text}**\n"
                langs.append(f"{get_languages_with_names(server_settings['engine'])[to_lang].title()} ({to_lang})")
            embed = msg_layout(
                translated_text,
                event.message.member.get_top_role().color,
                event.message.member.display_name,
                event.message.member.default_avatar_url if event.message.member.avatar_url is None else event.message.member.avatar_url,
                langs
            )
            return await event.message.respond(embed=embed, reply=True)
        
        roles = [role for role in event.message.member.role_ids if role_translation_base.find_one({"role_id": f"{role}"})]
        message = ""
        roles_nums = 0
        for role in roles:
            if role := role_translation_base.find_one({"role_id": f"{role}"}):
                if roles_nums >= 3:
                    break

                replaced_text   = event.content
                text_language   = get_language(server_settings["engine"], replaced_text) # ["language"]
                translated_text = ""

                if text_language == role["lang"]:
                    continue

                mention_check    = r"<(#|@|@&|@!)[0-9]+>"
                emoji_check      = r"<a?:\w+:\w+>"
                url_check        = r"https?:\/\/(\w\.)*\w+\.\w+\/[a-zA-Z0-9_\.\/\+=%\$&#@!\?\-]*"
                re_mention_check = r"(<(#|@|@&|@!)[0-9]+>)+"
                re_emoji_check   = r"(<a?:\w+:\w+>)+"
                re_url_check     = r"(https?:\/\/(\w\.)*\w+\.\w+\/[a-zA-Z0-9_\.\/\+=%\$&#@!\?\-]*)+"
                mention_checker  = True
                emoji_checker    = True
                url_checker      = True

                if re.fullmatch(re_mention_check, replaced_text) or re.fullmatch(re_emoji_check, replaced_text) or re.fullmatch(re_url_check, replaced_text):
                    continue
                
                replaced_text = emoji.replace_emoji(replaced_text, "")
                
                while mention_checker:
                    mention_found = re.search(mention_check, replaced_text)
                    if mention_found:
                        this = replaced_text.split(mention_found.group())
                        replaced_text = "".join(this)
                    else:
                        mention_checker = False
                
                while emoji_checker:
                    emoji_found = re.search(emoji_check, replaced_text)
                    if emoji_found:
                        this = replaced_text.split(emoji_found.group())
                        replaced_text = "".join(this)
                    else:
                        emoji_checker = False
                
                while url_checker:
                    url_found = re.search(url_check, replaced_text)
                    if url_found:
                        this = replaced_text.split(url_found.group())
                        replaced_text = "".join(this)
                    else:
                        url_checker = False

                if len(replaced_text.strip()) == 0:
                    continue
                
                langs = []
                text = get_translate(server_settings["engine"], replaced_text, role["lang"])
                translated_text += f"**{text}**\n"
                langs.append(f"{get_languages_with_names(server_settings['engine'])[role['lang']].title()} ({role['lang']})")
                roles_nums += 1
        try:
            if len(translated_text) > 0:
                embed = msg_layout(
                    translated_text,
                    event.message.member.get_top_role().color,
                    event.message.member.display_name,
                    event.message.member.default_avatar_url if event.message.member.avatar_url is None else event.message.member.avatar_url,
                    langs
                )
                await event.message.respond(embed=embed)
        except: ...
    except Exception as e:
        except_error(e)


def load(bot: Bot):
    bot.add_plugin(on_message)

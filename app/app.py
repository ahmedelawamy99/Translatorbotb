import lightbulb
from hikari import Embed
from pymongo import MongoClient
import requests
from deep_translator import GoogleTranslator
from langid import classify
from traceback import extract_tb
from sys import exc_info
from os import environ


## ENV
TOKEN = environ["TOKEN"]
MONGO_CLIENT = environ["MONGO_CLIENT"]
##

client = MongoClient(MONGO_CLIENT)
db = client.get_database("transbase")
blacklist             = db.blacklist
auto_translation_base = db.auto_translation
role_translation_base = db.role_translation
settings              = db.settings
libretranslate        = db.libretranslate


DEFAULT_ENGINE = "googletranslate"
URL = libretranslate.find_one({"engine": "engine"})["url"]


def except_error(e):
    tb = exc_info()[-1]
    print(e)
    print(f"File Name: {__file__}")
    print(f"Error Line: {extract_tb(tb, limit=1)[-1][1]}")


@lightbulb.Check
def blacklist_check(ctx: lightbulb.Context):
    if blacklist.find_one({'user_id': f'{ctx.member.id}'}):
        return False
    else:
        return True


@lightbulb.Check
def guild_blacklist_check(ctx: lightbulb.Context):
    if blacklist.find_one({'guild_id': f'{ctx.guild_id}'}):
        return False
    else:
        return True


def get_translate(engine: str, q, target, source="auto"):
    try:
        if engine.strip().lower() == "libretranslate":
            params = {"q": q, "source": source, "target": target}
            req = requests.post(URL+"translate", params=params)
            data = req.json()
            return data["translatedText"]
        elif engine.strip().lower() == "googletranslate":
            req = GoogleTranslator(source=source, target=target).translate(q)
            return req
    except Exception as e:
        except_error(e)


def get_language(engine: str, q):
    try:
        if engine == "libretranslate":
            return classify(q)[0]
        if engine == "googletranslate":
            if (cl := classify(q)[0]) == "zh":
                return "zh-CN"
            return cl
    except Exception as e:
        except_error(e)


def get_languages(engine: str):
    try:
        if engine.strip().lower() == "libretranslate":
            params = dict()
            req = requests.get(URL+"languages", params=params)
            data = req.json()
            return data
        elif engine.strip().lower() == "googletranslate":
            req = GoogleTranslator().get_supported_languages(True)
            return req
    except Exception as e:
        except_error(e)


def get_languages_with_names(engine: str):
    languages = {}
    if engine.strip().lower() == "libretranslate":
        for i in get_languages(engine):
            languages[i["code"]] = i["name"]
    elif engine.strip().lower() == "googletranslate":
        langs = GoogleTranslator().get_supported_languages(True)
        values = [lang for lang in langs.values()]
        keys = [lang for lang in langs.keys()]
        for i, value in enumerate(values):
            languages[value] = keys[i]
    return languages


def msg_layout(msg, color, name, icon, langs):
    embed = Embed(color=color, description=msg)
    embed.set_author(name=name, icon=icon)
    embed.set_footer(f"Translated to [ {' , '.join(langs)} ]")
    return embed
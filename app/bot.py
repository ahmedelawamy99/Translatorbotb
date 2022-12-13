import hikari
from hikari.intents import Intents
import lightbulb
import logging
from os import listdir, environ
from .app import TOKEN



class Bot(lightbulb.BotApp):
    def __init__(self):
        self._extensions = [filename[:-3] for filename in listdir("./app/extensions") if filename.endswith(".py")]
        self._events = [filename[:-3] for filename in listdir("./app/events") if filename.endswith(".py")]

        super().__init__(
            TOKEN,
            intents=hikari.Intents.GUILDS | hikari.Intents.GUILD_MESSAGES | hikari.Intents.GUILD_MESSAGE_REACTIONS
        )
    
    def runbot(self):
        self.event_manager.subscribe(hikari.StartingEvent, self.starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.started)
        self.run()

    async def starting(self, event: hikari.StartingEvent):
        for ext in self._extensions:
            self.load_extensions(f"app.extensions.{ext}")
        for event in self._events:
            self.load_extensions(f"app.events.{event}")

    async def started(self, event: hikari.StartedEvent):
        await self.update_presence(
            activity=hikari.Activity(
                name="/help",
                type=hikari.ActivityType.PLAYING
            )
        )
        logging.info(f"I am in {self.get_me().username}")

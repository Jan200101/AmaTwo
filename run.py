# Rewriten from scratch to have the same behavior as AmaRewrite but be
# written from original code instead

from discord import utils, __version__ as dpy_version
from discord.ext import commands
from os import path, chdir
from json import load
from json.decoder import JSONDecodeError
from traceback import format_exception

from modules.utils.setup import Setup

dir_path = path.dirname(path.realpath(__file__))
chdir(dir_path)

print("Starting Amadeus on discord.py version {}".format(dpy_version))

try:
    with open("data/settings.json") as config:
        settings = load(config)
except (FileNotFoundError, JSONDecodeError):
    settings = Setup.settings()
token = settings['token']
prefix = settings['prefix']
description = settings['description']

try:
    with open("data/channels.json") as config:
        channels = load(config)
except (FileNotFoundError, JSONDecodeError):
    channels = Setup.channels()
log_id = channels['logs']
welcome_id = channels['welcome']

try:
    with open("data/roles.json") as config:
        role_list = load(config)
except (FileNotFoundError, JSONDecodeError):
    role_list = Setup.roles()
bot_role_id = role_list['bot']
bit_role_id = role_list['default']
mod_role_id = role_list['mod']
admin_role_id = role_list['admin']

try:
    open("data/wallets.json")
except FileNotFoundError:
    with open("data/wallets.json", "w") as config:
        config.write("{}")

bot = commands.Bot(command_prefix=prefix, description=description)


@bot.event
async def on_ready():
    modules = ['modules.fun', 'modules.logging',
               'modules.mod', 'modules.utility', ]

    failed_modules = []

    for module in modules:
        try:
            bot.load_extension(module)
            print("{} loaded".format(module))
        except Exception as error:
            print("Failed to load {}: {}".format(module, "".join(
                format_exception(type(error), error, error.__traceback__))))
            failed_modules.append((module, type(error).__name__, error))

    for guild in bot.guilds:
        try:
            bot.guild = guild

            # Temporary workaround because using the ID results in a "NoneType" error when trying to send to a channel
            bot.log_channel = utils.get(guild.channels, name="server-log-owo♥♥")
            bot.welcome_channel = utils.get(guild.channels, name="📝welcome-txt")

            # Temporary workaround because using the ID results in a "NoneType" error when trying to assign or check a role
            bot.bot_role = utils.get(guild.roles, name="Bot")
            bot.bit_role = utils.get(guild.roles, name="Bit")
            bot.mod_role = utils.get(guild.roles, name="Moderator")
            bot.admin_role = utils.get(guild.roles, name="Administrator")

            print('{0.user} is up and running on {1.name}!'.format(bot, guild))
        except Exception as e:
            print("Failed to start up properly on {} :(".format(guild.name))
            print("\t{}".format(e))

        applicationinfo = await bot.application_info()

        bot.creator = applicationinfo.owner

bot.run(token)

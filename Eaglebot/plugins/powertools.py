import os
from asyncio.exceptions import CancelledError
from time import sleep

from Eaglebot import eagle

from ..core.logger import logging
from ..core.managers import eor
from ..sql_helper.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID, HEROKU_APP

LOGS = logging.getLogger(__name__)
menu_category = "tools"


@eagle.eagle_cmd(
    pattern="restart$",
    command=("restart", menu_category),
    info={
        "header": "Restarts the bot !!",
        "usage": "{tr}restart",
    },
    disable_errors=True,
)
async def _(event):
    "Restarts the bot !!"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n" "Bot Restarted")
    await event.edit("Restarting **[ ░░░ ]** ...\nωαιτ ƒєω мιиυτє⚠️")
    await event.edit("Restarting **[ █░░ ]** ...\nωαιτ ƒєω мιиυτє☣️")
    await event.edit("Restarting **[ ██░ ]** ...\nωαιτ ƒєω мιиυτє☢️")
    await event.edit("Restarting **[ ███ ]** ...\nωαιτ ƒєω мιиυτєѕ☢️")
    EAGLE = await eor(
        event,
        "Restarted.\nAfter 2 min Type `.ping` me or `.help` to check if I am online, Actually I Am Going To Restart To Restart All System",
    )
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
    try:
        add_to_collectionlist("restart_update", [EAGLE.chat_id, EAGLE.id])
    except Exception as e:
        LOGS.error(e)
    try:
        await eagle.disconnect()
    except CancelledError:
        pass
    except Exception as e:
        LOGS.error(e)


@eagle.eagle_cmd(
    pattern="shutdown$",
    command=("shutdown", menu_category),
    info={
        "header": "Shutdowns the bot !!",
        "description": "To turn off the dyno of heroku. you cant turn on by bot you need to got to heroku and turn on or use @hk_heroku_bot",
        "usage": "{tr}shutdown",
    },
)
async def _(event):
    "Shutdowns the bot"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n" "Bot shut down")
    await eor(event, "`Turning off bot now ...Manually turn me on later`")
    if HEROKU_APP is not None:
        HEROKU_APP.process_formation()["worker"].scale(0)
    else:
        os._exit(143)


@eagle.eagle_cmd(
    pattern="sleep( [0-9]+)?$",
    command=("sleep", menu_category),
    info={
        "header": "Userbot will stop working for the mentioned time.",
        "usage": "{tr}sleep <seconds>",
        "examples": "{tr}sleep 60",
    },
)
async def _(event):
    "To sleep the Eaglebot"
    if " " not in event.pattern_match.group(1):
        return await eor(event, "Syntax: `.sleep time`")
    counter = int(event.pattern_match.group(1))
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "You put the bot to sleep for " + str(counter) + " seconds",
        )
    event = await eor(event, f"`ok, let me sleep for {counter} seconds`")
    sleep(counter)
    await event.edit("`OK, I'm awake now.`")


@eagle.eagle_cmd(
    pattern="notify (on|off)$",
    command=("notify", menu_category),
    info={
        "header": "To update the your chat after restart or reload .",
        "description": "Will send the ping cmd as reply to the previous last msg of (restart/reload/update cmds).",
        "usage": [
            "{tr}notify <on/off>",
        ],
    },
)
async def set_pmlog(event):
    "To update the your chat after restart or reload ."
    input_str = event.pattern_match.group(1)
    if input_str == "off":
        if gvarstatus("restartupdate") is None:
            return await eod(event, "__Notify was already disabled__")
        delgvar("restartupdate")
        return await eor(event, "__Notify was disabled successfully.__")
    if gvarstatus("restartupdate") is None:
        addgvar("restartupdate", "turn-oned")
        return await eor(event, "__Notify was enabled successfully.__")
    await eod(event, "__Notify was already enabled.__")

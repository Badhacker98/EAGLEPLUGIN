import sys

import Eaglebot
from Eaglebot import BOTLOG_CHATID, PM_LOGGER_GROUP_ID

from .Config import Config
from .core.logger import logging
from .core.session import eagle
from .start import killer
from .utils import (
    add_bot_to_logger_group,
    hekp,
    install_externalrepo,
    load_plugins,
    setup_bot,
    startupmessage,
    verifyLoggerGroup,
)

LOGS = logging.getLogger("ᴇᴀɢʟᴇ ᴜsᴇʀʙᴏᴛ")

print(Eaglebot.__copyright__)
print("ʟɪᴄᴇɴsᴇᴅ ᴜɴᴅᴇʀ ᴛʜᴇ ᴛᴇʀᴍs ᴏғ ᴛʜʀ " + Eaglebot.__license__)

cmdhr = Config.HANDLER


try:
    LOGS.info("sᴛᴀʀᴛ ᴛʜᴇ ᴇᴀɢʟᴇ ᴜsᴇʀʙᴏᴛ")
    eagle.loop.run_until_complete(setup_bot())
    LOGS.info("ᴛɢ ʙᴏᴛ sᴇᴛᴜᴘ ᴄᴏᴍᴘʟᴇᴛᴇᴅ")
except Exception as e:
    LOGS.error(f"{e}")
    sys.exit()
async def startup_process():
    try:
        await verifyLoggerGroup()
        await load_plugins("ᴘʟᴜɢɪɴs")
        await load_plugins("ᴀssɪsᴛᴀɴᴛ")
        await externalrepo()
        await killer()
        print("----------------")
        print("sᴛᴀʀᴛɪɴɢ ʙᴏᴛ ᴍᴏᴅᴇ!")
        print("ᴇᴀɢʟᴇʙᴏᴛ ʜᴀꜱ ʙᴇᴇɴ ᴅᴇᴘʟᴏʏᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ")
        print("ᴏᴡɴᴇʀ - @ll_BAD_MUNDA_ll")
        print("ɢʀᴏᴜᴘ - @PBX_CHAT")
        print("----------------")
        await verifyLoggerGroup()
        await add_bot_to_logger_group(BOTLOG_CHATID)
        if PM_LOGGER_GROUP_ID != -100:
            await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
        await startupmessage()
        await hekp()
    except Exception as e:
        LOGS.error(f"{str(e)}")
        sys.exit()


async def externalrepo():
    if Config.EXTERNAL_REPO:
        await install_externalrepo(
            Config.EXTERNAL_REPO, Config.EXTERNAL_REPOBRANCH, "xtraplugins"
        )
    if Config.VCMODE:
        await install_externalrepo(Config.VC_REPO, Config.VC_REPOBRANCH, "eaglevc")


eagle.loop.run_until_complete(startup_process())

if len(sys.argv) not in (1, 3, 4):
    eagle.disconnect()
else:
    try:
        eagle.run_until_disconnected()
    except ConnectionError:
        pass
        
        

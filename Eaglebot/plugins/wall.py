import os
import random

import requests
from bs4 import BeautifulSoup

from Eaglebot import eagle

from ..core.logger import logging
from ..core.managers import eod, eor
from ..helpers.utils import reply_id

LOGS = logging.getLogger(os.path.basename(__name__))
menu_category = "extra"


async def wall_download(piclink, query):
    try:
        if not os.path.isdir("./temp"):
            os.mkdir("./temp")
        picpath = f"./temp/{query.title().replace(' ', '')}.jpg"
        if os.path.exists(picpath):
            i = 1
            while os.path.exists(picpath) and i < 11:
                picpath = f"./temp/{query.title().replace(' ', '')}-{i}.jpg"
                i += 1
        with open(picpath, "wb") as f:
            f.write(requests.get(piclink).content)
        return picpath
    except Exception as e:
        LOGS.info(str(e))
        return None


@eagle.eagle_cmd(
    pattern="wall(?:\s|$)([\s\S]*)",
    command=("wall", menu_category),
    info={
        "header": "Searches and uploads wallpaper",
        "usage": ["{tr}wall <query>", "{tr}wall <query> ; <1-10>"],
        "examples": ["{tr}wall eagle", "{tr}wall eagle ; 2"],
    },
)
async def noods(event):
    "Wallpaper searcher"
    query = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    limit = 1
    if not query:
        return await eod(event, "`what should i search`", 10)
    if ";" in query:
        query, limit = query.split(";")
    if int(limit) > 10:
        return await eod(event, "`Wallpaper search limit is 1-10`", 10)
    eagleevent = await eor(event, "🔍 `Searching...`")
    r = requests.get(
        f"https://wall.alphacoders.com/search.php?search={query.replace(' ','+')}"
    )
    soup = BeautifulSoup(r.content, "lxml")
    walls = soup.find_all("img", class_="img-responsive")
    if not walls:
        return await eod(eagleevent, f"**Can't find anything with** `{query}`", 10)
    i = count = 0
    piclist = []
    piclinks = []
    captionlist = []
    await eor(eagleevent, "⏳ `Processing..`")
    url2 = "https://api.alphacoders.com/content/get-download-link"
    for x in walls:
        wall = random.choice(walls)["src"][8:-4]
        server = wall.split(".")[0]
        fileid = wall.split("-")[-1]
        data = {
            "content_id": fileid,
            "content_type": "wallpaper",
            "file_type": "jpg",
            "image_server": server,
        }
        res = requests.post(url2, data=data)
        a = res.json()["link"]
        if "We are sorry," not in requests.get(a).text and a not in piclinks:
            await eor(eagleevent, "📥** Downloading...**")
            pic = await wall_download(a, query)
            if pic is None:
                return await eod(eagleevent, "__Sorry i can't download wallpaper.__")
            piclist.append(pic)
            piclinks.append(a)
            captionlist.append("")
            count += 1
            i = 0
        else:
            i += 1
        await eor(
            eagleevent, f"**📥 Downloaded : {count}/{limit}\n\n❌ Errors : {i}/5**"
        )
        if count == int(limit):
            break
        if i == 5:
            await eor(eagleevent, "`Max search error limit exceed..`")
    try:
        await eor(eagleevent, "`Sending...`")
        captionlist[-1] = f"**➥ Query :-** `{query.title()}`"
        await event.client.send_file(
            event.chat_id,
            piclist,
            caption=captionlist,
            reply_to=reply_to_id,
            force_document=True,
        )
        await eagleevent.delete()
    except Exception as e:
        LOGS.info(str(e))
    for i in piclist:
        os.remove(i)

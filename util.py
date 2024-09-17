import random
import os
import aiohttp
import httpx
from pathlib import Path
BGIMAGE_PATH=Path('/home/asankilp/biography/User/RavenSenorita/sayings')
def choose_random():
    randomfile = random.choice(list(BGIMAGE_PATH.iterdir()))
    randomurl = str(randomfile)
    return randomurl
async def download_file(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # 确保请求成功
        with open("./azureaipic.png", 'wb') as f:
            f.write(response.content)

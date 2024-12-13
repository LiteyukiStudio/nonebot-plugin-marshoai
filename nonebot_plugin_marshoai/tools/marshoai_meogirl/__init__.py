from . import mg_info, mg_introduce, mg_search


# meogirl
async def meogirl():
    return mg_info.meogirl()


# Search
async def search(msg: str, num: int = 3):
    return str(await mg_search.search(msg, num))


# Show
async def introduce(msg: str):
    return str(await mg_introduce.introduce(msg))

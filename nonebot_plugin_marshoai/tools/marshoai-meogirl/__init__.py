
from . import mg_Info
from . import mg_Search
from . import mg_Introduce

# meogirl
async def meogirl () :
    return mg_Info.meogirl()

# Search
async def search (msg : str, num : int = 3) :
    return str(await mg_Search.search(msg, num))

# Show
async def introduce (msg : str) :
    return str(await mg_Introduce.introduce(msg))

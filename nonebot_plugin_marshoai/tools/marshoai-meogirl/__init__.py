from . import mg_Info
from . import mg_Search

# meogirl
async def meogirl():
    return mg_Info.meogirl()

# Search
async def search(msg : str, num : int = 3):
    return str(mg_Search.search(msg, num))
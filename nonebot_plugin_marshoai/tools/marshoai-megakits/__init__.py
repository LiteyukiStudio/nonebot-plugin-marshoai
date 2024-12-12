
from . import mk_Info
from . import mk_Common
from . import mk_MorseCode
from . import mk_NyaCode

# Twisuki
async def twisuki():
    return str(await mk_Info.twisuki())

# MegaKits
async def megakits():
    return str(await mk_Info.megakits())

# Random Turntable
async def random_turntable(upper: int, lower: int = 0):
    return str(await mk_Common.random_turntable(upper, lower))

# Number Calc
async def number_calc(a: str, b: str, op: str):
    return str(await mk_Common.number_calc(a, b, op))

# MorseCode Encrypt
async def morse_encrypt(msg: str):
    return str(await mk_MorseCode.morse_encrypt(msg))

# MorseCode Decrypt
async def morse_decrypt(msg: str):
    return str(await mk_MorseCode.morse_decrypt(msg))

# NyaCode Encrypt
async def nya_encode(msg: str):
    return str(await mk_NyaCode.nya_encode(msg))

# NyaCode Decrypt
async def nya_decode(msg: str):
    return str(await mk_NyaCode.nya_decode(msg))

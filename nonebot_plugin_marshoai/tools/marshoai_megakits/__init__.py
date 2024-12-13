from . import mk_common, mk_info, mk_morse_code, mk_nya_code


# Twisuki
async def twisuki():
    return str(await mk_info.twisuki())


# MegaKits
async def megakits():
    return str(await mk_info.megakits())


# Random Turntable
async def random_turntable(upper: int, lower: int = 0):
    return str(await mk_common.random_turntable(upper, lower))


# Number Calc
async def number_calc(a: str, b: str, op: str):
    return str(await mk_common.number_calc(a, b, op))


# MorseCode Encrypt
async def morse_encrypt(msg: str):
    return str(await mk_morse_code.morse_encrypt(msg))


# MorseCode Decrypt
async def morse_decrypt(msg: str):
    return str(await mk_morse_code.morse_decrypt(msg))


# NyaCode Encrypt
async def nya_encode(msg: str):
    return str(await mk_nya_code.nya_encode(msg))


# NyaCode Decrypt
async def nya_decode(msg: str):
    return str(await mk_nya_code.nya_decode(msg))

# MorseCode
MorseEncode = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ".": ".-.-.-",
    ":": "---...",
    ",": "--..--",
    ";": "-.-.-.",
    "?": "..--..",
    "=": "-...-",
    "'": ".----.",
    "/": "-..-.",
    "!": "-.-.--",
    "-": "-....-",
    "_": "..--.-",
    '"': ".-..-.",
    "(": "-.--.",
    ")": "-.--.-",
    "$": "...-..-",
    "&": "....",
    "@": ".--.-.",
    " ": " ",
}
MorseDecode = {value: key for key, value in MorseEncode.items()}


# MorseCode Encrypt
async def morse_encrypt(msg: str):
    result = ""
    msg = msg.upper()
    for char in msg:
        if char in MorseEncode:
            result += MorseEncode[char]
        else:
            result += "..--.."
        result += " "

    return result


# MorseCode Decrypt
async def morse_decrypt(msg: str):
    result = ""

    msg_arr = msg.split()
    for char in msg_arr:
        if char in MorseDecode:
            result += MorseDecode[char]
        else:
            result += "?"

    return result

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


async def morse_decrypt(msg: str):
    result = ""
    msg = msg.replace("_", "-")
    msg_arr = msg.split(" ")
    for element in msg_arr:
        if element in MorseDecode:
            result += MorseDecode[element]
        else:
            result += "?"
    return result

# Dictionary mapping each tool to the operations it supports, the key type it requires, the name of the function to call when that tool is selected, and the argument that function expects. This is a way to call dynamically the function without needing to code more than neccesary
TOOL_INFO = {
    "rot": {
        "name": "Rotation / Caesar cipher",
        "operations": ["encrypt", "decrypt", "bruteforce", "generate", "info"],
        "key_type": "int"
    },
    "subst": {
        "name": "Substitution cipher",
        "operations": ["encrypt", "decrypt", "generate", "info"],
        "key_type": "str"
    },
    "atbash": {
        "name": "Atbash cipher",
        "operations": ["encrypt", "decrypt", "info"],
        "key_type": None
    },
    "vigenere": {
        "name": "Vigenère cipher",
        "operations": ["encrypt", "decrypt", "generate", "info"],
        "key_type": "str"
    },
    "railfence": {
        "name": "Rail fence cipher",
        "operations": ["encrypt", "decrypt", "bruteforce", "generate", "info"],
        "key_type": "int"
    },
    "columnar": {
        "name": "Columnar transposition cipher",
        "operations": ["encrypt", "decrypt", "generate", "info"],
        "key_type": "str"
    },
    "numval": {
        "name": "Numeric value cipher",
        "operations": ["encrypt", "decrypt", "info"],
        "key_type": None
    }
}
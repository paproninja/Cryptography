import argparse, os
from scripts import railfence, atbash, vigenere, subst, numval, rot


# --------------------------------------------------------------------------------------------------------------
# ---------------------------------------- ARGUMENT PARSER ----------------------------------------
# --------------------------------------------------------------------------------------------------------------

def argument_parser():

    # ---------------- CREATE THE PARSER ----------------

    parser = argparse.ArgumentParser(
        prog="crypto",
        description="CLI tool for classical ciphers",
        usage="usage: crypto [TOOL] [OPERATION] [-t TEXT] [-k KEY]",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
        
    Compatibility table:
    
    Tool              | Operations                        | T             | K            | Key Type
    ------------------+-----------------------------------+---------------+--------------+------------------
    ROT               | -e (T, K); -d (T, K); -b (T); -g  | Requires Text | Requires Key | int
    SUBST             | -e (T, K); -d (T, K); -g          | Requires Text | Requires Key | 26 char long str
    NUMVAL            | -e (T); -d (T)                    | Requires Text | -            | -
    ATBASH            | -e (T); -d (T)                    | Requires Text | -            | -
    VIGENERE          | -e (T, K); -d (T, K), -g          | Requires Text | Requires Key | str
    RAIL FENCE        | -e (T, K); -d (T, K); -b (T); -g  | Requires Text | Requires Key | int
    
    """)

    #Tools
    tool_monoalphabetic_group = parser.add_argument_group("substitution/monoalphabetic ciphers") #tool_monoalphabetic_group is a parser group. In this group, tools are managed: --caesar, --atbash

    tool_monoalphabetic_group.add_argument("--rot", action="store_true", help="Rotation cipher", dest="rot") #"--rot" is the name of the flag. action="store_true means that if it exists, set it to true, if not false. Dest is how we access the argument when parsed.
    tool_monoalphabetic_group.add_argument("--subst", action="store_true", help="Substitution cipher", dest="subst")
    tool_monoalphabetic_group.add_argument("--atbash", action="store_true", help="Atbash cipher (ABC -> ZYX)", dest="atbash")


    tool_polyalphabetic_group = parser.add_argument_group("polyalphabetic ciphers")

    tool_polyalphabetic_group.add_argument("--vigenere", action="store_true", help="", dest="vigenere")


    tool_transposition_group = parser.add_argument_group("transposition ciphers")

    tool_transposition_group.add_argument("--railfence", action="store_true", help="Rail fence cipher", dest="railfence")


    tool_other_group = parser.add_argument_group("other ciphers")

    tool_other_group.add_argument("--numval", action="store_true", help="Numeric value cipher (ABC -> 1 2 3)", dest="numval")


    #Operations
    operation_group = parser.add_argument_group("Operation Selection").add_mutually_exclusive_group(required=False)

    operation_group.add_argument("-e", "--encrypt", action="store_true", help="Encrypts provided text", dest="encrypt")
    operation_group.add_argument("-d", "--decrypt", action="store_true", help="Decrypts provided text", dest="decrypt")
    operation_group.add_argument("-b", "--bruteforce", action="store_true", help="Brute forces provided text with all keys if compatible", dest="bruteforce")
    operation_group.add_argument("-g", "--generate", action="store_true", help="Generates a random key if compatible", dest="generate")
    operation_group.add_argument("-i", "--info", action="store_true", help="Provides information about the selected tool", dest="info")


    #Conditional args. These aren't forced since they aren't needed in all situations f.e. when we select --info
    input_group = parser.add_argument_group("Inputs")
    input_group.add_argument("-t", "--text", help="String or file to be encrypted or decrypted", dest="text")
    input_group.add_argument("-k", "--key", help="String or file used as a key for encryption or decryption if needed", dest="key")

    # ---------------- TOOL INFORMATION TABLE ----------------

    # Dictionary mapping each tool to the operations it supports, the key type it requires, the name of the function to call when that tool is selected, and the argument that function expects. This is a way to call dynamically the function without needing to code more than neccesary
    TOOL_INFO = {
        "rot": {
            "operations": ["encrypt", "decrypt", "bruteforce", "generate", "info"],
            "key_type": "int",
        },
        "subst": {
            "operations": ["encrypt", "decrypt", "generate", "info"],
            "key_type": "str",
        },
        "numval": {
            "operations": ["encrypt", "decrypt", "info"],
            "key_type": None,
        },
        "atbash": {
            "operations": ["encrypt", "decrypt", "info"],
            "key_type": None,
        },
        "vigenere": {
            "operations": ["encrypt", "decrypt", "generate", "info"],
            "key_type": "str",
        },
        "railfence": {
            "operations": ["encrypt", "decrypt", "bruteforce", "generate", "info"],
            "key_type": "int",
        }
    }

    # ---------------- PARSE ALL ARGUMENTS ----------------

    args = parser.parse_args()

    # ---------------- DETECT SELECTED TOOL ----------------

    SELECTED_TOOL = None

    for name, value in vars(args).items():
        # Skip non-tool args
        if name in ["encrypt", "decrypt", "bruteforce", "generate", "info", "text", "key"]:
            continue
        # If the flag is True, select this tool
        if value:
            # If we already have a tool selected, show an error
            if SELECTED_TOOL is None:
                SELECTED_TOOL = name
            else:
                parser.error("Must provide only one tool. Use crypto --help")

    # If no tool was selected, show an error
    if SELECTED_TOOL is None:
        parser.error("Must provide a tool. Use crypto --help")

    # ---------------- DETECT SELECTED OPERATION ----------------

    SELECTED_OPERATION = None

    for name, value in vars(args).items():
        # Only check operation flags
        if name in ["encrypt", "decrypt", "bruteforce", "generate", "info"]:
            if value:
                SELECTED_OPERATION = name

    # If no operation was selected, show an error
    if SELECTED_OPERATION is None:
        SELECTED_OPERATION = "encrypt"

    # --------------- CHECK COMPATIBILITY BETWEEN TOOL/OPERATION ---------------

    if SELECTED_OPERATION not in TOOL_INFO[SELECTED_TOOL]["operations"]:
        parser.error(
            "Operation " + SELECTED_OPERATION + " is not compatible with " + SELECTED_TOOL + ". Use crypto --help")

    # ---------------- LOAD AND VALIDATE TEXT (-t / --text) ----------------

    TEXT = None

    # Required for encrypt, decrypt, and bruteforce
    if SELECTED_OPERATION in ["encrypt", "decrypt", "bruteforce"]:
        if args.text is None:
            parser.error(SELECTED_OPERATION + " requires -t/--text argument")

        # Read from file if it exists, else treat as direct string input
        if os.path.isfile(args.text):
            with open(args.text, "r") as file:
                TEXT = file.read().strip()
        else:
            TEXT = str(args.text).strip()

        # Ensure the text is not purely numeric
        if TEXT.isdigit():
            parser.error("-t/--text input must be a string, not a number")

    elif args.text is not None:
        parser.error(SELECTED_OPERATION + " does not require -t/--text argument")

    # ---------------- LOAD AND VALIDATE KEY (-k / --key) ----------------

    KEY = None

    # Only required for ciphers that need a key and encrypt/decrypt operations
    if TOOL_INFO[SELECTED_TOOL]["key_type"] is not None and SELECTED_OPERATION in ["encrypt", "decrypt"]:
        if args.key is None:
            parser.error(SELECTED_TOOL + " cipher requires -k/--key argument")

        # Read key from file if it exists, else treat as direct input
        if os.path.isfile(args.key):
            with open(args.key, "r") as file:
                KEY = file.read().strip()
        else:
            KEY = str(args.key).strip()

        # Try converting to int, else leave as string
        try:
            KEY = int(KEY)
        except ValueError:
            pass

    # ---------------- CHECK KEY TYPE ----------------

    if TOOL_INFO[SELECTED_TOOL]["key_type"] is not None and KEY is not None:  #If we have a needed key
        if TOOL_INFO[SELECTED_TOOL]["key_type"] == "int" and not isinstance(KEY, int):    #If we need int and key isn't we give an error
            parser.error(SELECTED_TOOL + " tool requires numeric key (-k)")
        elif TOOL_INFO[SELECTED_TOOL]["key_type"] == "str" and not isinstance(KEY, str):  #If we need str and key isn't we give an error
            parser.error(SELECTED_TOOL + " tool requires string key (-k)")

    # --------------- CALL TOOL FUNCTION WITH PARSED ARGUMENTS ---------------

    if SELECTED_TOOL == "rot":
        rot.rot(text=TEXT, key=KEY, operation=SELECTED_OPERATION)
    elif SELECTED_TOOL == "subst":
        subst.subst(text=TEXT, key=KEY, operation=SELECTED_OPERATION)
    elif SELECTED_TOOL == "numval":
        numval.numval(text=TEXT, operation=SELECTED_OPERATION)
    elif SELECTED_TOOL == "atbash":
        atbash.atbash(text=TEXT, operation=SELECTED_OPERATION)
    elif SELECTED_TOOL == "vigenere":
        vigenere.vigenere(text=TEXT, key=KEY, operation=SELECTED_OPERATION)
    elif SELECTED_TOOL == "railfence":
        railfence.railfence(text=TEXT, key=KEY, operation=SELECTED_OPERATION)


# --------------------------------------------------------------------------------------------------------------
# ---------------------------------------- START PROGRAM ----------------------------------------
# --------------------------------------------------------------------------------------------------------------

argument_parser()
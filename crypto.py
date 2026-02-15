import argparse
import os
import string
import random

# --------------------------------------------------------------------------------------------------------------
# ---------------------------------------- INFORMATION TO ADD A NEW CIPHER----------------------------------------
# --------------------------------------------------------------------------------------------------------------

# To add a new cipher, you need to:
#   1. Add help text for the cipher in argunment_parser() -> parser definition -> epilog
#   2. Add argument parsing logic for the cipher in argument_parser() below parser definition, in the Ciphers section
#   3. Add the cipher to the CIPHER_INFO dictionary in argument_parser() -> CIPHER INFORMATION TABLE section.
#   4. Add the cipher's functions to the bottom of this file in the CIPHER FUNCTIONS section.


# --------------------------------------------------------------------------------------------------------------
# ---------------------------------------- ARGUMENT PARSER ----------------------------------------
# --------------------------------------------------------------------------------------------------------------

def argument_parser():

    # ---------------- CREATE THE PARSER ----------------

    parser = argparse.ArgumentParser(
        prog="crypto",
        description="CLI tool for classical ciphers",
        usage="usage: crypto [CIPHER] [OPERATION] [-t TEXT] [-k KEY]",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
    Cipher   | Operations                        | T             | K            | Key Type
    ---------+-----------------------------------+---------------+--------------+------------------
    ROT      | -e (T, K); -d (T, K); -b (T); -g  | Requires Text | Requires Key | int
    SUBST    | -e (T, K); -d (T, K); -g          | Requires Text | Requires Key | 26 char long str
    NUMVAL   | -e (T); -d (T)                    | Requires Text | -            | -
    ATBASH   | -e (T); -d (T)                    | Requires Text | -            | -
    
    """)

    #Ciphers
    cipher_group = parser.add_argument_group("Cipher Selection").add_mutually_exclusive_group(required=True) #cipher_group is a parser group, that is required, and mutually exclusive. In this group, ciphers are managed: --caesar, --atbash ... where only one can be selected.

    cipher_group.add_argument("--rot", action="store_true", help="Rotation cipher", dest="rot") #"--rot" is the name of the flag. action="store_true means that if it exists, set it to true, if not false. Dest is how we access the argument when parsed.
    cipher_group.add_argument("--subst", action="store_true", help="Substitution cipher", dest="subst")
    cipher_group.add_argument("--numval", action="store_true", help="Number value cipher (ABC -> 1 2 3)", dest="numval")
    cipher_group.add_argument("--atbash", action="store_true", help="Atbash cipher (ABC -> ZYX)", dest="atbash")

    #Operations
    operation_group = parser.add_argument_group("Operation Selection").add_mutually_exclusive_group(required=True)

    operation_group.add_argument("-e", "--encrypt", action="store_true", help="Encrypts provided text", dest="encrypt")
    operation_group.add_argument("-d", "--decrypt", action="store_true", help="Decrypts provided text", dest="decrypt")
    operation_group.add_argument("-b", "--bruteforce", action="store_true", help="Brute forces provided text with all keys if compatible", dest="bruteforce")
    operation_group.add_argument("-g", "--generate", action="store_true", help="Generates a random key if compatible", dest="generate")
    operation_group.add_argument("-i", "--info", action="store_true", help="Provides information about the selected cipher", dest="info")

    #Conditional args. These aren't forced since they aren't needed in all situations f.e. when we select --info
    input_group = parser.add_argument_group("Inputs")
    input_group.add_argument("-t", "--text", help="String or file to be encrypted or decrypted", dest="text")
    input_group.add_argument("-k", "--key", help="String or file used as a key for encryption or decryption if needed", dest="key")

    # ---------------- CIPHER INFORMATION TABLE ----------------

    # Dictionary mapping each cipher to the operations it supports, the key type it requires, the name of the function to call when that cipher is selected, and the argument that function expects. This is a way to call dynamically the function without needing to code more than neccesary
    CIPHER_INFO = {
        "rot": {
            "operations": ["encrypt", "decrypt", "bruteforce", "generate", "info"],
            "key_type": "int",
            "func_name": rot,
            "func_args": ["text", "key", "operation"]
        },
        "subst": {
            "operations": ["encrypt", "decrypt", "generate", "info"],
            "key_type": "str",
            "func_name": subst,
            "func_args": ["text", "key", "operation"]
        },
        "numval": {
            "operations": ["encrypt", "decrypt", "info"],
            "key_type": None,
            "func_name": numval,
            "func_args": ["text", "operation"]
        },
        "atbash": {
            "operations": ["encrypt", "decrypt", "info"],
            "key_type": None,
            "func_name": atbash,
            "func_args": ["text", "operation"]
        }
    }

    # ---------------- PARSE ALL ARGUMENTS ----------------

    args = parser.parse_args()

    # ---------------- DETECT SELECTED CYPHER ----------------

    SELECTED_CIPHER = None

    for name, value in vars(args).items():
        # Skip non-cipher args
        if name in ["encrypt", "decrypt", "bruteforce", "generate", "info", "text", "key"]:
            continue
        # If the flag is True, select this cipher
        if value:
            SELECTED_CIPHER = name

    # If no cipher was selected, show an error
    if SELECTED_CIPHER is None:
        parser.error("Must provide a cipher. Use crypto --help")

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

    # --------------- CHECK COMPATIBILITY BETWEEN CIPHER/OPERATION ---------------

    if SELECTED_OPERATION not in CIPHER_INFO[SELECTED_CIPHER]["operations"]:
        parser.error(
            "Operation " + SELECTED_OPERATION + " is not compatible with " + SELECTED_CIPHER + ". Use crypto --help")

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
    if CIPHER_INFO[SELECTED_CIPHER]["key_type"] is not None and SELECTED_OPERATION in ["encrypt", "decrypt"]:
        if args.key is None:
            parser.error(SELECTED_CIPHER + " cipher requires -k/--key argument")

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

    if CIPHER_INFO[SELECTED_CIPHER]["key_type"] is not None and KEY is not None:  #If we have a needed key
        if CIPHER_INFO[SELECTED_CIPHER]["key_type"] == "int" and not isinstance(KEY, int):    #If we need int and key isn't we give an error
            parser.error("Cipher " + SELECTED_CIPHER + " requires numeric key (-k)")
        elif CIPHER_INFO[SELECTED_CIPHER]["key_type"] == "str" and not isinstance(KEY, str):  #If we need str and key isn't we give an error
            parser.error("Cipher " + SELECTED_CIPHER + " requires string key (-k)")

    # --------------- DYNAMICALLY CALL CIPHER FUNCTION WITH PARSED ARGUMENTS ---------------

    # This code is a dynamic way to call the function specified in the CIPHER_INFO dictionary, without needing to code for each cipher separately.

    CIPHER_INFO[SELECTED_CIPHER]["func_name"](*[TEXT if arg == "text" else KEY if arg == "key" else SELECTED_OPERATION for arg in CIPHER_INFO[SELECTED_CIPHER]["func_args"]])

    # Starting from the beginning, CIPHER_INFO[SELECTED_CIPHER]["func_name"] takes the function name specified in the CIPHER_INFO dictionary.
    # Then, parenthesis are opened to signalize the argument inputs. Inside, there's square brackets opening a list, and a * that unpacks the iterable to function arguments.
    # Inside this list theres an inline for loop (expression for iterable_var in list), that iterates through the "func_args" list defined in the CIPHER_INFO dictionary.
    # In each iteration, arg gets the value of one of the arguments needed for the function.
    # The expression, is an inline if (expression_if_true if condition else expression_if_false), that, f.e., it gives "TEXT" if arg is "text"

# --------------------------------------------------------------------------------------------------------------
# ---------------------------------------- CIPHER FUNCTIONS ----------------------------------------
# --------------------------------------------------------------------------------------------------------------

def rot(text, key, operation):

    def rot_logic(text, key):

        # Define alphabets and final text variable
        letters_lower = string.ascii_lowercase
        letters_upper = string.ascii_uppercase
        final_text = ""

        for char in text:
            # If the character is in the lower alphabet, move it in the alphabet <key> times ahead
            if char in letters_lower:
                final_text += letters_lower[(letters_lower.index(char) + key) % 26]
            # If the character is in the upper alphabet, move it in the alphabet <key> times ahead
            elif char in letters_upper:
                final_text += letters_upper[(letters_upper.index(char) + key) % 26]
            # If the character is not in the alphabet, add it as is
            else:
                final_text += char

        return final_text

    if operation == "encrypt":
        print(rot_logic(text, key))    # Encrypts the text with the key provided
        return None

    elif operation == "decrypt":
        print(rot_logic(text, 0 - key))    # Decrypts the text with the key provided
        return None

    if operation == "bruteforce":
        for i in range(26):     # Brute forces the text with all possible keys
            print("ROT " + str(i) + ": " + rot_logic(text, i))
        return None

    if operation == "generate":
        print(random.randint(1,26))     # Generates a random key
        return None

    if operation == "info":
        print("Rot info: Each letter of the string is moved in the alphabet <key> times ahead. For example, with a key of 1 a would become b, b would be c, ... A common key is 13 (ROT13) where each letter is moved 13 times.")
        return None


def subst(text, key, operation):

    def subst_logic_enc(text, key):

        # Define alphabets and final text variable
        letters_lower = string.ascii_lowercase
        letters_upper = string.ascii_uppercase
        key_lower = key.lower()
        key_upper = key.upper()
        final_text = ""

        for char in text:
            # If the character is in the lower alphabet, replace it with the corresponding character in the key
            if char in letters_lower:
                final_text += key_lower[letters_lower.index(char)]
            # If the character is in the upper alphabet, replace it with the corresponding character in the key
            elif char in letters_upper:
                final_text += key_upper[letters_upper.index(char)]
            # If the character is not in the alphabet, add it as is
            else:
                final_text += char

        return final_text

    def subst_logic_dec(text, key):

        # Define alphabets and final text variable
        letters_lower = string.ascii_lowercase
        letters_upper = string.ascii_uppercase
        key_lower = key.lower()
        key_upper = key.upper()
        final_text = ""

        for char in text:
            # If the character is in the key, replace it with the corresponding character in the lower alphabet
            if char in key_lower:
                final_text += letters_lower[key_lower.index(char)]
            # If the character is in the key, replace it with the corresponding character in the upper alphabet
            elif char in key_upper:
                final_text += letters_upper[key_upper.index(char)]
            # If the character is not in the key, add it as is
            else:
                final_text += char

        return final_text

    def subst_logic_gen():

        # Define alphabets and final text variable
        letters = list(string.ascii_uppercase)
        final_text = ""

        # Loop 26 times, each time picking a random letter from the alphabet and removing it from the list
        for i in range(26):
            rnd = random.randint(0, len(letters) - 1)
            final_text += letters[rnd]
            letters.pop(rnd)

        return final_text

    if operation == "encrypt":
        print(subst_logic_enc(text, key))   # Encrypts the text with the key provided
        return None

    if operation == "decrypt":
        print(subst_logic_dec(text,key))    # Decrypts the text with the key provided
        return None

    if operation == "generate":
        print(subst_logic_gen())    # Generates a random key
        return None

    if operation == "info":
        print("Substitution cipher uses a custom alphabet (key), and each letter from the regular alphabet (a, b, c, ...) becomes the letter in the same position in the key.")
        return None


def numval(text, operation):

    def numval_logic_enc(text):

        # Define alphabets and final text variable
        letters = string.ascii_uppercase
        final_text = ""

        for char in text.upper():
            if char in letters:
                final_text += str(letters.index(char)+1) + " "  # Adds the index of the character in the alphabet + 1, followed by a space
            elif char == " ":
                final_text += "0 "
            else:
                continue

        return final_text

    def numval_logic_dec(text):

        # Define alphabets and final text variable
        letters = string.ascii_uppercase
        final_text = ""

        for char in list(map(int, text.split())):   # Splits the text by spaces and converts each element to int, and puts them in a list
            if char != 0:
                final_text += letters[char - 1]
            else:
                final_text += " "

        return final_text

    if operation == "encrypt":
        print (numval_logic_enc(text))
        return None

    if operation == "decrypt":
        print (numval_logic_dec(text))
        return None

    if operation == "info":
        print("Numeric Value changes each letter for it's index in the alphabet.")
        return None


def atbash(text, operation):

    def atbash_logic(text):

        # Define alphabets and final text variable
        letters_lower = string.ascii_lowercase
        letters_upper = string.ascii_uppercase
        final_text = ""

        for char in text:
            if char in letters_lower:
                final_text += letters_lower[25 - letters_lower.index(char)]     # Changes the letter to the opposite position in the alphabet
            elif char in letters_upper:
                final_text += letters_upper[25 - letters_upper.index(char)]     # Changes the letter to the opposite position in the alphabet
            else:
                final_text += char  # If the character is not in the alphabet, add it as is

        return final_text

    if operation == "encrypt" or operation == "decrypt":    # It's the same logic
        print(atbash_logic(text))
        return None

    if operation == "info":
        print("Atbash cipher reverses the order of the letters in the alphabet.")
        return None

# --------------------------------------------------------------------------------------------------------------
# ---------------------------------------- START PROGRAM ----------------------------------------
# --------------------------------------------------------------------------------------------------------------

argument_parser()
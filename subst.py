import string, random

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

    return None
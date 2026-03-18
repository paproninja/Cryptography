import string, random

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

    return None
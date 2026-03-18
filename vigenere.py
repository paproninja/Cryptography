import string, random

def vigenere(text, key, operation):

    def vigenere_logic_enc(text, key, operation):   # We also input the operation to know if we gotta rotate forwards or backwards.

        # Define alphabets and final text variable
        letters_lower = string.ascii_lowercase
        letters_upper = string.ascii_uppercase
        final_text = ""

        n = 0
        for char in text:
            if char in letters_lower:
                final_text += letters_lower[
                    (
                            letters_lower.index(char) +     # We take the index of the letter in the text
                            (
                                letters_upper.index(key.upper()[n]) if operation == "encrypt" else 0 - letters_upper.index(key.upper()[n])  # And add to it the index of the letter in the key in the alphabet, or subtract it if we're decrypting
                            )
                    ) % 26
                ]
                n = (n + 1) % len(key)  # Add one for next character in the key in the next iteration

            elif char in letters_upper:
                final_text += letters_upper[
                    (
                            letters_upper.index(char) +     # We take the index of the letter in the text
                            (
                                letters_upper.index(key.upper()[n]) if operation == "encrypt" else 0 - letters_upper.index(key.upper()[n])  # And add to it the index of the letter in the key in the alphabet, or subtract it if we're decrypting
                            )
                    ) % 26
                ]
                n = (n + 1) % len(key)  # Add one for next character in the key in the next iteration

            else:
                final_text += char

        return final_text

    def vigenere_logic_gen():

        # Define alphabets and final text variable
        letters = list(string.ascii_uppercase)
        final_text = ""

        for i in range(random.randint(5, 15)):
            final_text += letters[random.randint(0, 25)]

        return final_text


    if operation == "encrypt" or operation == "decrypt":
        print(vigenere_logic_enc(text, key, operation))
        return None

    if operation == "generate":
        print(vigenere_logic_gen())
        return None

    if operation == "info":
        print("Vigenère cipher takes each letter of the plaintext, and its encoded with a different Caesar cipher, whose increment is determined by the corresponding letter of another text, the key")
        return None

    return None
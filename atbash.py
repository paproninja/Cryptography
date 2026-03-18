import string

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

    return None
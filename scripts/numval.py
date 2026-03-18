import string

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

    return None
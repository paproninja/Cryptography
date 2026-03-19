import string, random

def columnar(text, key, operation):

    def columnar_logic_enc(text, key):

        final_text = ""

        columns = [[] for i in range(len(key))] # Create a list of lists. Each list will represent a column.
        key=list(key.upper())

        n = 0
        for char in text: # Loop through the text and add each character to the corresponding column
            columns[n%len(key)].append(char)
            n += 1

        for i in sorted(key): # Go through a sorted list of the key, ordered by the position in the alphabet and join the columns in the same order
            final_text += "".join(columns[key.index(i)])
            columns.pop(key.index(i))
            key.pop(key.index(i))

        return final_text

    def columnar_logic_dec(text, key):

        final_text = ""

        columns = [[] for i in range(len(key))]
        key=list(key.upper())
        sorted_key = sorted(key)

        n = 0
        for i in sorted_key: # For each column, in order...
            for j in range(len(text)//len(key)): # ...add the corresponding character to the final text
                columns[key.index(i)].append(text[n])
                n += 1
            if len(text)%len(key) != 0 and len(text)%len(key) <= n%len(key) and n<len(text): # Add left letters
                columns[key.index(i)].append(text[n])
                n += 1

            key=list("".join(key).replace(i,":",1)) # Remove the used letter so duplicates dont overlap

        for i in range(len(text)):
            final_text += columns[i%len(key)][i//len(key)]

        return final_text

    def columnar_logic_gen():

        # Define alphabets and final text variable
        letters = list(string.ascii_uppercase)
        final_text = ""

        # Loop x times, each time picking a random letter from the alphabet and removing it from the list
        for i in range(random.randint(3,5)):
            rnd = random.randint(0, len(letters) - 1)
            final_text += letters[rnd]
            letters.pop(rnd)

        return final_text


    if operation == "encrypt":
        print(columnar_logic_enc(text, key))
        return None

    if operation == "decrypt":
        print(columnar_logic_dec(text, key))
        return None

    if operation == "generate":
        print(columnar_logic_gen())
        return None

    if operation == "info":
        print("Columnar cipher is a transposition cipher, where the plaintext is separated in columns, and the encrypted text is the union of the columns in a specific order, determined by the key.")
        return None

    return None
import string, random

def railfence(text, key, operation):

    def railfence_logic_enc(text, key):

        letters_lower = string.ascii_lowercase
        letters_upper = string.ascii_uppercase
        final_text = ""

        #Remove not wanted chars, like spaces or punctuation
        working_text = ""
        for char in text:
            if char in letters_lower or char in letters_upper:
                working_text += char

        if key == 1: # If theres 1 rail, we just return the text
            return working_text

        rails = [[] for i in range(key)] # Creates a list where each item is [] (another list). Creates as much lists as rails.
        cicle = 2 * (key - 1)  # The cicle is the number of letters before the zigzag pattern repeats. With 2 rails, the cicle is 2, since the first one is in rail 0, the second one in rail 1, and the third is again in rail 0

        for i in range(len(working_text)): # For each letter in the text, we add it to the rail in which it is located

            pos = i % cicle  # pos gets the position inside the cicle. F.e., with 3 rails, 4 is the rail 0
            if pos >= key:  # In a 3 rail system, i 0-2 are in its respective rails, but 3 is in rail 1, so we invert those one greater than the rail number.
                pos = cicle - pos

            rails[pos].append(working_text[i])

        final_text = ''.join(''.join(n) for n in rails) # Joins the lists in the rails, and joins the lists in the final text

        return final_text

    def railfence_logic_dec(text, key):

        final_text = ""

        if key == 1:
            return text

        counts = [0 for i in range(key)]  # Creates a list with as many 0 as rails.
        cicle = 2 * (key - 1) # The cicle is the number of letters before the zigzag pattern repeats.

        for i in range(len(text)): # Count how many letters are in each rail

            pos = i % cicle # pos gets the position inside the cicle.
            if pos >= key: # Reflect to get the correct rail
                pos = cicle - pos

            counts[pos] += 1

        rails = [] # Creates a list
        idx = 0

        for i in range(key):

            rails.append(list(text[idx : idx + counts[i]])) # append to the list a listed string consisting of a slice of the text, where the slice starts at the idx, and ends in the idx + counts[i]
            idx += counts[i]


        pointers = [0 for i in range(key)] # Creates a list to keep track of the number of letters we added already in each rail

        for i in range(len(text)):

            pos = i % cicle
            if pos >= key:
                pos = cicle - pos

            final_text += rails[pos][pointers[pos]]
            pointers[pos] += 1

        return final_text


    if operation == "encrypt":
        print(railfence_logic_enc(text, key))
        return None

    if operation == "decrypt":
        print(railfence_logic_dec(text, key))
        return None

    if operation == "bruteforce":
        for i in range(1, len(text)+1):
            print("Railfence with " + str(i) + " rails: " + railfence_logic_dec(text, i))
        return None

    if operation == "generate":
        print(random.randint(1,10))
        return None

    if operation == "info":
        print("Rail fence cipher is a type of transposition cipher, where the plaintext is separated in a zigzag pattern between the rails, where the key is the number of rails. The encrypted text is the union of the rails.")
        return None

    return None
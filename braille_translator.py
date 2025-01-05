# braille_translator.py

# Define Grade 1 Braille mappings (letters and basic punctuation)
GRADE1_BRAILLE = {
    # Alphabets
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
    'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
    'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽',
    'z': '⠵',
    ' ': '⠀',

    # Punctuation
    # '.': '⠲', ',': '⠂', ';': '⠆', ':': '⠒', '!': '⠖',
    # '(': '⠶', ')': '⠶', '?': '⠦', '\'': '⠄', '-': '⠤',
    # '"': '⠶', '/': '⠌', '@': '⠈', '#': '⠼', '*': '⠔',
}

BRAILLE_NUMBERS = {
    # Numbers
    '0': '⠚', '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙',
    '5': '⠑', '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊',
}

# Reverse the dictionary for decoding
BRAILLE_TO_GRADE1 = {v: k for k, v in GRADE1_BRAILLE.items()}

# Define some common Grade 2 Braille contractions
GRADE2_CONTRACTIONS = {
    'and': '⠯',
    'for': '⠿',
    'the': '⠮',
    'with': '⠾',  
    'of': '⠷',
    'to': '⠞⠕', 
    'but': '⠃',
    'can': '⠉',
    'do': '⠙',
    'go': '⠛',
    'have': '⠓',
    'in': '⠔', 
    'it': '⠭', 
    'that': '⠞',
    'this': '⠹',  
    'you': '⠽',
    'she': '⠩⠑', 
    'he': '⠓⠑',  
    'they': '⠮⠽',
    'we': '⠺⠑',
    # Add more contractions as needed
}

# Reverse the contractions for decoding
BRAILLE_TO_GRADE2 = {v: k for k, v in GRADE2_CONTRACTIONS.items()}

# Define the number sign in Braille
NUMBER_SIGN = '⠼'

# Define the capital sign in Braille
CAPITAL_SIGN = '⠠'

def translate_to_grade2_braille(text):
    """
    Translates English text to a simplified version of Grade 2 Braille.
    This implementation handles a subset of Grade 2 contractions and numeric content.

    :param text: The English text to translate.
    :return: A string representing the translated Braille.
    """
    braille = ''
    words = text.split()

    for word in words:
        word_braille = ''
        original_word = word  # Save original for debugging

        # Handle numbers (Changed this as well (Galih))
        if word.isdigit():
            word_braille += NUMBER_SIGN  # Add numeric mode indicator
            for digit in word:
                word_braille += BRAILLE_NUMBERS.get(digit, '')

        # Add space to separate numbers from subsequent letters
            braille += word_braille + ' '  # Ensure a space follows numbers
            continue

        # Check if the word is capitalized
        if word[0].isupper():
            word_braille += CAPITAL_SIGN
            word = word.lower()

        # Check if the entire word has a contraction
        if word in GRADE2_CONTRACTIONS:
            print(f"Word-level contraction found: '{original_word}' -> '{GRADE2_CONTRACTIONS[word]}'")
            word_braille += GRADE2_CONTRACTIONS[word]
        else:
            # Check for contractions within the word
            i = 0
            while i < len(word):
                contraction_found = False
                for contraction in sorted(GRADE2_CONTRACTIONS.keys(), key=lambda x: len(x), reverse=True):
                    contraction_end = i + len(contraction)
                    # Match contraction only if it fits completely and is bounded (I chaged this abit (Galih))
                    if (
                        word[i:contraction_end] == contraction
                        and (i == 0 or not word[i - 1].isalpha())  # Start boundary check
                        and (contraction_end == len(word) or not word[contraction_end].isalpha())  # End boundary check
                    ):
                        # Log contraction match
                        print(f"Contraction match: '{word[i:contraction_end]}' in '{original_word}' -> '{GRADE2_CONTRACTIONS[contraction]}'")
                        word_braille += GRADE2_CONTRACTIONS[contraction]
                        i += len(contraction)
                        contraction_found = True
                        break
                if not contraction_found:
                    # Map individual letters
                    char = word[i]
                    braille_char = GRADE1_BRAILLE.get(char, '')
                    if braille_char:
                        print(f"Letter match: '{char}' -> '{braille_char}'")
                    else:
                        print(f"No Braille mapping for character: '{char}'")
                    word_braille += braille_char
                    i += 1

        braille += word_braille + ' '

    return braille.strip()

def translate_from_braille(braille_text):
    """
    Translates Braille text back to English, handling Grade 2 contractions on a word basis.
    If a word doesn't match a Grade 2 contraction, it is translated letter-by-letter (Grade 1).

    :param braille_text: The Braille text to translate.
    :return: A string representing the English translation.
    """
    text = ''
    words = braille_text.split(' ')  # Use space to split words

    for word in words:
        word_text = ''
        i = 0  # Initialize character pointer
        capitalized = False  # Flag to track capitalization

        while i < len(word):
            # Check for capital sign
            # Handle capital sign
            if word[i] == CAPITAL_SIGN:
                i += 1  # Move to the next character
                if word[i] in BRAILLE_TO_GRADE2:
                    # Translate contraction after capital sign
                    contraction_text = BRAILLE_TO_GRADE2[word[i]]
                    word_text += contraction_text.capitalize()  # Capitalize the contraction
                    i += 1  # Skip the contraction character
                    continue
                else:
                    capitalized = True  # Set capital flag for next individual character   

            # Check for number sign
            if word[i] == NUMBER_SIGN:
                i += 1
                while i < len(word) and word[i] in BRAILLE_NUMBERS.values():
                    for digit, braille_char in BRAILLE_NUMBERS.items():
                        if word[i] == braille_char:
                            word_text += digit
                            break
                    i += 1
                continue

            # Handle Grade 2 contractions
            if word in BRAILLE_TO_GRADE2:
                print(f"Word-level contraction found: '{word}' -> '{BRAILLE_TO_GRADE2[word]}'")
                word_text = BRAILLE_TO_GRADE2[word]
                capitalized = False  # Reset capitalization after applying
                break  # Move to the next word

            # Decode individual letters (Grade 1 Braille)
            char_braille = word[i]
            char_text = BRAILLE_TO_GRADE1.get(char_braille, None)
            if char_text:
                # Apply capitalization if the flag is set
                if capitalized:
                    char_text = char_text.upper()
                    capitalized = False  # Reset capitalization after applying
                word_text += char_text
            else:
                print(f"No English mapping for Braille character: '{char_braille}'")
            i += 1

        text += word_text + ' '

    return text.strip()

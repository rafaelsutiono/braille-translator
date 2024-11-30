# braille_translator.py

# Define Grade 1 Braille mappings (letters and basic punctuation)
GRADE1_BRAILLE = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
    'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
    'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽',
    'z': '⠵',
    ' ': '⠀',
    '.': '⠲', ',': '⠂', ';': '⠆', ':': '⠒', '!': '⠖',
    '(': '⠶', ')': '⠶', '?': '⠦', '\'': '⠄', '-': '⠤',
    '"': '⠶', '/': '⠌', '@': '⠈', '#': '⠼', '*': '⠔',
}

# Define some common Grade 2 Braille contractions
GRADE2_CONTRACTIONS = {
    'and': '⠯',
    'for': '⠿',
    'the': '⠮',
    'with': '⠱',
    'of': '⠷',
    'to': '⠞',
    'but': '⠃',
    'can': '⠉',
    'do': '⠙',
    'go': '⠛',
    'have': '⠓',
    'in': '⠊',
    'it': '⠊',
    'that': '⠹',
    'this': '⠹⠱',  # Example: 'this' as a combination
    'you': '⠽',
    'she': '⠎⠓',
    'he': '⠓',
    'they': '⠮⠽',
    'we': '⠺⠑',
    # Add more contractions as needed
}

# Define the capital sign in Braille
CAPITAL_SIGN = '⠠'

def translate_to_grade2_braille(text):
    """
    Translates English text to a simplified version of Grade 2 Braille.
    Note: This implementation handles only a subset of Grade 2 contractions.

    :param text: The English text to translate.
    :return: A string representing the translated Braille.
    """
    braille = ''
    words = text.split()

    for word in words:
        word_braille = ''
        original_word = word  # Save original for debugging
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
                    # Match contraction only if it fits completely and is bounded
                    if (
                        word[i:contraction_end] == contraction
                        and (contraction_end == len(word) or not word[contraction_end].isalpha())
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

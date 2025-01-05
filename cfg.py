import os
import nltk
from nltk import CFG
from nltk.parse import ChartParser
import re

# Import the Text to Braille translator
from braille_translator import translate_to_grade2_braille

# Import the Braille to Text translator
from braille_translator import translate_from_braille

def read_pos_files(grammar_dir):
    """
    Reads terminal words from separate POS files within the grammar directory.

    :param grammar_dir: Path to the directory containing POS .txt files.
    :return: Dictionary mapping non-terminals to lists of terminal words.
    """
    pos_files = {
        'Vi': 'Vi.txt',
        'Vt': 'Vt.txt',
        'DT': 'DT.txt',
        'NN': 'NN.txt',
        'PRP': 'PRP.txt',
        'PRE': 'PRE.txt',
        'Aux': 'Axv.txt',
        'Adv': 'Adv.txt',
        'CONJ': 'CONJ.txt',
        'NUM':  'NUM.txt',
        'NEG': 'NEG.txt',
        'Adj': 'Adj.txt',
    }

    lexicon = {}

    for non_terminal, filename in pos_files.items():
        file_path = os.path.join(grammar_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                words = [line.strip() for line in file if line.strip()]
                quoted_words = [f"'{word}' | '{word.capitalize()}'" for word in words]
                lexicon[non_terminal] = quoted_words
        except FileNotFoundError:
            print(f"Error: {filename} not found in {grammar_dir}.")
            exit(1)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            exit(1)

    return lexicon

def construct_grammar(lexicon):
    """
    Constructs the CFG grammar string by combining fixed rules with terminal words.

    :param lexicon: Dictionary mapping non-terminals to terminal words.
    :return: A string representing the CFG.
    """
    # Fixed grammar rules
    '''
    S=sentence, VP=verb phrase, NP=noun phrase,
    PP=prepositional phrase, DT=determiner, Vi=intransitive verb,
    Vt=transitive verb, NN=noun, PRP=Pronoun, CONJ=conjunction, Aux=auxiliary verb,
    Adv=adverb, Adj=adjective, PRE=Preposition
    NEG=negatio, NUM=number
    '''
    grammar_rules = """
    S -> NP VP 
    S -> NP
    S -> VP
    S -> NUM
    S -> S CONJ S
    CONJ -> CONJ CONJ

    VP -> Vi
    VP -> Vt
    VP -> Vt NP
    VP -> Vt Adv
    VP -> Aux VP
    VP -> Adj VP
    VP -> Aux NEG VP
    VP -> Vt PP
    VP -> VP CONJ VP
    VP -> VP NEG VP
    VP -> PRE VP

    NP -> DT NN
    NP -> NP PP
    NP -> NN
    NP -> NUM NN
    NP -> NP CONJ NP
    NP -> Adj NN
    NP -> DT Adj NN
    NP -> NP Aux PRP
    NP -> PRP NN

    PP -> PRE NP
    PP -> PRE VP

    NUM -> NUM NUM
    """

    # Add terminal productions from lexicon
    for non_terminal, words in lexicon.items():
        # Join words with ' | ' to denote alternatives
        terminals = ' | '.join(words)
        grammar_rules += f"{non_terminal} -> {terminals}\n"

    return grammar_rules

def preprocess_sentence(sentence):
    """
    Preprocesses a sentence to ensure numbers are separated and properly tokenized.
    """
    sentence = re.sub(r'(\d+)', r' \1 ', sentence)
    return sentence

def custom_tokenize(sentence):
    """
    Custom tokenizer that splits multi-digit numbers into individual digits
    and retains other tokens as-is.

    :param sentence: The input sentence to tokenize.
    :return: A list of tokens.
    """
    tokens = []
    for word in sentence.split():
        if word.isdigit():  # Check if the word is a multi-digit number
            tokens.extend(list(word))  # Split digits into individual tokens
        else:
            tokens.append(word)  # Add non-digit words as-is
    return tokens

def parse_sentence(parser, sentence):
    """
    Parses a sentence and prints all possible parse trees.

    :param parser: An NLTK parser object.
    :param sentence: A string representing the sentence to parse.
    :return: Parsed sentence as a string.
    """
    # Preprocess the sentence to handle numbers correctly
    sentence = preprocess_sentence(sentence)
    
    # tokens = nltk.word_tokenize(sentence)
    tokens = custom_tokenize(sentence)  # Use custom tokenizer
    print(f"\nParsing sentence: '{sentence}'")
    print(f"\nTokenized sentence: {tokens}")
    parse_trees = list(parser.parse(tokens))

    try:
        parse_trees = list(parser.parse(tokens))
    except Exception as e:
        print(f"Error parsing sentence: {e}")
        return None

    if not parse_trees:
        print("No parse trees found.")
        return None
    else:
        for idx, tree in enumerate(parse_trees, 1):
            print(f"\nParse Tree {idx}:")
            print(tree)
            # tree.draw()
        return sentence  # Return the sentence for translation

def main():
    # Ensure NLTK data is downloaded
    # nltk.download('punkt')

    # Define the path to the grammar directory
    grammar_dir = os.path.join(os.getcwd(), 'grammar')

    # Read terminal words from POS files
    lexicon = read_pos_files(grammar_dir)

    # Construct the grammar string
    grammar_string = construct_grammar(lexicon)
    print("Constructed Grammar:\n")
    print(grammar_string)

    # Create CFG
    try:
        grammar = CFG.fromstring(grammar_string)
    except Exception as e:
        print(f"Error constructing CFG: {e}")
        exit(1)

    # Initialize the parser
    parser = ChartParser(grammar)

    # Define sample sentences
    sentences = [
        # S -> NP VP
        "The cat sits",

        # S -> S and S
        "The cat sat and the dog barked",

        # S -> NP Aux not VP
        "The cat did not sit",

        "The cat did not sit",

        "The cat will not eat food",
        # 'The cat wants to eat food',
        'The cat sucks at eating food',

        'The cat will not eat its food',
        'The book is mine',
        'That cat is hers',
        '4 dogs are barking',
        'That dog is mine',
        'cat and dog',
        'angry cat',
        'Will run',
        'Eat food on table'
    ]

    # Define sample Braille sentences (Grade 1 and Grade 2 Braille)
    sample_brailles = [
        # "The cat sits"
        "⠮ ⠉⠁⠞ ⠎⠊⠞⠎",

        # "The cat sat and the dog barked"
        "⠮ ⠉⠁⠞ ⠎⠁⠞ ⠯ ⠮ ⠙⠕⠛ ⠃⠁⠗⠅⠑⠙",

        # "The cat did not sit"
        "⠮ ⠉⠁⠞ ⠙⠊⠙ ⠝⠕⠞ ⠎⠊⠞",

        # "The cat will not eat food"
        "⠮ ⠉⠁⠞ ⠺⠊⠇⠇ ⠝⠕⠞ ⠑⠁⠞ ⠋⠕⠕⠙",

        # "4 dogs are barking"
        "⠼⠙ ⠙⠕⠛⠎ ⠁⠗⠑ ⠃⠁⠗⠅⠊⠝⠛",
        
        # "The book is mine"
        "⠠⠮ ⠃⠕⠕⠅ ⠊⠎ ⠍⠊⠝⠑",

        # "That cat is hers"
        "⠞ ⠉⠁⠞ ⠊⠎ ⠓⠑⠗⠎",
        "⠠⠞ ⠙⠕⠛ ⠊⠎ ⠍⠊⠝⠑",
    ]


    # Parse each sentence and translate to Braille
    for sentence in sentences:
        parsed_sentence = parse_sentence(parser, sentence)
        if parsed_sentence:
            braille_translation = translate_to_grade2_braille(parsed_sentence)
            if braille_translation:
                print("\nGrade 2 Braille Translation:")
                print(braille_translation)
                # Optionally, save the Braille translation to a file
                # with open('braille_output.txt', 'a', encoding='utf-8') as braille_file:
                #     braille_file.write(f"{sentence}\n{braille_translation}\n")

                # # Translate the Braille back to text
                # text_translation = translate_from_braille(braille_translation)
                # if text_translation:
                #     print("\nTranslated Back to Text:")
                #     print(text_translation)
                # else:
                #     print("\nFailed to translate Braille back to text.")
                # Translate each sample Braille sentence back to text
                
    print("\nTranslating Sample Braille Sentences Back to Text:\n")
    for braille_text in sample_brailles:
        print(f"Braille Input: {braille_text}")
        translated_text = translate_from_braille(braille_text)
        print(f"Translated Text: {translated_text}\n")

if __name__ == "__main__":
    main()
    
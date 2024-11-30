import os
import nltk
from nltk import CFG
from nltk.parse import ChartParser

# Import the Braille translator
from braille_translator import translate_to_grade2_braille

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
        'IN': 'IN.txt',
        'Aux': 'Axv.txt',
        'WH': 'WH.txt',
        'PRP': 'PRP.txt',
        'TO': 'TO.txt',
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
    Vt=transitive verb, NN=noun, IN=preposition
    '''
    grammar_rules = """
    S -> WH SSub
    SSub -> IN S
    S -> NP VP
    VP -> Vt NP
    VP -> Vt TO Vi
    NP -> PRP
    NP -> DT NN
    NP -> NP PP
    PP -> IN NP
    """

    # Add terminal productions from lexicon
    for non_terminal, words in lexicon.items():
        # Join words with ' | ' to denote alternatives
        terminals = ' | '.join(words)
        grammar_rules += f"{non_terminal} -> {terminals}\n"

    return grammar_rules

def parse_sentence(parser, sentence):
    """
    Parses a sentence and prints all possible parse trees.

    :param parser: An NLTK parser object.
    :param sentence: A string representing the sentence to parse.
    :return: Parsed sentence as a string.
    """
    tokens = nltk.word_tokenize(sentence)
    print(f"\nParsing sentence: '{sentence}'")
    parse_trees = list(parser.parse(tokens))
    
    if not parse_trees:
        print("No parse trees found.")
        return None
    else:
        for idx, tree in enumerate(parse_trees, 1):
            print(f"\nParse Tree {idx}:")
            print(tree)
            tree.draw()
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
        "i tried to eat the computer",
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

if __name__ == "__main__":
    main()
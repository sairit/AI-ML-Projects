import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S
NP -> Det N | Det Adj N | N | Det N PP | NP PP
VP -> V | V NP | V PP | VP Conj VP
PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    from nltk.tokenize import word_tokenize

    # Tokenizing the sentence
    words = word_tokenize(sentence)

    # Converting to lowercase and filter out words without alphabetic characters
    filtered_words = []
    for word in words:
        word_lower = word.lower()
        contains_alpha = False
        for char in word_lower:
            if char.isalpha():
                contains_alpha = True
                break
        if contains_alpha:
            filtered_words.append(word_lower)

    return filtered_words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    chunks = []

    # Iterating over all subtrees in the tree
    for subtree in tree.subtrees():
        # Checking if the subtree is labeled "NP"
        if subtree.label() == "NP":
            contains_nested_np = False

            # Checking if any child of this subtree is also labeled "NP"
            for child in subtree:
                if isinstance(child, nltk.Tree) and child.label() == "NP":
                    contains_nested_np = True
                    break

            # If no nested NP, adding the subtree to chunks
            if not contains_nested_np:
                chunks.append(subtree)

    return chunks


if __name__ == "__main__":
    main()

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from collections import defaultdict
import nltk
import requests
import json


def get_pos_tokens(sentence):
    """
    Return dictionary, where key is word and value
    is list with Part-Of-Speech tags, index of tag in list
    is order of occurrence
    """
    tokenized_sen = nltk.word_tokenize(sentence)
    tokens_dict = defaultdict(list)
    for word, word_class in nltk.pos_tag(tokenized_sen):
        tokens_dict[word].append(word_class)
    return tokens_dict


def get_pos(word, tokens_dict, order=0):
    word_class = tokens_dict[word][order]
    if word_class in ['NN', 'NNS', 'NNP', 'NNPS']:
        return wn.NOUN
    elif word_class in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
        return wn.VERB
    elif word_class in ['RB', 'RBR', 'RBS']:
        return wn.ADV
    elif word_class in ['JJ', 'JJR', 'JJS']:
        return wn.ADJ


def oxf_2_wn_lex_cat(oxf_class):
    """
    Return lexical category in WordNet form from
    lexical category from Oxford API
    """
    oxf_2_wn = {"Adjective": "JJ", "Adverb": "RB", "Conjuction": "CC",
                "Determiner": "DT", "Idiomatic": "Idiomatic", "Interjection": "UH",
                "Noun": "NN", "Numeral": "CD", "Other": "Other", "Prefix": "Prefix",
                "Preposition": "IN", "Pronoun": "PRP", "Suffix": "Suffix", "Verb": "VB"}
    return oxf_2_wn[oxf_class]


def wn_2_oxf_lex_cat(wn_class):
    wn_2_oxf = {"JJ": "Adjective", "RB": "Adverb", "CC": "Conjuction", "DT": "Determiner",
                "Idiomatic": "Idiomatic", "UH": "Interjection", "NN": "Noun", "CD": "Numeral",
                "Other": "Other", "Prefix": "Prefix", "IN": "Preposition", "PRP": "Pronoun",
                "Suffix": "Suffix", "VB": "Verb"}
    return wn_2_oxf[wn_class]


def get_oxf_definitions(word):
    """
    Get definations of word from Oxford API
    """
    app_id = '0dd8f390'
    app_key = '1671423a9398f671e334350676749918'
    url = "https://od-api.oxforddictionaries.com:443/api/v1/entries/en/" + word
    ret = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    word_definition_dict = defaultdict(list)
    for lexical_category in json.loads(ret.text)["results"][0]["lexicalEntries"]:
        # print("lexicalCategory", lexical_category["lexicalCategory"])
        for definition in lexical_category["entries"][0]["senses"]:
            try:
                wn_lexical_cat = oxf_2_wn_lex_cat(lexical_category["lexicalCategory"])
                word_definition_dict[wn_lexical_cat].append({
                    "definition": definition["definitions"][0],
                    "example": definition["examples"][0]["text"]
                })
                # print("\tDefinition:", definition["definitions"][0])
                # print("\tExample: \"" + definition["examples"][0]["text"] + "\"")
            except KeyError:
                pass
    return word_definition_dict


def lemmatize(word, tokens_dict, order=0):
    pos_tag = get_pos(word, tokens_dict)
    poss_lemm = wn._morphy(word, pos_tag)
    if len(poss_lemm) == 1:
        return poss_lemm[0]
    else:
        if tokens_dict[word][order] == "VBD":
            for w in poss_lemm:
                if w != word:
                    return w
    print(poss_lemm, tokens_dict[word])
    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatized = wordnet_lemmatizer.lemmatize(word, pos_tag)
    return lemmatized


def get_definitions(lemmatized_word, word, tokens_dict):
    """
    Return possible definitions of word in particular sentence
    and original form of word
    """

    return get_oxf_definitions(lemmatized_word)[tokens_dict[word][0][:2]]


def print_definitions(word, sentence, order=0):
    """
    Print possible definition of word in this sentence
    """
    tokens_dict = get_pos_tokens(sentence)
    lemmatized_word = lemmatize(word, tokens_dict, order)
    print("------")
    print("Word: " + lemmatized_word + " (" + wn_2_oxf_lex_cat(tokens_dict[word][order][:2]) + ")")
    print("------")
    for definition_example in get_definitions(lemmatized_word, word, tokens_dict):
        print("Definition: ", definition_example["definition"])
        if "example" in definition_example:
            print("Example: ", definition_example["example"])
        print("------")


sentence = input("Write sentence: ")
word = input("Write unknown word in this sentence: ")
if sentence.count(word) > 1:
    order = int(input("Write order of word in this sentence: "))
    print_definitions(word, sentence, order - 1)
else:
    print_definitions(word, sentence)

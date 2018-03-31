from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
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
    tokens_lst = nltk.pos_tag(tokenized_sen)
    tokens_dict = defaultdict(list)
    for word, word_class in tokens_lst:
        tokens_dict[word].append(word_class)
    return tokens_dict


def get_pos_wn(word, tokens_dict, order=0):
    word_class = tokens_dict[word][order]
    if word_class in ['NN', 'NNS', 'NNP', 'NNPS']:
        return wn.NOUN
    elif word_class in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
        return wn.VERB
    elif word_class in ['RB', 'RBR', 'RBS']:
        return wn.ADV
    elif word_class in ['JJ', 'JJR', 'JJS']:
        return wn.ADJ


def simple_wn_2_oxf(wn_class):
    wn_2_oxf = {wn.ADJ: "Adjective", wn.ADV: "Adverb", wn.NOUN: "Noun",
                wn.VERB: "Verb", wn.ADJ_SAT: "Adjective"}
    return wn_2_oxf[wn_class]

def wn_2_oxf(wn_class):
    wn_2_oxf = {"JJ": "Adjective", "RB": "Adverb", "CC": "Conjuction",
                "DT": "Determiner", "UH": "Interjection", "NN": "Noun",
                "CD": "Numeral", "IN": "Preposition", "PRP": "Pronoun",
                "VB": "Verb"}
    return wn_2_oxf[wn_class]


def lemmatize(word, tokens_dict, order=0):
    pos_tag = get_pos_wn(word, tokens_dict)
    if pos_tag:
        poss_lemm = wn._morphy(word, pos_tag)
    else:
        poss_lemm = ""
    if len(poss_lemm) == 1:
        return poss_lemm[0]
    else:
        if tokens_dict[word][order] == "VBD":
            for w in poss_lemm:
                if w != word:
                    return w
    # print(poss_lemm, tokens_dict[word])
    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatized = wordnet_lemmatizer.lemmatize(word)
    return lemmatized


def get_sen_lemmas(sentence, word, word_order):
    tokens_dict = get_pos_tokens(sentence)
    lemmas_set = set()
    word_lemma = lemmatize(word, tokens_dict, word_order)
    word_pos = get_pos_wn(word, tokens_dict, word_order)

    for token in tokens_dict.keys():
        for order, pos in enumerate(tokens_dict[token]):
            if not (token in punctuation or token in stopwords.words("english")) or token == word:
                lemma = lemmatize(token, tokens_dict, order)
                lemmas_set.add((lemma, get_pos_wn(token, tokens_dict, order)))

    return lemmas_set, (word_lemma, word_pos)


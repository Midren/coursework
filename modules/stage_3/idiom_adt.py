from collections import defaultdict
import json
import auxiliar_functions as af

class IdiomKind:
    INSEPARABLE = "inseparable"
    INTRANSITIVE = "intransitive"
    OBLIGATORY = "separable [obligatory]"
    OPTIONAL = "separable [optional]"
    
class IdiomExpression:
    def __init__(self, name, definition, example, kind):
        self.name = name
        self.lemmatized = af.get_lemmatized_sen(name)
        self.definition = definition
        self.example = example
        self.kind = kind.strip()

    def __repr__(self):
        return "<Idiom: " + self.name + ": " + self.definition + ": " + self.kind + ">"

    def check_sentence(self, lemmatized_sen):
        # print("<"+self.kind+">")
        if self.kind == "inseparable" or self.kind == "intransitive":
            return self._check_inseparable(lemmatized_sen)
        elif self.kind == "separable [optional]":
            return self._check_inseparable(lemmatized_sen) or \
                    self._check_separable(lemmatized_sen)
        elif self.kind == "separable [obligatory]":
            return self._check_separable(lemmatized_sen)

    def _check_inseparable(self, lemmatized_sen):
        # print(lemmatized_sen)
        try:
            st = lemmatized_sen.index(self.lemmatized[0])
        except ValueError:
            return False
        try:
            replacing_words = set(["you", "your", "someone", "something",
                                  "somebody"])
            for word in range(st, st + len(self.lemmatized)):
                if self.lemmatized[word - st] in replacing_words:
                    continue
                if lemmatized_sen[word] != self.lemmatized[word - st]:
                    return False
        except IndexError:
            return False
        return True

    def _check_separable(self, lemmatized_sen):
        pass

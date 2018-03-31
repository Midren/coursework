from collections import defaultdict
import json
import auxiliar_functions as af

class IdiomExpression:
    def __init__(self, name, definition, example, kind):
        self.name = name
        self.lemmatized = af.get_lemmatized_sen(idiom["name"])
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



from time import time
st = time()
idioms = json.loads(open("expressions.json").read().strip())
sentence = """ When I set off for work this morning, my car broke down, so I ended up taking the bus. """.lower()
lemmatized_sen = af.get_lemmatized_sen(sentence)
print(lemmatized_sen)
print("Read from file: ",time() - st)
st = time()
idiom_dict = defaultdict(list)
for idiom in idioms:
    exp = IdiomExpression(idiom["name"], idiom["definition"],
                            idiom["example"], idiom["kind"])
    idiom_dict[exp.name].append(exp)
print("Create dict with idioms", time() - st)
#print(idiom_dict["answer back"][0].check_sentence(lemmatized_sen))
st = time()
for idiom in idiom_dict.keys():
    for exp in idiom_dict[idiom]:
        if exp.check_sentence(lemmatized_sen):
            print(exp)
print("Check sentence", time() - st)
st = time()

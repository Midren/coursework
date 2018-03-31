from collections import defaultdict
from idiom_adt import IdiomExpression, IdiomKind

class IdiomDict:
    def __init__(self):
        self.idioms = defaultdict(list)
        self.kinds = defaultdict(set)
    def __setitem__(self, key, value):
        self.idioms[key].append(value)
        self.kinds[key].add(value.kind)
    def get_kinds(self, key):
        return self.kinds[key]
    def __getitem__(self, key):
        return self.idioms[key]
    def __len__(self):
        return len(self.idioms)
    def __iter__(self):
        return self.idioms.__iter__()

if __name__ == "__main__":
    a = IdiomDict()
    a["set up"] = IdiomExpression("set up", "plant bomb", "I set up", IdiomKind.INSEPARABLE)
    a["set up"] = IdiomExpression("set up", "not plant bomb", "I don't set up", IdiomKind.OBLIGATORY)
    print(a["set up"])
    print(a.get_kinds("set up"))

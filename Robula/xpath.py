import re


class XPath(object):

    def __init__(self, value: str):
        self.value = value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def getValue(self) -> str:
        return self.value

    def startsWith(self, value: str) -> bool:
        return self.value.startswith(value)

    def substring(self, value: int) -> str:
        return self.value[value:]

    def headHasAnyPredicates(self) -> bool:
        return '[' in self.value.split('/')[2]

    def headHasPositionPredicate(self) -> bool:
        splitXPath = self.value.split('/')
        regExp = re.compile(r'\[\d+\]')
        return (
            'position()' in splitXPath[2]
            or 'last()' in splitXPath[2]
            or bool(regExp.search(splitXPath[2]))
        )

    def headHasTextPredicate(self) -> bool:
        return 'text()' in self.value.split('/')[2]

    def addPredicateToHead(self, predicate: str):
        splitXPath = self.value.split('/')
        splitXPath[2] += predicate
        self.value = '/'.join(splitXPath)

    def getLength(self) -> int:
        splitXPath = self.value.split('/')
        length = 0
        for piece in splitXPath:
            if piece:
                length += 1

        return length

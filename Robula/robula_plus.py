from lxml.etree import parse
from lxml.etree import HTMLParser
from lxml.etree import Element
from io import StringIO

from .xpath import XPath


def cmp_to_key(cmp_function):
    """Transfer cmp=func to key=func"""

    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return cmp_function(self.obj, other.obj) < 0

        def __gt__(self, other):
            return cmp_function(self.obj, other.obj) > 0

        def __eq__(self, other):
            return cmp_function(self.obj, other.obj) == 0

        def __le__(self, other):
            return cmp_function(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return cmp_function(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return cmp_function(self.obj, other.obj) != 0

    return K


class RobulaPlusOptions(object):
    """
    :attribute - attributePriorizationList: A prioritized list of HTML attributes,
                which are considered in the given order.
    :attribute - attributeBlackList: Contains HTML attributes,
                 which are classified as too fragile and are ignored by the algorithm.

    """

    def __init__(self):
        self.attributePriorizationList = ['name', 'class', 'title', 'alt', 'value']
        self.attributeBlackList = [
            'href',
            'src',
            'onclick',
            'onload',
            'tabindex',
            'width',
            'height',
            'style',
            'size',
            'maxlength',
            'data-io-article-url'
        ]


class RobulaPlus(object):
    def __init__(self, options: RobulaPlusOptions = None):
        if not options:
            self.attributePriorizationList = ['name', 'class', 'title', 'alt', 'value']
            self.attributeBlackList = [
                'href',
                'src',
                'onclick',
                'onload',
                'tabindex',
                'width',
                'height',
                'style',
                'size',
                'maxlength',
                'data-io-article-url'
            ]
        else:
            self.attributePriorizationList = options.attributePriorizationList
            self.attributeBlackList = options.attributeBlackList

    def makeDocument(self, document: str) -> Element:
        parser = HTMLParser()
        return parse(StringIO(document), parser=parser)

    def getElementByXPath(self, xPath: str, document: Element) -> Element:
        """
        Returns an element in the given document located by the given xPath locator.

        :param xPath - A xPath string, describing the desired element.
        :param document - The document to analyse, that contains the desired element.

        :return - The first maching Element located.
        """
        elements = document.xpath(xPath)
        if len(elements) == 0:
            raise ValueError(f"Wrong Xpath, coudn`t get data by XPath: {xPath}")
        else:
            return elements[0]

    def uniquelyLocate(self, xPath: str, element: Element, document: Element) -> bool:
        elements = document.xpath(xPath)
        return len(elements) == 1 and elements[0] == element

    def getAncestor(self, element: Element, index: int) -> Element:
        output = element
        for i in range(0, index):
            output = output.getparent()

        return output

    def getAncestorCount(self, element: Element) -> int:
        count = 0
        while element.getparent() is not None:
            element = element.getparent()
            count += 1

        return count

    def transfConvertStar(self, xPath: XPath, element: Element) -> list:
        output = []
        ancestor = self.getAncestor(element, xPath.getLength() - 1)
        if xPath.startsWith('//*'):
            output.append(XPath('//' + ancestor.tag.lower() + xPath.substring(3)))

        return output

    def transfAddId(self, xPath: XPath, element: Element) -> list:
        output = []
        ancestor = self.getAncestor(element, xPath.getLength() - 1)
        _id = ancestor.get('id')
        if _id and not xPath.headHasAnyPredicates():
            newXPath = XPath(xPath.getValue())
            newXPath.addPredicateToHead(f'[@id="{_id}"]')
            output.append(newXPath)

        return output

    def transfAddAttribute(self, xPath: XPath, element: Element) -> list:
        output = []
        ancestor: Element = self.getAncestor(element, xPath.getLength() - 1)
        if not xPath.headHasAnyPredicates():
            # add priority attributes to output
            for priorityAttribute in self.attributePriorizationList:
                for attribute_name, attribute_value in ancestor.attrib.items():
                    if attribute_name == priorityAttribute:
                        newXPath = XPath(xPath.getValue())
                        newXPath.addPredicateToHead(f"[@{attribute_name}='{attribute_value}']")
                        output.append(newXPath)
                        break

        # append all other non-blacklist attributes to output
        for attribute_name, attribute_value in ancestor.attrib.items():
            if attribute_name not in self.attributeBlackList and attribute_name not in self.attributePriorizationList:
                newXPath = XPath(xPath.getValue())
                newXPath.addPredicateToHead(f"[@{attribute_name}='{attribute_value}']")
                output.append(newXPath)
        return output

    def transfAddPosition(self, xPath: XPath, element: Element) -> list:
        output = []
        position = 0
        ancestor = self.getAncestor(element, xPath.getLength() - 1)
        if not xPath.headHasPositionPredicate():
            position = 1

        if xPath.startsWith('//*'):
            position = ancestor.getparent().getchildren().index(ancestor) + 1

        else:
            for child in ancestor.getparent().getchildren():
                if ancestor == child:
                    break

                if ancestor.tag == child.tag:
                    position += 1

        newXPath = XPath(xPath.getValue())
        newXPath.addPredicateToHead(f"[{position}]")
        output.append(newXPath)
        return output

    def transfAddLevel(self, xPath: XPath, element: Element) -> list:
        output = []
        if xPath.getLength() - 1 < self.getAncestorCount(element):
            output.append(XPath('//*' + xPath.substring(1)))

        return output

    def generatePowerSet(self, a: list) -> list:
        """generate all combinations"""
        if len(a) == 0:
            return [[]]
        cs = []
        for c in self.generatePowerSet(a[1:]):
            cs += [c, c + [a[0]]]
        return cs

    def elementCompareFunction(self, attr1: dict, attr2: dict) -> int:
        for element in self.attributePriorizationList:
            if element == attr1["name"]:
                return -1

            if element == attr2["name"]:
                return 1

        return 0

    def compareListElementAttributes(self, set1: list, set2: list) -> int:
        if len(set1) < len(set2):
            return -1

        if len(set1) > len(set2):
            return 1

        for i in range(0, len(set1)):
            if set1[i] != set2[i]:
                return self.elementCompareFunction(set1[i], set2[i])

        return 0

    def transfAddAttributeSet(self, xPath: XPath, element: Element) -> list:
        output = []
        ancestor = self.getAncestor(element, xPath.getLength() - 1)
        if not xPath.headHasAnyPredicates():
            # add id to attributePriorizationList
            self.attributePriorizationList.insert(0, 'id')

            attributes = ancestor.attrib

            # remove black list attributes
            attributes = [{"name": k, "value": v} for k, v in attributes.items() if k not in self.attributeBlackList]

            # generate power set
            attributePowerSet = self.generatePowerSet(attributes)

            # remove sets with cardinality < 2
            attributePowerSet = [s for s in attributePowerSet if len(s) >= 2]

            # sort elements inside each powerset
            for i, attributeSet in enumerate(attributePowerSet):
                attributePowerSet[i] = sorted(attributeSet, key=cmp_to_key(self.elementCompareFunction))

            # sort attributePowerSet
            attributePowerSet = sorted(attributePowerSet, key=cmp_to_key(self.compareListElementAttributes))

            # remove id from attributePriorizationList
            self.attributePriorizationList.pop(0)

            # convert to predicate
            for attributeSet in attributePowerSet:
                key = attributeSet[0]['name']
                value = attributeSet[0]['value']
                predicate = f"[@{key}='{value}'"

                for i in range(1, len(attributeSet)):
                    key = attributeSet[i]['name']
                    value = attributeSet[i]['value']
                    predicate += f" and @{key}='{value}'"

                predicate += ']'
                newXPath = XPath(xPath.getValue())
                newXPath.addPredicateToHead(predicate)
                output.append(newXPath)

        return output

    def getRobustXPath(self, element: Element, document: Element) -> str:

        xPathList = [XPath('//*')]
        while len(xPathList) > 0:
            xPath = xPathList.pop(0)
            temp = []
            temp.extend(self.transfConvertStar(xPath, element))
            temp.extend(self.transfAddId(xPath, element))
            temp.extend(self.transfAddAttribute(xPath, element))
            temp.extend(self.transfAddAttributeSet(xPath, element))
            temp.extend(self.transfAddPosition(xPath, element))
            temp.extend(self.transfAddLevel(xPath, element))
            temp = sorted(set(temp), key=lambda key: len(key.getValue()))  # removes duplicates and sort by len

            for x in temp:
                if self.uniquelyLocate(x.getValue(), element, document):
                    return x.getValue()

                xPathList.append(x)

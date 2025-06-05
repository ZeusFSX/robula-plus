import pytest
from Robula.xpath import XPath


def test_xpath_basic():
    xp = XPath('//div')
    assert xp.getValue() == '//div'
    assert xp.startsWith('//')
    assert xp.substring(2) == 'div'
    assert not xp.headHasAnyPredicates()
    xp.addPredicateToHead("[@id='x']")
    assert xp.getValue() == "//div[@id='x']"
    assert xp.headHasAnyPredicates()
    assert not xp.headHasTextPredicate()


def test_xpath_text_predicate_and_length():
    xp = XPath('//*[text()="a"]/span')
    assert xp.headHasTextPredicate()
    assert xp.getLength() == 2


def test_xpath_position_predicate():
    assert XPath('//div[2]').headHasPositionPredicate()
    assert XPath('//*[last()]').headHasPositionPredicate()
    assert XPath('//*[position()=1]').headHasPositionPredicate()
    assert not XPath('//*[@id="x"]').headHasPositionPredicate()

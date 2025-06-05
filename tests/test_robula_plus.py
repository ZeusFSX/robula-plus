import pytest
from lxml.etree import _Element as Element
from Robula.robula_plus import RobulaPlus, cmp_to_key
from Robula.xpath import XPath

HTML_DOC = (
    "<html><body>"
    "<div id='id1' class='foo' title='bar'><span>hello</span></div>"
    "<div class='foo' name='second'><span>bye</span></div>"
    "</body></html>"
)

FULL_HTML_DOC = (
    "<html><body>"
    "<div class='product-link'></div>"
    "<div><div>"
    "<li><a href='#'>one</a></li>"
    "<li><a href='#'>two</a></li>"
    "<li><a class='product-link'>three</a></li>"
    "</div></div>"
    "</body></html>"
)

@pytest.fixture
def rp_doc():
    rp = RobulaPlus()
    doc = rp.makeDocument(HTML_DOC)
    return rp, doc

def test_make_document_and_get_element_by_xpath(rp_doc):
    rp, doc = rp_doc
    el = rp.getElementByXPath('//div', doc)
    assert isinstance(el, Element)
    with pytest.raises(ValueError):
        rp.getElementByXPath('//unknown', doc)

def test_uniquely_locate(rp_doc):
    rp, doc = rp_doc
    el1 = doc.xpath('//div')[0]
    assert rp.uniquelyLocate('//*[@id="id1"]', el1, doc)
    assert not rp.uniquelyLocate('//div', el1, doc)

def test_get_ancestor_and_count(rp_doc):
    rp, doc = rp_doc
    el = doc.xpath('//div/span')[0]
    assert rp.getAncestor(el, 1).tag == 'div'
    assert rp.getAncestor(el, 2).tag == 'body'
    assert rp.getAncestorCount(el) == 3

def test_transforms(rp_doc):
    rp, doc = rp_doc
    el1 = doc.xpath('//div')[0]
    # convert star
    res = rp.transfConvertStar(XPath('//*'), el1)
    assert res[0].getValue() == '//div'
    assert rp.transfConvertStar(XPath('//div'), el1) == []
    # add id
    res = rp.transfAddId(XPath('//*'), el1)
    assert any(x.getValue().replace('"', "'") == "//*[@id='id1']" for x in res)
    # add attribute
    res = rp.transfAddAttribute(XPath('//*'), el1)
    vals = [x.getValue() for x in res]
    assert "//*[@class='foo']" in vals
    assert "//*[@title='bar']" in vals
    assert any(v.replace('"', "'") == "//*[@id='id1']" for v in vals)
    # add position
    res = rp.transfAddPosition(XPath('//*'), el1)
    assert res[0].getValue() == '//*[1]'
    el2 = doc.xpath('//div')[1]
    res2 = rp.transfAddPosition(XPath('//div'), el2)
    assert res2[0].getValue() == '//div[2]'
    # add level
    res = rp.transfAddLevel(XPath('//div'), el1)
    assert res[0].getValue() == '//*/div'

def test_generate_power_set_and_compare_functions():
    rp = RobulaPlus()
    assert rp.generatePowerSet([1,2]) == [[], [1], [2], [2,1]]
    a1 = {'name':'name','value':'x'}
    a2 = {'name':'other','value':'y'}
    assert rp.elementCompareFunction(a1,a2) == -1
    assert rp.elementCompareFunction(a2,a1) == 1
    assert rp.elementCompareFunction(a2,a2) == 0
    assert rp.compareListElementAttributes([a1], [a1,a2]) == -1
    assert rp.compareListElementAttributes([a1,a2], [a1]) == 1
    assert rp.compareListElementAttributes([a1], [a1]) == 0

def test_transf_add_attribute_set(rp_doc):
    rp, doc = rp_doc
    el = doc.xpath('//div')[0]
    res = rp.transfAddAttributeSet(XPath('//*'), el)
    values = [x.getValue() for x in res]
    assert "//*[@id='id1' and @class='foo']" in values

def test_get_robust_xpath(rp_doc):
    rp, doc = rp_doc
    el1, el2 = doc.xpath('//div')
    assert rp.getRobustXPath(el1, doc).replace('"', "'") == "//*[@id='id1']"
    assert rp.getRobustXPath(el2, doc) == '//*[2]'

def test_cmp_to_key_sorting():
    def reverse_cmp(a, b):
        return (b - a)
    values = [1,3,2]
    sorted_vals = sorted(values, key=cmp_to_key(reverse_cmp))
    assert sorted_vals == [3,2,1]


def test_full_example_xpath_reduction():
    rp = RobulaPlus()
    doc = rp.makeDocument(FULL_HTML_DOC)
    element = doc.xpath('/html/body/div/div[1]/li[3]/a')[0]
    assert rp.getRobustXPath(element, doc) == "//a[@class='product-link']"

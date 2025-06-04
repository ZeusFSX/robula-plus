import unittest
from Robula.robula_plus import RobulaPlus
from Robula.xpath import XPath

from lxml.etree import HTML

class TestRobula(unittest.TestCase):
    def test_transf_add_attribute_set(self):
        rp = RobulaPlus()
        doc = rp.makeDocument('<html><body><div id="id1" class="foo"></div></body></html>')
        el = doc.xpath('//div')[0]
        results = rp.transfAddAttributeSet(XPath('//*'), el)
        values = [x.getValue() for x in results]
        self.assertIn("//*[@id='id1' and @class='foo']", values)

    def test_head_has_position_predicate(self):
        self.assertTrue(XPath('//div[2]').headHasPositionPredicate())
        self.assertTrue(XPath('//*[last()]').headHasPositionPredicate())
        self.assertTrue(XPath('//*[position()=1]').headHasPositionPredicate())
        self.assertFalse(XPath('//*[@id="x"]').headHasPositionPredicate())

if __name__ == '__main__':
    unittest.main()

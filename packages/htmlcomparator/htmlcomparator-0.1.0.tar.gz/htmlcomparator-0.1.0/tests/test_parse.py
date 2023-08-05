import unittest
from htmlcomparator import *


class TestBasic(unittest.TestCase):
    def test_tag(self):
        s1 = "<html><head><title>Test</title></head></html>"
        s2 = "<html><head><title>Test</title></head></html>"
        comparator = HTMLComparator()
        self.assertTrue(comparator.compare(s1,s2))

    def test_decl(self):
        s1 = "<!DOCTYPE html> <head> </head>"
        s2 = "<!DOCTYPE html> <head>  </head>"
        comparator = HTMLComparator()
        self.assertTrue(comparator.compare(s1,s2))

    def test_decl_2(self):
        s1 = "<!DOCTYPE xml> "
        s2 = "<!DOCTYPE html> <head> </head>"
        comparator = HTMLComparator()
        self.assertFalse(comparator.compare(s1,s2))
    
    def test_decl_diff(self):
        s1 = "<!DOCTYPE xml> "
        s2 = "<!DOCTYPE html>"
        comparator = HTMLComparator()
        self.assertEqual(comparator.compare(s1,s2, compare_type = "all", quick_compare = False),
                        "@@ DOCTYPE Difference @@\n*DOCTYPE xml\n-DOCTYPE html\n\n")

    def test_diff_data(self):
        s1 = "<html><div><title>Test</title></div>"
        s2 = "<html><div><title>test</title></div>"
        comparator = HTMLComparator()
        self.assertFalse(comparator.compare(s1,s2))
    
    def test_file_input(self):
        with open("tests/test1.html") as f1:
            with open("tests/test2.html") as f2:
                comparator = HTMLComparator()
                self.assertFalse(comparator.compare(f1,f2))
    

class TestTags(unittest.TestCase):
    def test_parallel_tag(self):
        s1 = "<head><title>Test</title></head> <body> test </body>"
        s2 = "<head><title>Test</title>   </head> <body> test </body>"
        comparator = HTMLComparator()
        self.assertTrue(comparator.compare(s1,s2))

    def test_spaces_between_tag(self):
        s1 = "     <html>  <head><title>Test</title>   </head>"
        s2 = "<html><head><title>Test   </title></head>   "
        comparator = HTMLComparator()
        self.assertTrue(comparator.compare(s1,s2))
    
    def test_tag(self):
        s1 = "<html><div><title>Test</title></div></html>"
        s2 = "<html><head><title>Test</title></head></html>"
        comparator = HTMLComparator()
        self.assertFalse(comparator.compare(s1,s2))

    def test_children(self):
        s1 = "<html> <p> test </p> </html>"
        s2 = "<html> <head> </head> <p> test </p> </html>"
        comparator = HTMLComparator()
        self.assertFalse(comparator.compare(s1,s2))

    def test_tag_diff(self):
        s1 = "<html><div><title>Test</title></div></html>"
        s2 = "<html><head><title>Test</title></head></html>"
        comparator = HTMLComparator()
        self.assertEqual(comparator.compare(s1,s2, compare_type = "tag", quick_compare = False),
                        "@@ (1, 6) , (1, 6) @@\n<div> vs <head>\n\n")

    def test_same(self):
        s1 = "     <html>  <head><title>Test</title>   </head>"
        s2 = "<html><head><title>Test   </title></head>   "
        comparator = HTMLComparator()
        self.assertEqual(comparator.compare(s1,s2, compare_type = "all", quick_compare = False), "")

class TestErrors(unittest.TestCase):
    def test_malformed(self):
        s1 = "<html> <head> </body> </html>"
        s2 = "<html> </html>"
        comparator = HTMLComparator()
        with self.assertRaises(ParsingError):
            comparator.compare(s1, s2)

    def test_unexpected_data(self):
        s1 = " data <html> </html>"
        s2 = " "
        comparator = HTMLComparator()
        with self.assertRaises(ParsingError):
            comparator.compare(s1, s2)

    def test_unexpected_data_2(self):
        s1 = "<html> </html> data2"
        s2 = "<html> </html>"
        comparator = HTMLComparator()
        with self.assertRaises(ParsingError):
            comparator.compare(s1, s2)

    def test_invalid_input(self):
        comparator = HTMLComparator()
        with self.assertRaises(TypeError):
            comparator.compare(1, 1)

class TestAttrs(unittest.TestCase):
    def test_single_attr(self):
        s1 = '<p style="color:red"> test </p>'
        s2 = '<p     style="color:red"> test </p>'
        comparator = HTMLComparator()
        self.assertTrue(comparator.compare(s1,s2))
    
    def test_attr(self):
        s1 = '<p style="color:red"> test </p>'
        s2 = '<p title="test difference"> test </p>'
        comparator = HTMLComparator()
        self.assertFalse(comparator.compare(s1,s2))
    
    def test_empty(self):
        s1 = '<p style=""> test </p>'
        s2 = '<p > test </p>'
        comparator = HTMLComparator()
        self.assertTrue(comparator.compare(s1,s2))

    def test_attr_diff(self):
        s1 = '<p style="color:red"> test </p>'
        s2 = '<p title="test difference"> test </p>'
        comparator = HTMLComparator()
        self.assertEqual(comparator.compare(s1,s2, compare_type = "all", quick_compare = False),
                        "@@ (1, 0) , (1, 0) @@\n*{'style': 'color:red'}\n-{'title': 'test difference'}\n\n")

class TestData(unittest.TestCase):
    def test_data_diff(self):
        s1 = "<html><div><title>Test</title></div>"
        s2 = "<html><div><title>test</title></div>"
        comparator = HTMLComparator()
        self.assertEqual(comparator.compare(s1,s2, compare_type = "data", quick_compare = False),
                        "@@ (1, 18) , (1, 18) @@\n*Test\n-test\n\n")
                    
class TestAdvanced(unittest.TestCase):
    def test_mixed_diff(self):
        s1 = "<!DOCTYPE xml> <head> <p> Test </p> <p> different here </p> </head>"
        s2 = "<!DOCTYPE html> <head> <p> test </p> </head>"
        comparator = HTMLComparator()
        self.assertEqual(comparator.compare(s1,s2, compare_type = "all", quick_compare = False),
                        "@@ DOCTYPE Difference @@\n*DOCTYPE xml\n-DOCTYPE html\n\nextra tag <p> in the first html at (1, 36)\n\n@@ (1, 25) , (1, 26) @@\n*Test\n-test\n\n")
    
    def test_extra_data(self):
        s1 = "<p> </p>"
        s2 = "<p> extra </p>"
        comparator = HTMLComparator()
        self.assertEqual(comparator.compare(s1,s2, compare_type = "data", quick_compare = False),
                        "@@ None , (1, 3) @@\n*\n-extra\n\n")

    def test_no_attr(self):
        s1 = '<head style="lalala"> <p> Test </p> <p> different here </p> </head>'
        s2 = '<head style="papapa"> <p> test </p> </head>'
        comparator = HTMLComparator()
        self.assertEqual(comparator.compare(s1, s2, compare_type = "data", quick_compare = False),
                        "extra tag <p> in the first html at (1, 36)\n\n@@ (1, 25) , (1, 25) @@\n*Test\n-test\n\n")

if __name__ == "__main__":
    unittest.main()
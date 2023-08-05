from html.parser import HTMLParser
import io

class Node:
    def __init__(self, tag="", attrs={}):
        self.tag = tag
        self.attrs = {}
        for p in attrs:
            if p[1].strip() == "":
                continue
            self.attrs[p[0]] = p[1]
        self.data = "" 
        self.children = []

        self.startPos = None 
        self.dataPos = None
        self.endPos = None

    def add_data(self, data):
        self.data = data

class HTMLTree:
    def __init__(self):
        self.root = Node() 
        self.decl = "" 
    
    
class ParseToTree(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tree = HTMLTree()
        self.stack = [self.tree.root]

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs)
        n.startPos = self.getpos()
        if self.stack:
            self.stack[-1].children.append(n)
        self.stack.append(n)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1].tag != tag:
            raise ParsingError("Malformed HTML file. Unexpected end tag: " + tag)
        self.stack.pop()

    def handle_data(self, data):
        data = data.strip()
        if data == "":
            return
        if not self.stack or self.stack[-1] == self.tree.root:
            raise ParsingError("Unexpected data block. Parsing falied.")
        self.stack[-1].add_data(data)
        self.stack[-1].dataPos = self.getpos()

    def handle_decl(self, decl):
        self.tree.decl = decl

class Difference:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.rec = []
        self.type_diff = None 

    def add_tag_diff(self, n1, n2):
        self.rec.append(("t", n1, n2))
    
    def add_attr_diff(self, n1, n2):
        self.rec.append(("a", n1, n2))
    
    def add_data_diff(self, n1, n2):
        self.rec.append(("d", n1, n2))

    def to_string(self, types = "all"):
        res = ""
        if not self.type_diff and not self.rec:
            return res
        if self.type_diff:
            d1 = self.type_diff[0]
            d2 = self.type_diff[1]
            res += "@@ DOCTYPE Difference @@\n"
            res += "*" + d1.rjust(1, "*") + "\n"
            res += "-" + d2.rjust(1, "-") + "\n\n"

        if types == "tag":
            for d in self.rec:
                if d[0] == "t":
                    res += self.format_tag(d)
        elif types == "data":
            for d in self.rec:
                if d[0] == "t":
                    res += self.format_tag(d)
                elif d[0] == "d":
                    res += self.format_data(d) 
        elif types == "all":
            for d in self.rec:
                if d[0] == "t":
                    res += self.format_tag(d)
                elif d[0] == "d":
                    res += self.format_data(d) 
                else:
                    res += self.format_attr(d)
        else:
            raise ParsingError("{} is not a valid argument".format(types))

        return res
    
    def format_tag(self, diff):
        n1 = diff[1]
        n2 = diff[2]
        res = ""
        if n1 and n2:
            res += "@@ {} , {} @@\n".format(n1.startPos, n2.startPos)
            res += "<{}> vs <{}>\n\n".format(n1.tag, n2.tag)
        elif n1:
            res += "extra tag <{}> in the first html at {}\n\n".format(n1.tag, n1.startPos)
        else:
            res += "extra tag <{}> in the second html at {}\n\n".format(n2.tag, n2.startPos)
        return res

    def format_data(self, diff):
        n1 = diff[1]
        n2 = diff[2]
        res = ""
        if n1.dataPos and n2.dataPos:
            res += "@@ {} , {} @@\n".format(n1.dataPos, n2.dataPos)
        elif n1.dataPos:
            res += "@@ {} , {} @@\n".format(n1.dataPos, "None")
        else:
            res += "@@ {} , {} @@\n".format("None", n2.dataPos)
        res += "*" + "*".join(n1.data.splitlines(True)) + "\n"
        res += "-" + "-".join(n2.data.splitlines(True)) + "\n\n"
        return res

    def format_attr(self, diff):
        n1 = diff[1]
        n2 = diff[2]
        res = "@@ {} , {} @@\n".format(n1.startPos, n2.startPos)
        res += "*" + str(n1.attrs)+ "\n"
        res += "-" + str(n2.attrs)+ "\n\n"
        return res


class HTMLComparator:
    def __init__(self):
        self.diff = Difference()

    def compare(self, o1, o2, quick_compare = True, compare_type = "all"):
        if type(o1) == str and type(o2) == str:
            c1 = o1
            c2 = o2 
        elif isinstance(o1, io.IOBase) and isinstance(o2,io.IOBase):
            c1 = o1.read()
            c2 = o2.read()
        else:
            raise TypeError("arguments are not file objects or strings")

        tree1 = ParseToTree()
        tree1.feed(c1)

        tree2 = ParseToTree()
        tree2.feed(c2)

        if quick_compare:
            return self._quick_compare_trees(tree1, tree2)
        else:
            self._compare_difference(tree1, tree2)
            res = self.diff.to_string(compare_type)
            self.diff.reset()
            return res

    def _quick_compare_trees(self, t1, t2):
        if t1.tree.decl != t2.tree.decl:
            return False
        queue1 = [t1.tree.root]
        queue2 = [t2.tree.root]
        while queue1 and queue2:
            node1 = queue1.pop(0)
            node2 = queue2.pop(0)
            if node1.tag != node2.tag:
                return False
            elif node1.data != node2.data:
                return False
            elif node1.attrs != node2.attrs:
                return False

            if len(node1.children) != len(node2.children):
                return False
            else:
                queue1 += node1.children
                queue2 += node2.children
        return True

    def _compare_difference(self, t1, t2):
        if t1.tree.decl != t2.tree.decl:
            self.diff.type_diff = (t1.tree.decl, t2.tree.decl) 
        queue1 = [t1.tree.root]
        queue2 = [t2.tree.root]
        while queue1 and queue2:
            node1 = queue1.pop(0)
            node2 = queue2.pop(0)
            if node1.tag != node2.tag:
                self.diff.add_tag_diff(node1, node2)
            else:
                if node1.data != node2.data:
                    self.diff.add_data_diff(node1, node2)
                if node1.attrs != node2.attrs:
                    self.diff.add_attr_diff(node1, node2)

            if len(node1.children) != len(node2.children):
                length = min(len(node1.children), len(node2.children))
                queue1 += node1.children[:length]
                queue2 += node2.children[:length]
                if len(node1.children) > len(node2.children):
                    for i in range(length, len(node1.children)):
                        self.diff.add_tag_diff(node1.children[i], None)
                else:
                    for i in range(length, len(node2.children)):
                        self.diff.add_tag_diff(None, node2.children[i])
            else:
                queue1 += node1.children
                queue2 += node2.children

class ParsingError(Exception):
    pass


if __name__ == "__main__":
    # s1 = '<p style="color:red"> test </p>'
    # s2 = '<p title="test difference"> test </p>'
    # comparator = HTMLComparator()
    # print(comparator.compare(s1,s2, compare_type = "all", quick_compare = False))

    s1 = "<!DOCTYPE xml> <head> <p> Test </p> <p> different here </p> </head>"
    s2 = "<!DOCTYPE html> <head> <p> test </p> </head>"
    comparator = HTMLComparator()
    print(comparator.compare(s1,s2, compare_type = "all", quick_compare = False))
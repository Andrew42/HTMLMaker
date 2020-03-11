import os

from BaseTags import BaseHTMLTag

INDENT_SIZE = " "*4

#NOTE: We use an alternate form of the dumpTag method, as a consequence VoidTags can't have nested tags
class VoidTag(BaseHTMLTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = None

    def dumpTag(self,depth=0):
        indent = INDENT_SIZE*depth*int(self.pretty_print)
        string = "{}<{tag}".format(indent,tag=self.tag_name)
        for k,v in self.getAttributes().iteritems():
            string += " {key}={val}".format(key=k,val=self.attr2Str(k,v))
        string += ">\n"
        return string

class MetaTag(VoidTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "meta"

class LinkTag(VoidTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "link"

class ImgTag(VoidTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "img"

class InputTag(VoidTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "input"
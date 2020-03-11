import os

from BaseTags import HTMLTag, HeadTag, BodyTag

class HTMLGenerator:
    def __init__(self,doc_type="<!DOCTYPE html>"):
        self.doc_type = doc_type
        self.html = HTMLTag()
        self.html.setPrettyPrint(True)

        # Our html files always have a <head> tag
        self.head_tag_index = len(self.html.getTags())
        self.html.addTag(HeadTag())

        # Our html files always have a <body> tag
        self.body_tag_index = len(self.html.getTags())
        self.html.addTag(BodyTag())

    # Returns the head tag of the html file
    def getHeadTag(self):
        return self.html.nested_tags[self.head_tag_index]

    # Returns the body tag of the html file
    def getBodyTag(self):
        return self.html.nested_tags[self.body_tag_index]

    # Add a generic tag to the head section of the html file
    def addHeadTag(self,new_tag):
        head_tag = self.getHeadTag()
        head_tag.addTag(new_tag)

    # Add a generic tag to the body section of the html file
    def addBodyTag(self,new_tag):
        body_tag = self.getBodyTag()
        body_tag.addTag(new_tag)

    # TODO: Should probably remove this, since it can be done using the addHeadTag() method instead
    # Adds a link tag to the head section of the html file
    # def addLinkTag(self,_rel,_type,_href,opts={}):
    #     link_tag = LinkTag()
    #     link_tag.addAttributes(rel=_rel,type=_type,href=_href)
    #     if opts: new_link_tag.addAttributes(**opts)
    #     self.addHeadTag(link_tag)

    # Dumps the entire html file to a string
    def dumpHTML(self):
        string = ""
        string += self.doc_type
        string += "\n"
        string += self.html.dumpTag()
        return string

    # Saves the entire html file to a specified file
    def saveHTML(self,f_name='index.html',f_dir='.'):
        #output = self.html.dumpTag()
        output = self.dumpHTML()
        f_path = os.path.join(f_dir,f_name);
        
        print "Saving HTML output to: %s" % f_path
        
        #html_file = open(f_path,'wb')
        html_file = open(f_path,'w')
        html_file.write(output)
        html_file.close()

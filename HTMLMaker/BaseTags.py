import os

INDENT_SIZE = " "*4

# A base class to generate html content
class BaseHTMLTag:
    CLASS_TRANSLATION = ["cls"]     # List of strings to check against to replace with 'class', b/c thats a protected word in python
    def __init__(self):
        self.tag_name = ""
        self.tag_content = ""
        self.nested_tags = []       # This is an ordered list!
        self.tag_attributes = {}

        self.pretty_print = False   # Whether or not to indent the tag (this option gets passed down to all child tags)

    # Sets the tag content
    def setContent(self,content):
        self.tag_content = content

    # Return the tag content in a string format
    def getContent(self):
        return str(self.tag_content)

    # Check if the tag has the corresponding attribute
    def hasAttribute(self,k):
        return self.tag_attributes.has_key(k)

    # Adds new attribute:value pairs to this tag
    def addAttributes(self,**kwargs):
        for k,v in kwargs.iteritems():
            # Skip already defined attributes
            if k in self.CLASS_TRANSLATION: k = 'class'
            if self.hasAttribute(k): continue 
            self.tag_attributes[k] = v

    # Modify existing attributes (if found)
    def setAttributes(self,**kwargs):
        for k,v in kwargs.iteritems():
            if not self.hasAttribute(k): continue
            self.tag_attributes[k] = v

    # Get the attributes dictionary
    def getAttributes(self):
        return self.tag_attributes

    # Add a new nested tag, the child tag inherits the parent's pretty_print option
    def addTag(self,child_tag):
        child_tag.setPrettyPrint(self.pretty_print)
        self.nested_tags.append(child_tag)

    # Return the list of nested tags
    def getTags(self):
        return self.nested_tags

    # Remove all nested tags from this tag
    def clearTags(self):
        self.nested_tags = []

    # Set the tag to dump strings with indentation or not
    def setPrettyPrint(self,b):
        self.pretty_print = bool(b)

    # Convers an attribute:value pair to a string
    def attr2Str(self,k,v):
        # For now we don't do anything with the attr name
        if isinstance(v,int):
            return "%d" % (v)
        elif isinstance(v,str):
            return "\"%s\"" % (v)
        else:
            return "\"%s\"" % (str(v))

    # Check if this tag is an empty tag (i.e. no content and no nested tags)
    def isEmptyTag(self):
        return (self.getContent() == "" and len(self.getTags()) == 0)

    # Dumps the tag (and all nested tags) info to a string
    def dumpTag(self,depth=0):
        indent = INDENT_SIZE*depth*int(self.pretty_print)
        # Empty tags don't get indented, might want to change this at some point
        string = "<%s" % (self.tag_name) if self.isEmptyTag() else "%s<%s" % (indent,self.tag_name)
        for k,v in self.getAttributes().iteritems():
            string += " %s=%s" % (k,self.attr2Str(k,v))
        if self.isEmptyTag(): return string+"/>"
        string += ">"
        if len(self.getTags()) == 0:
            # For now, only tags with no nested tags can have content
            content = self.getContent()
            lines = content.strip().split('\n')
            if len(lines) > 1 and self.pretty_print:    # Indent content of tags that is multi-line
                content = "\n"
                for l in lines:
                    content += "%s%s\n" % (indent+INDENT_SIZE,l) if len(l) else "\n"
                content += "%s" % (indent)              # This is so the closing tag gets indented properly
            string += "%s</%s>\n" % (content,self.tag_name)
            return string
        string += "\n"
        for tag in self.getTags():
            string += tag.dumpTag(depth=depth+1)
        string += "%s</%s>\n" % (indent,self.tag_name)
        return string

class BreakTag(BaseHTMLTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "br"

class StyleTag(BaseHTMLTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "style"

class HyperLinkTag(BaseHTMLTag):
    def __init__(self,link_location,link_name):
        BaseHTMLTag.__init__(self)
        self.tag_name = "a"
        #self.addAttribute('href',link_location)
        self.addAttributes(href=link_location)
        self.setContent(link_name)

class ListItemTag(BaseHTMLTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "li"

class OrderedListTag(BaseHTMLTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "ol"

class UnorderedListTag(BaseHTMLTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "ul"

class HeadingTag(BaseHTMLTag):
    def __init__(self,rank=1):
        BaseHTMLTag.__init__(self)
        r = min(rank,6)
        r = max(rank,1)
        self.tag_name = "h%d" % (r)

class DivisionTag(BaseHTMLTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "div"

class TableTag(BaseHTMLTag):
    def __init__(self,attributes={},header_cols=[]):
        BaseHTMLTag.__init__(self)
        self.tag_name = "table"
        self.table_head_index = -1
        self.table_body_index = -1

        if attributes: self.addAttributes(**attributes)

        if header_cols:
            header_row = []
            for tag_info in header_cols:
                new_col = HeaderCellTag()
                # NOTE: We need to set this tag's pretty_print flag by hand b/c otherwise this tag's
                #       children won't inherit the proper pretty_print setting when they are added to
                #       the parent tag
                new_col.setPrettyPrint(self.pretty_print)
                if tag_info.has_key('content'):
                    new_col.setContent(tag_info['content'])
                if tag_info.has_key('attributes'):
                    new_col.addAttributes(**tag_info['attributes'])
                if tag_info.has_key('tags'):
                    for tag in tag_info['tags']:
                        new_col.addTag(tag)
                header_row.append(new_col)
            self.addTableHeader(header_row)

    # Adds a <thead> tag for this <table> tag
    def addTableHeader(self,th_list):
        self.clearTags()
        self.table_head_index = len(self.nested_tags)
        self.num_cols = len(th_list)
        new_head_tag = TableHeadTag(th_list)
        self.addTag(new_head_tag)

    # Adds a <tbody> tag for this <table> tag
    def addTableBody(self):
        self.table_body_index = len(self.nested_tags)
        self.addTag(TableBodyTag())

    # Returns the <thead> tag for this <table> tag
    def getTableHeader(self):
        if self.table_head_index < 0:
            return None
        return self.nested_tags[self.table_head_index]

    # Returns the <tbody> tag for this <table> tag
    def getTableBody(self):
        if self.table_body_index < 0:
            return None
        return self.nested_tags[self.table_body_index]

    # Returns the n-th <th> tag for this <table> tag
    def getHeaderColumn(self,n):
        if n >= self.nCols or n < 0:
            print "ERROR: Requested column out of range!"
            return
        elif self.table_head_index < 0:
            return
        else:
            table_head = self.getTableHeader()
            return table_head.getColumn(n)

    # Returns the specified row from the <tbody> (if present), otherwise returns the specified row from the <table>
    def getTableRow(self,row_index):
        table_row = None
        table_body = self.getTableBody()
        if  table_body is None:
            if row_index >= len(self.nested_tags):
                # Index out of range!
                return None
            if row_index < 0:
                # We are starting from the tail!
                row_index = row_index % self.nRows()
            table_row = self.nested_tags[row_index]
        else:
            if row_index >= table_body.nRows():
                # Index out of range!
                return None
            if row_index < 0:
                # We are starting from the tail!
                row_index = row_index % self.nRows()
            table_row = table_body.nested_tags[row_index]
        return table_row

    # Adds a <tr> tag to the <table> and formats each <td> element according to the tag_info dict
    def appendTableRow(self,row_attributes={},cell_list=[]):
        #tag_info = {
        #    'content': '',         Specify string content for the specific <TD>
        #    'tags': [],            Specify nested tags for the specific <TD>
        #    'attributes': {},      Specify <TD> specific attributes
        #}
        if len(cell_list) == 0:
            # Don't try to add a row with no cells
            return

        row = TableRowTag()
        row.setPrettyPrint(self.pretty_print)   # See comment in init()
        row.addAttributes(**row_attributes)

        for tag_info in cell_list:
            new_cell = DataCellTag()
            row.addTag(new_cell)
            if tag_info.has_key('content'):
                new_cell.setContent(tag_info['content'])
            if tag_info.has_key('attributes'):
                new_cell.addAttributes(**tag_info['attributes'])
            if tag_info.has_key('tags'):
                for tag in tag_info['tags']:
                    new_cell.addTag(tag)
        self.addTableRow(row)

    # Adds a <tr> tag to the <tbody> (if present) for this <table> tag, otherwise add the row directly to the table
    def addTableRow(self,table_row):
        if not self.nCols() is None and self.nCols() != table_row.nCols():
            print "ERROR: Column Mismatch!"
            return

        table_body = self.getTableBody()
        if table_body is None:
            # Add the row directly to the <table>
            self.addTag(table_row)
        else:
            # Add the row to the <tbody>
            table_body.addTag(table_row)
        return

    # Adds a <tr> tag to the <tbody> for this <table> tag
    def addRow(self,td_list):
        if self.nCols() != len(td_list):
            print "ERROR: Column Mismatch!"
            return
        new_row = TableRowTag()
        new_row.setPrettyPrint(self.pretty_print)   # See comment in init()
        for td in td_list:
            new_row.addTag(td)
        self.addTableRow(new_row)

    # Returns the number of columns for this <table> tag
    def nCols(self):
        table_head = self.getTableHeader()
        if (table_head is None):
            # The table doesn't have a <thead>!
            return None
        return table_head.nCols()

    # Returns the number of rows in the <tbody> (if present) or the number of nested tags for this <table> tag
    def nRows(self):
        table_body = self.getTableBody()
        if table_body is None:
            counter = 0
            return (len(self.nested_tags) - counter)
        else:
            return table_body.nRows()

class TableHeadTag(BaseHTMLTag):
    def __init__(self,th_list=[]):
        BaseHTMLTag.__init__(self)
        self.tag_name = "thead"

        trt = TableRowTag()
        self.addTag(trt)                    # Add the tag first, so that it inherits the pretty_print setting
        for t in th_list: trt.addTag(t)     # Since the tag objects are stored by ref, this should be fine

    # Returns the <tr> of the header tag
    def getHeaderRow(self):
        return self.nested_tags[0]

    # Returns the n-th <th> tag for this <thead> tag
    def getColumn(self,n):
        if n >= self.nCols or n < 0:
            print "ERROR: Requested column out of range!"
            return
        head_row = self.getHeaderRow()
        return head_row.nested_tags[n]

    # Returns the number of columns for this <thead> tag
    def nCols(self):
        head_row = self.getHeaderRow()
        return head_row.nCols()

class TableBodyTag(BaseHTMLTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "tbody"

    # Returns the number of rows for this <tbody> tag
    def nRows(self):
        return len(self.nested_tags)

class TableRowTag(BaseHTMLTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "tr"
        self.num_cols = 0

    # Returns the number of columns for this <tr> tag
    def nCols(self):
        return len(self.nested_tags)

class HeaderCellTag(BaseHTMLTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "th"

class DataCellTag(BaseHTMLTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "td"

class TitleTag(BaseHTMLTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "title"

class HTMLTag(BaseHTMLTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "html"

class ScriptTag(BaseHTMLTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "script"

class HeadTag(BaseHTMLTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "head"

class BodyTag(BaseHTMLTag):
    def __init__(self):
        BaseHTMLTag.__init__(self)
        self.tag_name = "body"
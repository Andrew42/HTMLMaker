import os
import sys

from HTMLMaker.BaseTags import *
from HTMLMaker.VoidTags import *
from HTMLMaker.HTMLGenerator import HTMLGenerator

# Create an index.html file for a web-directory with .png files

STYLE_STR = """
div.image {
    float: left;
    margin: 5px;
    text-align: center;
    font-size: 10pt;
    font-family: Verdana, Arial, sans-serif;
    background-color: white;
    border: 1px solid #ccc;
    /* padding: 2px; */
    /* margin: 2px 10px 10px 2px; */
    -moz-box-shadow: 7px 5px 5px rgb(80,80,80);    /* Firefox 3.5 */
    -webkit-box-shadow: 7px 5px 5px rgb(80,80,80); /* Chrome, Safari */
    box-shadow: 7px 5px 5px rgb(80,80,80);         /* New browsers */
}

div.image img {
    width: 355px;
    height: 229px;
}

div.image div {width: 355px;}
"""

# Return list of files with a specified file_type in a directory
def getImages(tar_dir,file_type='png'):
    fnames = []
    for out in sorted(os.listdir(tar_dir)):
        fpath = os.path.join(tar_dir,out)
        if (os.path.isdir(fpath)):
            continue
        f,ftype = out.rsplit(".",1)
        if ftype != file_type:
            continue
        fnames.append(out)
    return fnames

# Creates an index.html file at the specified location for displaying .png files in a web-browser
def make_html(tar_dir):
    home_dir = os.getcwd()
    if not os.path.exists(tar_dir):
        print "Target directory does not exists: %s" % (tar_dir)
        return

    os.chdir(tar_dir)

    my_html = HTMLGenerator()

    meta_tag = MetaTag(); my_html.addHeadTag(meta_tag)
    meta_tag.addAttributes(charset='UTF-8')

    style_tag = StyleTag(); my_html.addHeadTag(style_tag)
    style_tag.setContent(STYLE_STR)
    style_tag.addAttributes(type='text/css')

    image_files = getImages(tar_dir)
    for fname in image_files:
        image_name,ftype = fname.rsplit(".",1)

        div_tag   = DivisionTag(); my_html.addBodyTag(div_tag)
        image_tag = ImgTag()
        text_div  = DivisionTag()
        link_tag  = HyperLinkTag(link_location="./%s" % (fname),link_name='')

        # This ensures the pretty_print setting gets inherited properly
        div_tag.addTag(link_tag)
        div_tag.addTag(text_div)
        link_tag.addTag(image_tag)

        image_tag.addAttributes(src="./{}".format(fname))

        link_tag.addAttributes(target='_blank')

        text_div.addAttributes(id='imgName')
        text_div.setContent(image_name)

        div_tag.addAttributes(cls='image')


    print my_html.dumpHTML()
    # my_html.saveHTML(f_name='index.html',f_dir=tar_dir)

    os.chdir(home_dir)

def main():
    if len(sys.argv) == 2:
        fpath = sys.argv[1]
    else:
        print "ERROR: Must specify path"
    if not os.path.exists(fpath):
        print "ERROR: Unknown path {}".format(fpath)
        return
    make_html(fpath)

if __name__ == "__main__":
    main()

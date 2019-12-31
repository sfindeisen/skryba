import lxml.etree as ET

def parse_xml_dom(xml_filename):
    """Given an XML file name, returns the DOM tree."""
    return ET.parse(xml_filename)

def get_xslt_transformer(xslt_filename):
    """Given an XSLT file name, returns the XSLT transformer."""
    xslt = parse_xml_dom(xslt_filename)
    return ET.XSLT(xslt)

def get_xpath0(xml_node, path):
    """Given an XML node and XPath expression (a string), returns
       the node pointed to by this XPath (or None, if there is no
       such node). It is an error if there are multiple nodes.

    xml_node -- XML DOM node (as returned from lxml.etree)
    path     -- XPath expression (as a string)
    """
    t = xml_node.xpath(path)
    u = len(t)

    if (0 == u):
        return None
    elif (2 <= u):
        raise Exception("Multiple nodes ({}) selected by XPath: {}".format(u, path))
    else:
        return t[0]     # return the only node in the list

def get_xpath1(xml_node, path):
    """Given an XML node and XPath expression (a string), returns
       the node pointed to by this XPath. It is an error if there
       is no such node, or if there are multiple such nodes.

    xml_node -- XML DOM node (as returned from lxml.etree)
    path     -- XPath expression (as a string)
    """
    t = xml_node.xpath(path)
    u = len(t)

    if (0 == u):
        raise Exception("No node selected by XPath: {}".format(path))
    elif (2 <= u):
        raise Exception("Multiple nodes ({}) selected by XPath: {}".format(u, path))
    else:
        return t[0]     # return the only node in the list

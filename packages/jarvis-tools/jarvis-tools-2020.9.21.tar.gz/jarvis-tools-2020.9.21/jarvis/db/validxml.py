from lxml import etree


def is_xml_valid(xsd="jarvisdft.xsd", xml="JVASP-1002.xml"):
    """Check if XML is valid."""
    xml_file = etree.parse(xml)
    xml_validator = etree.XMLSchema(file=xsd)
    is_valid = xml_validator.validate(xml_file)
    return is_valid


is_valid = is_xml_valid()
print(is_valid)

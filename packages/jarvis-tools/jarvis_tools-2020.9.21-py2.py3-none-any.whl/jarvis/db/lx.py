from lxml import etree
filename='JVASP-1002.xml'
try:
   xmlschema_doc = etree.parse(filename)
   xmlschema = etree.XMLSchema(xmlschema_doc)
   xmlschema.assertValid(elem_tree)
except etree.ParseError as e:
   raise etree.ParserError(str(e))
except etree.DocumentInvalid as e:
   if ignore_errors:
    raise etree.ValidationError("The Config tree is invalid with error message:\n\n" + str(e)) 

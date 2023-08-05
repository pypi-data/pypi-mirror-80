from lxml import etree

xsl = etree.parse("jarvisff.xsl")
updated = etree.XSLT(xsl)
xml = etree.parse("JLMP-1245.xml")
html = updated(xml)

html.write("XML-Transformed.html")

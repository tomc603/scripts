#!/usr/bin/env python

from xml.dom import minidom


def InspectNode(XmlNode):
	'''Inspect the attributes of XmlNode and report any that are > 19 chars long.
	Then Cycle through the child nodes of the specified node'''
	if XmlNode.attributes:
		if 'alias' in XmlNode.attributes.keys():
			aliasstr = XmlNode.attributes['alias'].value.replace('TOOLONG', '')
			if len(aliasstr) > 19:
				print aliasstr, len(aliasstr), '/', len(aliasstr) - 19

	if XmlNode.hasChildNodes():
		for cNode in XmlNode.childNodes:
			InspectNode(cNode)


mdom = minidom.parse('a10-ax.xml')

if mdom.hasChildNodes():
	# The top level node has children. This is good. Inspect it/them
	InspectNode(mdom)
else:
	# The top level node does NOT have children. We have an empty XML doc.
	print 'XML document has no child nodes!'


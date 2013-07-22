#-*- coding:utf-8 -*-

from xml.etree import ElementTree
import sys

#import data_trans
from data_trans import PythonDict2Lua as pydict2lua

def print_node(node, identcnt = 0):
	#打印结点基本信息
	ident_space = ' ' * identcnt
	def print_info(string):
		print ident_space + string	

	print_info("node.attrib:" + str(node.attrib))
	print_info("node.tag:%s" % node.tag)
	print_info("node.text:%s" % node.text)
	print_info("node.childrens:")
	for child in node:
		print_node(child, identcnt + 10)

	#data = pydict2lua(node)
	#print data

def trans_attrib(attrib):
	newAttr = {}
	for k in attrib.keys():
		try :
			v = int(attrib[k])
		except:
			v = attrib[k]
		newAttr[k] = v
	return newAttr

def parse_node(node):
	data = {}
	data["attrib"] = trans_attrib(node.attrib)
	data["tag"] = node.tag
	if node.text:
		data["text"] = node.text.strip()
		if len(data["text"]) <= 0:
			del data["text"]


	if len(node) > 0:
		index = 1
		data["childrens"] = {}
		for child in node:
			child_data = parse_node(child)
			data["childrens"][index] = child_data
			index = index + 1
	return data
	

def parse_xml(file):
	#print open(file).read()
	elem_tree = ElementTree.parse(file)

	root = elem_tree.getroot()

	#m = root.iter()

	#print_node(root)

	#root = Ele.getiterator("Behavior")

	data = parse_node(root)
	data_str = pydict2lua(data, True)

	return "return " + data_str

if __name__ == '__main__':
	#parse_xml("transporter.xml")
	if len(sys.argv) < 3:
		print 'usage: python xmltolua.py filename output'
		sys.exit(1)
	#parse_file = os.path.abspath((sys.argv[1]).strip())
	parse_file = sys.argv[1].strip()
	output = sys.argv[2].strip()
	data = parse_xml(parse_file)

	Util = __import__("util")
	Util.write_file(output, data)
	

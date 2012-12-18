import urllib2
import sys
import re
from sets import Set
import pickle

class Course:
	"""Simple class for a course"""
	
	code = ""
	title = ""
	description = ""
	prerequisite = ""
	distribution = ""
	exclusions = ""
	breadth = ""

class BooleanNode:
	'''Boolean node whose value is either True or False'''
	
class AndNode(BooleanNode):
	'''Boolean node that\'s evaluated based on the AND of its operands'''
	
	def __init__(self, operands):
		self.__operands = Set();
		for operand in operands: self.__operands.add(operand)
		
	def add(self, node):
		self.__operands.add(node)
		
	def nodes(self):
		return self.__operands
		
	def type(self):
		return "AND"
	
	def eval(self, taken):
		'''Return true if all the operands are TRUE'''
		for operand in self.__operands:
			if operand.eval(taken) == False: return False
		return True
	
	def __len__(self):
		return len(self.__operands)
	
	def __repr__(self):
		return str(self.__operands).replace("Set", "And")
		
class OrNode(BooleanNode):
	'''Boolean node that\'s evaluated based on the OR of its operands'''

	def __init__(self, operands):
		self.__operands = Set();
		for operand in operands: self.__operands.add(operand)
		
	def add(self, node):
		self.__operands.add(node)
		
	def nodes(self):
		return self.__operands
		
	def type(self):
		return "OR"

	def eval(self, taken):
		'''Return true if any of the operands are TRUE'''
		for operand in self.__operands:
			if operand.eval(taken) == True: return True
		return False
	
	def __len__(self):
		return len(self.__operands)
		
	def __repr__(self):
		return str(self.__operands).replace("Set", "Or")
	
		
class CourseNode(BooleanNode):
	'''Boolean node that\'s evaluated based on the whether or not the course is taken'''
	
	def __init__(self, course_code):
		self.__course_code = course_code
		
	def type(self):
		return "COURSE"
		
	def eval(self, taken):
		'''Return True if the course has been taken'''
		return self.__course_code in taken
		
	def __repr__(self):
		return self.__course_code

def unbracket(text):
	if text.startswith("(") and text.endswith(")"):
		if bracket_parity(text[1:-1]): return text[1:-1]
	return text
	
def bracket_parity(text):
	parity = 0
	for c in text:
		if c == "(": parity += 1
		elif c == ")": parity -= 1
		if parity < 0: return False
	return parity == 0

def to_node(text, delimiter=";"):
	text = unbracket(text)
	if re.search(';|/|\)|\(', text) == None:
		return CourseNode(text)
	texts = []
	nodes = []
	new_text = ""
	for c in text:
		if c == delimiter and bracket_parity(new_text):
			texts.append(new_text)
			new_text = ""
		else:
			new_text += c
	texts.append(new_text)
	if delimiter == ";":
		for t in texts:
			nodes.append(to_node(t, "/"))
		if len(nodes) > 1:
			node = AndNode(nodes)
		else:
			node = nodes[0]
	elif delimiter == "/":
		for t in texts:
			nodes.append(to_node(t, ";"))
		if len(nodes) > 1:
			node = OrNode(nodes)
		else:
			node = nodes[0]
	return node

def open_courses(filename):
	filehandler = open(filename, 'r') 
	courses = pickle.load(filehandler)
	return courses
	
def convert_prerequisite(courses):
	for course_code in courses:
		course = courses[course_code]
		course.prerequisite = to_node(course.prerequisite)
		
def get_available(courses, taken):
	available = Set()
	for course_code in courses:
		course = courses[course_code]
		if str(course.prerequisite) == "None" and course_code not in taken:
			available.add(course_code)
			pass
		elif course.prerequisite.eval(taken):
			available.add(course_code)
	return available
	
def get_required(courses, course_code, taken):
	course = courses[course_code]
	paths = []
	path = []
	node = course.prerequisite
	while not node.eval():
		if node.type() == "AND":
			path.append()

def get_paths(root, taken):
	if root.type() == "COURSE":
		return str(root)
	elif root.type() == "AND":
		
	elif root.type() == "OR":
		for node in root.nodes():
			paths.add(get_paths(node, taken))
		
	
courses = open_courses("sample.obj")
convert_prerequisite(courses)

for course_code in courses:
	course = courses[course_code]
	print course.prerequisite
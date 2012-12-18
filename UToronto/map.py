import urllib2
import sys
import re
from sets import Set
import pickle

# Class for a course
class Course:
	"""Simple class for a course"""
	
	code = ""
	title = ""
	description = ""
	prerequisite = ""
	distribution = ""
	exclusions = ""
	breadth = ""
	
class And:
	
  	def __init__(self):
		self.ray = []
	
	def add(self, value):
		self.ray.append(value)
		
	def eval(self, taken):
		retval = True
		for val in self.ray:
			if isinstance(val, unicode):
				retval = retval and val in taken
			else:
				retval = retval and val.eval(taken)
		return retval
		
	def __str__(self):
		return "AND" + str(self.ray)
		
	def __repr__(self):
		return "AND" + str(self.ray)

class Or:

	def __init__(self):
		self.ray = []

	def add(self, value):
		self.ray.append(value)
		
	def eval(self, taken):
		retval = False
		for val in self.ray:
			if isinstance(val, unicode):
				retval = retval or val in taken
			else:
				retval = retval or val.eval(taken)
		return retval
		
	def __str__(self):
		return "OR" + str(self.ray)
		
	def __repr__(self):
		return "OR" + str(self.ray)
	
def open_courses(filename):
	filehandler = open(filename, 'r') 
	courses = pickle.load(filehandler)
	return courses

def split_and(text):
	pre = text
	result = re.search("\(.*?\)", pre)
	while result is not None:
		result = result.group()
		new_result = result.replace(";", "<").replace("(","[").replace(")","]")
		pre = pre.replace(result, new_result)
		result = re.search("\(.*?\)", pre)
	pres = pre.split(";")
	for i in range(len(pres)):
		pres[i] = pres[i].replace("<", ";").replace("[","(").replace("]",")")
	
	a = And()
	for pre in pres:
		if pre.startswith("(") and pre.endswith(")"):
			pre = pre[1:-1]
			pass
		a.add(pre)
	return a

def split_or(text):
	pre = text
	result = re.search("\(.*?\)", pre)
	while result is not None:
		result = result.group()
		new_result = result.replace("/", "<").replace("(","[").replace(")","]")
		pre = pre.replace(result, new_result)
		result = re.search("\(.*?\)", pre)
	pres = pre.split("/")
	for i in range(len(pres)):
		pres[i] = pres[i].replace("<", "/").replace("[","(").replace("]",")")
	
	o = Or()
	for pre in pres:
		if pre.startswith("(") and pre.endswith(")"):
			pre = pre[1:-1]
			pass
		o.add(pre)
	return o

def convert(courses):
	for course_code in courses:
		course = courses[course_code]
		if course.prerequisite == "None":
			continue
		course.prerequisite = split_and(course.prerequisite)
		for i in range(len(course.prerequisite.ray)):
			if len(course.prerequisite.ray[i]) == 8:
				continue
			course.prerequisite.ray[i] = split_or(course.prerequisite.ray[i])
			for j in range(len(course.prerequisite.ray[i].ray)):
				if len(course.prerequisite.ray[i].ray[j]) == 8:
					continue
				course.prerequisite.ray[i].ray[j] = split_and(course.prerequisite.ray[i].ray[j])
				for k in range(len(course.prerequisite.ray[i].ray[j].ray)):
					if len(course.prerequisite.ray[i].ray[j].ray[k]) == 8:
						continue
					course.prerequisite.ray[i].ray[j].ray[k] = split_or(course.prerequisite.ray[i].ray[j].ray[k])
					for l in range(len(course.prerequisite.ray[i].ray[j].ray[k].ray)):
						if len(course.prerequisite.ray[i].ray[j].ray[k].ray[l]) == 8:
							continue
						course.prerequisite.ray[i].ray[j].ray[k].ray[l] = split_and(course.prerequisite.ray[i].ray[j].ray[k].ray[l])
						
def available(courses, taken):
	available = {}
	for course_code in courses:
		course = courses[course_code]
		if course.prerequisite == "None" and course_code not in taken:
			#available[course_code] = course
			pass
		elif course.prerequisite != "None" and course.prerequisite.eval(taken):
			available[course_code] = course
	return available
	
courses = open_courses("sample.obj")
convert(courses)

#taken = {}
#taken["ANT253H1"] = courses["ANT253H1"]
#available = available(courses, taken)				
		
for course_code in courses:
	print course_code, courses[course_code].prerequisite
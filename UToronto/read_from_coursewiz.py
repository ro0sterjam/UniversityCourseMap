import urllib2
import sys
from bs4 import BeautifulSoup
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

# Set of courses
courses = {}

filename = "courses.obj"
	
def get_data(soup, header_text):
	header = soup.find("th", text=header_text)
	if header is None:
		return None
	data = header.parent.find("td")
	return data.text.strip()
	
def print_course(course):	
	print course.code
	print course.title
	print course.description
	print course.prerequisite
	print course.distribution
	print course.breadth
	print "-----------------------------------------------"
	
def print_courses():
	print len(courses)
	for course in courses.values():
		print_course(course)
	
def save_courses(courses, filename):
	filehandler = open(filename, 'w')
	pickle.dump(courses, filehandler)
	
def open_courses(filename):
	filehandler = open(filename, 'r') 
	courses = pickle.load(filehandler)
	return courses
	
def parse_courses():	
	for i in range(1, 5000):
		print "parsing ", i
		base_url = "http://coursewiz.leila.cc/courses/" + str(i) + "/"
		try:
			page = urllib2.urlopen(base_url)
			soup = BeautifulSoup(page)
			page.close()
		except urllib2.HTTPError:
			pass
		else:
			temp = soup.find("h1", text=re.compile("|")).text.split("|")
			course = Course()
			course.code = temp[0].strip() + "1"
			course.title = temp[1].strip()
			course.description = get_data(soup, "Description")
			course.prerequisite = get_data(soup, "Prerequisites")
			course.exclusions = get_data(soup, "Exclusions")
			course.distribution = get_data(soup, "Distribution")
			course.breadth = get_data(soup, "Breadth")
			courses[course.code] = course

def remove_spaces(text):
	text = text.replace(" ", "")
	text = text.replace(u"\u00A0", "")
	text = text.replace(".", "")
	return text.replace("\n", "")

def append_one_to_code(text):
	return re.sub("(Y|H)(;|,|/|\)| |$)", r'\1 1\2', text).replace(" ", "")

def prefix(text):
	new_text = text.replace(")", "")
	new_text = text.replace("(", "")
	codes = re.split(";|,|/|$", new_text)
	for i in range(len(codes)):
		if len(codes[i]) == 5 or len(codes[i]) == 2:
			j = 1
			pre = codes[i-j][0:8-len(codes[i])]
			while(len(pre) != 8-len(codes[i])):
				j = j + 1
				pre = codes[i-j][0:8-len(codes[i])]
			if len(codes[i]) == 5:
				new_code = re.sub("([0-9]{3}[YH][15])", pre + r'\1', codes[i])
			else:
				new_code = re.sub("([YH]1)", pre + r'\1', codes[i])
			text = text.replace(codes[i], new_code)
			codes[i] = new_code
	return text
	
def replace_to_semi_colon(text):
	text = text.replace("+", ";")
	text = text.replace("&", ";")
	text = text.replace(" AND ", ";")
	return text.replace(",", ";")
	
def fix_direct_bracket(text):
	return re.sub("1\(([A-Z])", "1/(" + r"\1", text)

#parse_courses()
#save_courses(courses, filename)
courses = open_courses(filename)
#print_courses()

easy = {}
hard = {}
plus = {}
new_easy = {}

for course_code in courses:
	course = courses[course_code]
	if course.prerequisite == "None" or re.compile("[a-z%]").search(course.prerequisite) is None:
		# Replace all spaces
		course.prerequisite = replace_to_semi_colon(course.prerequisite)
		course.prerequisite = remove_spaces(course.prerequisite)
		# Add 1 to end of all codes
		course.prerequisite = fix_direct_bracket(course.prerequisite)
		course.prerequisite = append_one_to_code(course.prerequisite)
		course.prerequisite = prefix(course.prerequisite)
		easy[course_code] = course
		if "+" in course.prerequisite:
			plus[course_code] = course
	else:
		hard[course_code] = course
		
print len(easy)
print len(hard)

for course_code in easy:
	a = easy[course_code]
	new_easy[course_code] = a
	pre = a.prerequisite
	pre = pre.replace("(", "")
	pre = pre.replace(")", "")
	codes = re.split(";|/", pre)
	for code in codes:
		if len(code) != 8 and code != "None":
			del new_easy[course_code]
			break

save_courses(new_easy, "sample.obj")			

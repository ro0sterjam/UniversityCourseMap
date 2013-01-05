import urllib2
import sys
from bs4 import BeautifulSoup
import re
from sets import Set

# Class for a course
class Course:
	"""Simple class for a course"""
	
	description = ""
	prerequisite = ""
	corequisite = ""
	exclusion = ""
	distribution_requirement_status = ""
	breadth_requirement = ""
	
	def __init__(self, span_text):
		self.code = span_text.split(u"\u00A0" + u"\u00A0" + u"\u00A0" + u"\u00A0")[0].strip()
		self.title = span_text.split(u"\u00A0" + u"\u00A0" + u"\u00A0" + u"\u00A0")[1].strip()

# Regular expression for text starting with a course code
course_code_regex = re.compile("^[A-Z]{3}[0-9]{3}[A-Z][0-9].*?$")

# Sets span texts of courses and not courses
courses = Set()
not_courses = Set()

# Read main calendar page
base_url = "http://www.artsandscience.utoronto.ca/ofr/calendar/"
page = urllib2.urlopen(base_url)
soup = BeautifulSoup(page)
page.close()

# Get all the links to course pages
main_links = soup.find('div', attrs={"class" : "items"}).findAll('a')
program_urls = []
for link in main_links:
	program_urls.append(base_url + link.get('href'))

program_urls = ["http://www.artsandscience.utoronto.ca/ofr/calendar/crs_csc.htm"]

# Go through each course page
for program_url in program_urls:
	
	# Read course page
	page = urllib2.urlopen(program_url)
	soup = BeautifulSoup(page)
	page.close()

	# Get to first course code
	tags1 = soup.findAll('span', attrs={"class" : "strong"})
	tags2 = soup.find('span', attrs={"class" : "strong"})
	while tags1[1] != tags2:
		tags2 = tags2.next
	print tags1[1] == tags2
	print tags1[1]
	print tags2
	'''
	stop = False
	if tag is None: stop = True
	while stop == False and course_code_regex.match(tag.text) is None:
		tag = tag.findNext('span', attrs={"class" : "strong"})
		if tag is None: stop = True
		
	# While there's still courses on page
	while stop == False:
		
		# Get course code text
		text = tag.text
		print text
		
		# Sometimes course code ends with </span> and title is in its own <strong>
		if text.endswith(u"\u00A0" + u"\u00A0" + u"\u00A0" + u"\u00A0"):
			tag = tag.findNextSibling("strong")
			text = text + tag.text

		# Create the course
		course = Course(text.strip())
		
		# Keep adding text until next course code found
		tag = tag.next
		if tag is None: stop = True
		while stop == False and course_code_regex.match(tag.text) is None:
			course.description = course.description + tag.text
			tag = tag.next
			if tag is None: stop = True
		
		print course.code
		print course.title
		print course.description, "\n"

# Output all non-courses
for course in courses:
	print "-------------------------------------------------------------------"
	print course.code
	print course.title
	print course.description, "\n"
	print "-------------------------------------------------------------------"'''
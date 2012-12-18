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

	# Find all the strong spans on the page (holds course codes)
	strong_spans = soup.findAll('span', attrs={"class" : "strong"})

	# Add all courses / non-courses spans to sets
	for i in range(0, len(strong_spans)):
		strong_span = strong_spans[i]
		span_text = strong_span.text
		if course_code_regex.match(span_text):
			
			# Sometimes course code ends with </span> and title is in its own <strong>
			if span_text.endswith(u"\u00A0" + u"\u00A0" + u"\u00A0" + u"\u00A0"):
				strong_span = strong_span.findNextSibling("strong")
				span_text = span_text + strong_span.text.strip()

			# Create the course
			course = Course(span_text.strip())
			
			# Add description
			strong_span = strong_span.nextSibling
			if strong_span != strong_spans[i + 1]:
				course.description = strong_span.string
			strong_span = strong_span.nextSibling
			while strong_span != strong_spans[i + 1]:
				course.description = course.description + strong_span.string
			courses.add(course)
		else :
			not_courses.add(span_text)

# Output all non-courses
for course in courses:
	print "-------------------------------------------------------------------"
	print course.code
	print course.title
	print course.description, "\n"
	print "-------------------------------------------------------------------"
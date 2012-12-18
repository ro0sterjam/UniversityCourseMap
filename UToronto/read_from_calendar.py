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

# Set of courses
courses = Set()

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

#program_urls = ["http://www.artsandscience.utoronto.ca/ofr/calendar/crs_csc.htm"]

# Go through each course page
for program_url in program_urls:
	
	raw_input(program_url)
	
	# Read course page
	page = urllib2.urlopen(program_url)
	soup = BeautifulSoup(page)
	page.close()

	# Find all the strong spans on the page (holds course codes)
	strong_spans = soup.findAll('span', attrs={"class" : "strong"})

	# Add all courses / non-courses spans to sets
	for strong_span in strong_spans:
		span_text = strong_span.text
		if course_code_regex.match(span_text):
			
			# Sometimes course code ends with </span> and title is in its own <strong>
			if span_text.endswith(u"\u00A0" + u"\u00A0" + u"\u00A0" + u"\u00A0"):
				span_text = span_text + strong_span.findNextSibling("strong").text.strip()

			# Create the course
			course = Course(span_text.strip())
			
			# Add description
			course.description = strong_span.findNextSibling("p")
			# Sometimes the course title is under it's own 'p'; need to go up a level
			if course.description is None:
				course.description = strong_span.parent.findNextSibling("p")
			else:
				course.description = course.description.text.strip()
				
			# Sometimes the <strong> contents contains some shit in the beginning
			if course.description is not None and "[endif]" in course.description:
				course.description = course.description.split("[endif]")[-1]
			
			courses.add(course)
			print "-------------------------------------------------------------------"
			print course.code
			print course.title
			print course.description, "\n"
			print "-------------------------------------------------------------------"
		else :
			not_courses.add(span_text)

# Output all non-courses
for course in courses:
	print "-------------------------------------------------------------------"
	print course.code
	print course.title
	print course.description, "\n"
	print "-------------------------------------------------------------------"
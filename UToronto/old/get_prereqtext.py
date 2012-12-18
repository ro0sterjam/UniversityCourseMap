import urllib2
from bs4 import BeautifulSoup
import re
from sets import Set

course_codes = Set()

#STILL NEED TO FIX CAS393H1

base_url = "http://www.artsandscience.utoronto.ca/ofr/calendar/"
page = urllib2.urlopen(base_url)
soup = BeautifulSoup(page)
page.close()

main_links = soup.find('div', attrs={"class" : "items"}).findAll('a')
program_urls = []
for link in main_links:
	program_urls.append(base_url + link.get('href'))
	
for program_url in program_urls:
	page = urllib2.urlopen(program_url)
	soup = BeautifulSoup(page)
	page.close()
	program_name = soup.find('h1').text
	program_course_header = soup.find('h2', text=program_name + " Courses")
	if program_course_header:
		course_headers = program_course_header.findAllNext('a', attrs={'name' : re.compile('^[A-Z][A-Z][A-Z]\d\d\d[A-Z]\d$')})
		for course_header in course_headers:
			course_prerequisites_header = course_header.findNextSibling(text=re.compile('^Prerequisite'))
			course_code = course_header.get('name')
			if course_code in course_codes:
				continue
			else:
				course_codes.add(course_code)
			course_name_header = course_header.findNextSibling(text=re.compile(course_code))
			if course_name_header is None:
				course_name_header = course_header.findNext(text=re.compile(course_code))
			if hasattr(course_name_header, 'text'):
				course_name = course_name_header.text.strip()
				course_name = course_name[len(course_code):].strip()
			else:
				course_name = course_name_header.string.strip()
				course_name = course_name[len(course_code):].strip()
			
			print '>>'+course_code+'>>' + course_name 
			'''course_name = ''
			next = course_header.nextSibling
			if course_code == 'UNI411H1':
				print next
			while course_name.find(course_code) != 0 and next is not None:
				if hasattr(next, 'text'):
					course_name = next.text.strip()
				else:
					course_name = next.string.strip()
				next = next.nextSibling'''
			#print '>>' + course_name
			'''if course_header.findNextSibling(text=re.compile(course_code)) is None:
				print course_header.next.text
			else:
				course_name_header = course_header.findNextSibling(text=re.compile(course_code))
				if not hasattr(course_name_header, 'text'):
					course_name = course_name_header.string.strip()
				else:
					course_name = course_name_header.text.strip()'''
			if course_prerequisites_header:
				prerequisites_text = course_prerequisites_header.string
				next = course_prerequisites_header
				keep_going = True
				while keep_going and next is not None:
					next = next.nextSibling
					if next is None:
						continue
					elif hasattr(next, 'name') and next.name == 'br':
						prerequisites_text = prerequisites_text + '\n'
					if not hasattr(next, 'text'):
						text = next.string
					else:
						if next.get('name') is not None:
							keep_going = False
						else:
							text = next.text
					text = text.strip()
					if (not keep_going) or text.startswith('Exclusion') or text.startswith('Corequisite') or text.startswith('Distribution Requirement Status') or text.startswith('Breadth') or text.startswith('Recommended Preparation') or text.startswith('Enrolment Limits'):
						keep_going = False
					else:
						prerequisites_text = prerequisites_text + ' ' + text
				prerequisites_text = prerequisites_text[13:].strip()
			else:
				prerequisites_text = "NONE MOTHERFUCKA"
			#print
			#print '-----------------------------------------'
			#print course_name
			#print '-----------------------------------------'
			#print prerequisites_text
	else :
		pass
import urllib2
from bs4 import BeautifulSoup
import re

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
		course_headers = soup.findAll('a', attrs={'name' : re.compile('^[A-Z][A-Z][A-Z]\d\d\d[A-Z]\d$')})
		for course_header in course_headers:
			course_prerequisites_header = course_header.findNextSibling(text=re.compile('^Prerequisite'))
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
						'''
						bad_texts = ['Exclusion', 'Corequisite', 'Distribution', 'Breadth', 'Recommended Preparation']
						index = len(text) - 1
						for bad_text in bad_texts:
							if bad_text in text:
								keep_going = False
								index = min([index, text.find(bad_text) + 1])
						text = text[0:index]
						'''
						prerequisites_text = prerequisites_text + ' ' + text
				prerequisites_text = prerequisites_text[13:].strip()
				course_code = course_header.get('name')
				course_name = course_header.findNextSibling('span').text[len(course_code):].strip()
				print
				print '-----------------------------------------'
				print course_name
				print '-----------------------------------------'
				print prerequisites_text
				'''course_prerequisites = re.findall('[A-Z][A-Z][A-Z]\d\d\d[A-Z]\d?', course_prerequisites_header)
				course_prerequisite_links = course_prerequisites_header.findNextSiblings('a')
				for course_prerequisite_link in course_prerequisite_links:
					course_prerequisites.append(course_prerequisite_link.text)
				if len(course_prerequisites) >= 0:
					print
					print '-----------------------------------------'
					print course_header.findNextSibling('span').text
					print '-----------------------------------------'
					print course_prerequisites_header'''
				
	else :
		pass

import requests 
from bs4 import BeautifulSoup
import re
import json

# set to None if you want to process all courses, otherwise provide list of Subjects
RESTRICT_TO_SUBJECTS = None  
# RESTRICT_TO_SUBJECTS = ['AAS']

LOG_FILE = 'log.txt'

# Parse data from cisapi, then write it in JSON format:
example = { 
    'courses': [
        { 
            'course_num': '225',
            'department': 'CS',
            'prereqs': ['String with "Prerequisite:" in it'],  # TODO, see parse_requirements()
            'sections': [
                {
                    'section': 'ADE',
                    'crn': '618201',
                    'meetings': [
                        {
                            'building': 'Siebel',
                            'room': '234',
                            'start': '9:00am',
                            'end': '9:50am'
                        }
                    ]
                }
            ]
        }
    ]
}

'''
initialize regex compiled objects, etc
'''
def init():
    global LOG_FILE
    LOG_FILE = open(LOG_FILE, 'w')


'''
log the error and print it to terminal
'''
def log_error(err_string):
    print(err_string + '\n')
    LOG_FILE.write(err_string + '\n')

'''
given the string that follows "Requirements: ", extract it into a "prereqs" array
TODO: group them by requirement groups
    ex. 'CS 125 or ECE 220; One of CS 173, MATH 213'
    becomes a list of class groups:
    { 'prereqs': [['CS 125', 'ECE 220'], ['CS 173', 'MATH 213']] }
TODO: handle concurrent classes?
'''
def parse_requirements(requirements_string):
    if requirements_string is None:
        return None
    return [requirements_string] # TODO impleament with regex


'''
request the XML file from the link, then soupify it
'''
def link_to_soup(link):
    try:
        r = requests.get(link).text
        return BeautifulSoup(r, 'html.parser')
    except Exception as e:
        log_error(f'ERROR: Could not obtain \n{link}')
        return None


'''
parse all class data from the cisapi, and writes to a json:
'''
def parse_semester(year, sem, json_out):  #2020, spring
    init()
    link = f'https://courses.illinois.edu/cisapp/explorer/schedule/{year}/{sem.lower()}.xml'
    soup = link_to_soup(link)
    courses = []
    for subject in soup.find_all('subject'):
        if RESTRICT_TO_SUBJECTS is None or (RESTRICT_TO_SUBJECTS is not None and subject['id'] in RESTRICT_TO_SUBJECTS):
            print('Subject: ', subject['id'])
            parse_subject(subject['href'], courses)
    with open(json_out, 'w') as fd:
        fd.write(json.dumps({'courses': courses}))


'''
appends all courses from a subject (as dictionaries) to the given "courses" list
'''
def parse_subject(link, courses):
    soup = link_to_soup(link)
    try:
        for course in soup.find_all('course'):
            courses.append(parse_course(course['href']))
    except:
        log_error(f'SKIPPING\n{link}')


'''
return a "course" dictionary that also contains a list of "section" dictionaries
'''
def parse_course(link):
    course_dict = { 'course_num': None, 'department': None, 'prereqs': [], 'sections': [] }
    soup = link_to_soup(link)
    try:
        id = soup.find('ns2:course')['id'].split(' ')
        course_dict['department'], course_dict['course_num'] = id
    except:
        log_error(f'ERROR: \n{link}\n has no department or course number!')
    
    match = re.match(r'.*Prerequisite: (.*?)\.', str(soup))
    if match is not None:
        course_dict['prereqs'] = parse_requirements(match.group(1))
    for section in soup.find_all('section'):
        course_dict['sections'].append(parse_section(section['href']))

    # checking edge cases for Prerequisite -> notify us in terminal
    if match is None:
        match = re.match(r'.*Prerequisite.*', str(soup), re.IGNORECASE)  
        if match is not None:
            log_error(f'NOTE: \n{link}\n has "Prerequisite" without a period or different case')
        match = re.match(r'.*concurrent.*', str(soup), re.IGNORECASE)
        if match is not None:
            log_error(f'NOTE: \n{link}\n has "concurrent" without a Prerequisite')
    
    return course_dict


'''
return a "section" dictionary that also contains a list of "meeting" dictionaries
'''
def parse_section(link):
    section_dict = { 'section': None, 'crn': None, 'meetings': [] }
    soup = link_to_soup(link)
    try:
        section_dict['crn'] = soup.find('ns2:section')['id']
    except:
        log_error(f'ERROR: \n{link}\n has no crn!')
        LOG_FILE.write(f'ERROR: \n{link}\n has no crn!')
    if soup.sectionnumber is not None:
        section_dict['section'] = soup.sectionnumber.text
    for meeting in soup.find_all('meeting'):
        meeting_dict = { 'building': None, 'room': None, 'start': None, 'end': None }
        if meeting.buildingname is not None:
            meeting_dict['building'] = meeting.buildingname.text
        if meeting.roomnumber is not None:
            meeting_dict['room'] = meeting.roomnumber.text
        if meeting.start is not None:
            meeting_dict['start'] = meeting.start.text
        if meeting.end is not None:
            meeting_dict['end'] = meeting.end.text
        section_dict['meetings'].append(meeting_dict)
    return section_dict

if __name__ == '__main__':
    parse_semester(2020, 'spring', 'cisdata.json')

    # testing
    # ret = parse_section('https://courses.illinois.edu/cisapp/explorer/schedule/2020/spring/AAS/100/30107.xml')
    # ret = parse_course('https://courses.illinois.edu/cisapp/explorer/schedule/2020/spring/PHYS/213.xml')
    
    
    # parse_subject('https://courses.illinois.edu/cisapp/explorer/schedule/2020/spring/AAS.xml')

''' 
    TODO maybe
cache regex compiled objects for speed
start/end dates in parse_section (for half-sem courses)?

    NOTE
soup lowercases all tags
should we use the actual XML parser or is soup HTML ok?
meetings is a list - CS 233 has 1 section that meets twice in different rooms
'''



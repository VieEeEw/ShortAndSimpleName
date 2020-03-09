
import requests 
from bs4 import BeautifulSoup  # pip install bs4 && python3 -m pip install lxml 

def link_to_soup(link):
    r = requests.get(link).text
    return BeautifulSoup(r, 'lxml')  # 'html.parser' instead of 'lxml'

def parse_semester(year, sem, json_out):  #2020, spring
    link = f'https://courses.illinois.edu/cisapp/explorer/schedule/{year}/{sem.lower()}.xml'
    soup = link_to_soup(link)
    for subject in soup.find_all('subject'):
        try:
            print(subject['id'])
            parse_subject(subject['href'])
        except:
            print("ERROR: could not parse:\n\t", subject)
    pass

def parse_subject(link):
    soup = link_to_soup(link)
    for course in soup.find_all('course'):
        try:
            print(course['id'])
            parse_class(course['href'])
        except:
            print("ERROR: could not parse:\n\t", course)

def parse_class(link):
    soup = link_to_soup(link)
    for section in soup.find_all('section'):
        try:
            print(section.text)
            parse_section(section['href'])
        except:
            print("ERROR: could not parse:\n\t", section)

def parse_section(link):
    soup = link_to_soup(link)
    for meeting in soup.find_all('meeting'):
        if meeting.buildingname is not None:
            print(meeting.buildingname.text, meeting.roomnumber.text)
            print(meeting.start.text, "->", meeting.end.text)
        else:
            print('Online')

if __name__ == '__main__':
    # TODO revert to friendly user input
    # year = input('Enter year: ')
    # sem = input('Enter semester (fall/spring): ')
    # parse_semester(year, sem, None)
    parse_semester(2020, 'spring', None)

''' 
    TODO
nullchecks
start/end dates in parse_section (for half-sem courses)?
actual XML parser or is HTML ok?
list of meetings
'''

# testing
# parse_section('https://courses.illinois.edu/cisapp/explorer/schedule/2020/spring/AAS/100/30107.xml')
# parse_class('https://courses.illinois.edu/cisapp/explorer/schedule/2020/spring/AAS/100.xml')
# parse_subject('https://courses.illinois.edu/cisapp/explorer/schedule/2020/spring/AAS.xml')


import requests 
from bs4 import BeautifulSoup  # pip install bs4 && python3 -m pip install lxml 

def link_to_soup(link):
    r = requests.get(link).text
    return BeautifulSoup(r, 'lxml')  # 'html.parser' instead of 'lxml'

def parse_semester(year, sem, json_out):
    pass

def parse_subject(link):
    soup = link_to_soup(link)
    courses = soup.find_all('course')
    for course in courses:
        try:
            parse_section(course['href'])
        except:
            print("ERROR: could not parse:\n\t", course)

def parse_class(link):
    soup = link_to_soup(link)
    sections = soup.find_all('section')
    for section in sections:
        try:
            parse_section(section['href'])
        except:
            print("ERROR: could not parse:\n\t", section)

def parse_section(link):
    soup = link_to_soup(link)
    # print(soup.prettify())
    print(soup.buildingname.text, soup.roomnumber.text)
    print(soup.start.text, "->", soup.end.text)


# parse_section('https://courses.illinois.edu/cisapp/explorer/schedule/2020/spring/AAS/100/30107.xml')
# parse_class('https://courses.illinois.edu/cisapp/explorer/schedule/2020/spring/AAS/100.xml')
parse_subject('https://courses.illinois.edu/cisapp/explorer/schedule/2020/spring/AAS.xml')

''' 
    TODO
nullchecks
start/end dates in parse_section (for half-sem courses)?
actual XML parser or is HTML ok?
'''
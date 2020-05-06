"""
Parses a json of the following format:
{ 
    'courses': [
        { 
            'course_num': '225',
            'department': 'CS',
            'prereqs': ['String with "Prerequisite:" in it'],
            'sections': [
                {
                    'section': 'ADE',
                    'crn': '618201',
                    'meetings': [
                        {
                            'building': 'Siebel',
                            'room': '234',
                            'start': '9:00am',
                            'end': '9:50am',
                            'days': 'MW'
                        }
                    ]
                }
            ]
        }
    ]
}
"""

import json
from tqdm import tqdm
from server.gdb import Neo4jInterface

if __name__ == '__main__':

    try:
        print("Running...")
        db = Neo4jInterface('bolt://localhost:7687', 'neo4j', 'password')
        with open('cisdata.json', 'r') as json_file:
            data = json.load(json_file)
            with tqdm(data['courses']) as t:
                for course in t:
                    db.add_course(course['department'], course['course_num'])
                    for section in course['sections']:
                        db.add_section(course['department'], course['course_num'], section['crn'])
                        for meeting in section['meetings']:
                            if meeting['building'] is not None:
                                db.add_meeting(section['crn'], meeting['start'], meeting['end'], meeting['building'],
                                               meeting['room'], meeting['days'])
        print('Done!')
    except Exception as e:
        print('Make sure "cisdata.json" is in this directory, and the Neo4j command line arguments are correct.')
        print('Make sure the Neo4j server is created and started.')
        print(e)

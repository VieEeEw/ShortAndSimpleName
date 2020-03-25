
import json
from bs4 import BeautifulSoup
from neo4j_interface import Neo4j_Interface


if __name__ == '__main__':
    try:
        db = Neo4j_Interface('bolt://localhost:7687', 'neo4j', 'password')
        with open('cisdata.json', 'r') as json_file:
            data = json.load(json_file)
            for course in data['courses']:
                db.add_course(course['department'], course['course_num'])
                for section in course['sections']:
                    db.add_section(course['department'], course['course_num'], section['crn'])
                    for meeting in section['meetings']:
                        if meeting['building'] is not None:
                            db.add_meeting(section['crn'], meeting['start'], meeting['end'], meeting['building'], meeting['room'])
    except Exception as e:
        print('Make sure "cisdata.json" is in this directory')
        print(e)

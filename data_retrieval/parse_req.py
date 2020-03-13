
import json
from bs4 import BeautifulSoup

def parse_prereq(prereq):  # TODO
    return prereq

if __name__ == '__main__':
    with open('prereqs.txt', 'w') as prereq_out:
        try:
            count = 0
            with open('cisdata.json', 'r') as json_file:
                json_str = ''
                for line in json_file:
                    json_str += line
                json_data = json.loads(json_str)
                for course in json_data['courses']:
                    course['prereqs'] = parse_prereq(course['prereqs'])
                    if len(course['prereqs']) > 0:
                        count += 1
                        prereq_out.write(str(course['prereqs']))
                        prereq_out.write('\n')
            print(f'{count} lines written to "prereqs.txt"')
        except Exception as e:
            print('Make sure "cisdata.json" is in this directory')
            print(e)

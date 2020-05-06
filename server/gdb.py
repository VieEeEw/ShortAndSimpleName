from neo4j import GraphDatabase
from flask import current_app, g
import urllib.request
import json
from itertools import permutations
from datetime import datetime

"""
Initialize an interface with: Neo4j_Interface(URI, USER, PW)
example: 
    db = Neo4jInterface('bolt://localhost:7687', 'neo4j', 'password')
    db.add_course("CS", 411)

See available functions in the Neo4j_Interface() class.
Parameters are always strings, but ints should be internally converted to ints.

For ER diagram, see:
https://wiki.illinois.edu/wiki/display/CS411AASP20/ShortAndSimpleName+-+ER+Design
NOTE: user and prereqOf not implemented yet
TODO: update ER diagram with digital version and normalized capitalization

"""

class Neo4jInterface:

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    # -------  ADVANCED FEATURE  ------- #
    def get_intersection(self, crn_list_1, crn_list_2):
        """
        Finds all possible path intersections between 2 lists of crn enrollments
        :param crn_list_1 crn_list_2: list of crn numbers (can be strings or numbers)
        :return:
        {
            'intersections': [
                {
                    'intersection': {
                        'lat': 40.1036517, 
                        'long': -88.2279429,
                        'time_window': {
                            'start': '1:50pm',
                            'end': '2:00pm'
                            'days': 'MW'
                        }
                    },
                    'student1': {
                        'crn_from': '61820',
                        'crn_to': '42069',
                        'success': True,  # if Google API succeeded
                        'steps': [
                            {
                                'from': {
                                    'lat': 40.1036517,
                                    'long': -88.2279429
                                },
                                'to': {
                                    'lat': 40.10535530000001,
                                    'long': -88.2279397
                                },
                                'seconds': 134  # time taken walking
                            },
                        ],
                        'start_address': 'David Kinley Hall, 1407 W Gregory Dr, Urbana, IL 61801, USA',
                        'start_location': {
                            'lat': 40.1036517,
                            'lng': -88.2279429
                        },
                        'end_address': '201 N Goodwin Ave, Urbana, IL 61801, USA',
                        'end_location': {
                            'lat': 40.1138291,
                            'lng': -88.2256426
                        },  
                    }
                    'student2': {
                        # similar to student1
                    }
                }
            ]
        }
        """
        json_ret = {'intersections': []}
        meetings1 = self._get_meetings(crn_list_1)
        meetings2 = self._get_meetings(crn_list_2)

        paths1 = list(permutations(meetings1, 2))
        paths2 = list(permutations(meetings2, 2))

        for path1 in paths1:
            time_window1 = self._get_time_window(path1)
            if time_window1 is None:
                continue
            dir1 = self.get_directions(path1[0]['building'], path1[1]['building'])
            if not dir1['success']:
                continue
            for path2 in paths2:
                # TODO cache results
                time_window2 = self._get_time_window(path2)
                if time_window2 is None:
                    continue

                if not self._time_window_overlap(time_window1, time_window2):
                    continue

                dir2 = self.get_directions(path2[0]['building'], path2[1]['building'])
                if not dir2['success']:
                    continue

                intersection = self.intersect_paths(dir1['steps'], dir2['steps'])
                if intersection['intersects']:  # we found an intersection!
                    json_i = self._make_intersection_json(intersection, 
                        (dir1, path1[0]['crn'], path1[1]['crn'], time_window1), 
                        (dir2, path2[0]['crn'], path2[1]['crn'], time_window2))
                    json_ret['intersections'].append(json_i)
        return json_ret

    def _get_time_window(self, path):
        """
        Find the time window where the student could be walking between 2 classes
        :param path: a tuple of meeting dictionaries (from, to), see 'meetings' in get_crn_data() 
        :return: None if invalid pair of classes, otherwise a dictionary:
            {
                'start': datetime.datetime object,
                'end': datetime.datetime object,
                'days': 'MW'
            }
        """
        time_window = {
                'start': datetime.strptime(path[0]['end'].strip(), '%I:%M %p'),
                'end': datetime.strptime(path[1]['start'].strip(), '%I:%M %p'),
                'days': self._day_intersection(path[0]['days'].strip(), path[1]['days'].strip())
        }

        if (time_window['start'] > time_window['end']):  # I'm walking to a class that has already passed
            return None

        if len(time_window['days']) == 0:  # No days overlap
            return None

        return time_window

    def _make_intersection_json(self, intersection, info1, info2):
        """
        Builds a dictionary to be added to the array 'intersections' in get_intersection()
        :param intersection: dictionary returned by intersect_paths()
        :param info1: tuple of the format (dir, crn_from, crn_to, time_window)
            ex. (get_directions(), '61820', '42069', _get_time_window())
        :param info2: see :param info1
        :return: see dictionary in the array 'intersections' in get_intersection()
        """
        dir1, crn_from1, crn_to1, time_window1 = info1
        dir2, crn_from2, crn_to2, time_window2 = info2

        json_i = {
            'intersection': {
                'lat': intersection['lat'],
                'long': intersection['long'],
                'time_window': {
                    'start': max(time_window1['start'], time_window2['start']).strftime('%I:%M %p'),  # latest start
                    'end': min(time_window1['end'], time_window2['end']).strftime('%I:%M %p'),  # earliest end 
                    'days': self._day_intersection(time_window1['days'], time_window2['days'])
                }
            },
            'student1': dir1,
            'student2': dir2 
        }
        json_i['student1']['crn_from'] = crn_from1
        json_i['student1']['crn_to'] = crn_to1
        json_i['student2']['crn_from'] = crn_from2
        json_i['student2']['crn_to'] = crn_to2
        return json_i

    def _time_window_overlap(self, time_window1, time_window2):
        """
        Finds an intersections between 2 paths
        :param time_window1: See output for _get_time_window
        :param time_window2: See output for _get_time_window
        :return: bool if they overlap
        """
        if time_window1['start'] > time_window2['end'] or time_window2['start'] > time_window1['end']:
            return False
        if len(self._day_intersection(time_window1['days'], time_window2['days'])) == 0:
            return False
        return True

    def _day_intersection(self, days1, days2):
        """
        Finds an intersections between 2 paths
        :param days1: string containing only the letter for the days of the week; ex. 'MW'
        :param days2: Same as :param days1.
        :return: The common letters between days1 and days2
        """
        return ''.join([day for day in days1 if day in days2])

    def intersect_paths(self, steps1, steps2):
        """
        Finds an intersections between 2 paths
        :param steps1: array of steps (see 'steps' key in result of get_directions()).
        :param steps2: Same as :param step1.
        :return: { 
            'intersects': true
            'lat': 40.1036517, 
            'long': -88.2279429 
        }
        """
        for s1 in steps1:
            s1_p1 = (s1['from']['lat'], s1['from']['long'])
            s1_p2 = (s1['to']['lat'], s1['to']['long'])
            for s2 in steps2:
                s2_p1 = (s2['from']['lat'], s2['from']['long'])
                s2_p2 = (s2['to']['lat'], s2['to']['long'])
                p = self._line_intersection((s1_p1, s1_p2), (s2_p1, s2_p2))
                if p is not None:
                    return {'intersects': True, 'lat': p[0], 'long': p[1]}
        return {'intersects': False, 'lat': None, 'long': None}

    def get_directions(self, building_from, building_to):
        """
        Finds a list of gps cords between building_from and building_to, utilizing Google Maps Directions API
        :param building_from: building name strings (ex. 'Siebel Center for Comp Sci')
        :param building_to: See :param building_from
        :return: 
                { 
                    'success': True
                    'steps': [
                        {
                            'from': {
                                'lat': 40.1036517,
                                'long': -88.2279429
                            },
                            'to': {
                                'lat': 40.10535530000001,
                                'long': -88.2279397
                            },
                            'seconds': 134  # time taken walking
                        },
                    ],
                    'start_address': 'David Kinley Hall, 1407 W Gregory Dr, Urbana, IL 61801, USA',
                    'start_location': {
                        'lat': 40.1036517,
                        'lng': -88.2279429
                    },
                    'end_address': '201 N Goodwin Ave, Urbana, IL 61801, USA',
                    'end_location': {
                        'lat': 40.1138291,
                        'lng': -88.2256426
                    },  
                }
        """
        json_ret = {'steps': [], 'start_address': None, 'start_location': None, 'end_address': None,
                    'end_location': None, 'success': False}
        try:
            with open('google_backend.key', 'r') as f:
                api_key = f.read()
        except Exception:
            raise (FileNotFoundError(
                'Unable to read Google Maps API Key for the backend.\n'
                'Please save this key in "server/google_backend.key"'))

        # URL spacing # TODO localization?
        origin = building_from.replace(' ', '+') + ('+UIUC')
        destination = building_to.replace(' ', '+') + ('+UIUC')

        # Build URL for request
        endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
        url_variables = f'origin={origin}&destination={destination}&mode=walking&key={api_key}'
        request = endpoint + url_variables
        try:
            response = urllib.request.urlopen(request).read()
            directions = json.loads(response)
            routes = directions['routes']
            route = routes[0]  # defaulting to first route; if there are no routes, will throw exception
            leg = route['legs'][0]  # defaulting to closest match of locations

            json_ret['start_address'] = leg['start_address']
            json_ret['start_location'] = leg['start_location']
            json_ret['end_address'] = leg['end_address']
            json_ret['end_location'] = leg['end_location']
            for step in leg['steps']:
                json_ret['steps'].append({
                    'from': {
                        'lat': step['start_location']['lat'],
                        'long': step['start_location']['lng'],
                    },
                    'to': {
                        'lat': step['end_location']['lat'],
                        'long': step['end_location']['lng'],
                    },
                    'seconds': step['duration']['value']
                })
            json_ret['success'] = True
        except Exception as e:
            json_ret['success'] = False
            print(f'Got an error of type {type(e)} and message {e}'
                  f'\n(BAD RESPONSE FROM GOOGLE MAPS -> bad api key? bad internet?)')
        return json_ret

    # -------  GET DATA FROM NEO4J  ------- #
    def get_crn_data(self, crn):
        """
        :return: {
            'crn': '54523', 
            'dept': 'AAS', 
            'course_num': '281', 
            'meetings': [
                {
                    'building': 'Gregory Hall', 
                    'room': '307', 
                    'start': '11:00 AM', 
                    'end': '11:50 AM',
                    'days': 'MW'
                }
            ]}
        All fields except 'crn' are populated with NULLs if the course not found, and meetings is the empty list
        """
        with self._driver.session() as session:
            return session.write_transaction(self._get_crn_data, str(crn))

    def count_nodes(self):
        """
        :return: str(length)
        """
        with self._driver.session() as session:
            return session.write_transaction(self._count_nodes)

    # -------  ADD DATA TO NEO4J  ------- #
    def add_course(self, dept, num):
        with self._driver.session() as session:
            session.write_transaction(self._add_course, dept, str(num))

    def add_section(self, dept, num, crn):
        with self._driver.session() as session:
            session.write_transaction(self._add_section, dept, str(num), str(crn))

    def add_meeting(self, crn, start, end, building, room, days):
        with self._driver.session() as session:
            session.write_transaction(self._add_meeting, str(crn), start, end, building, str(room), days)

    # -------  DELETE FROM NEO4J  ------- #
    def delete_all(self):
        with self._driver.session() as session:
            session.write_transaction(self._delete_all)

    def close(self):
        self._driver.close()

    # -------  Helper Functions  ------- #
    def _get_meetings(self, crn_list):
        """
        Cover list of CRNs into list of meeting dictionaries
        each dictionary gets a new key: 'crn'
        :return:
            [{
                'building': 'Gregory Hall', 
                'room': '307', 
                'start': '11:00 AM', 
                'end': '11:50 AM',
                'days': 'MW',
                'crn': '66935'
            }]
        """
        meetings = []
        for crn in crn_list:
            crn_meetings = self.get_crn_data(crn)['meetings']
            for meeting in crn_meetings:
                meeting['crn'] = str(crn)
            meetings += crn_meetings
        return meetings

    @staticmethod
    def _line_intersection(line1, line2):
        """
        Find the intersection of 2 line segments
        :param line1, line2: tuple of coordinate tuples; ex. ( (0,1), (2,2) )
        :return: (x,y) coordinate, or None if no intersection
        """
        x_diff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        y_diff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(x_diff, y_diff)
        if div == 0:
            return None

        d = (det(*line1), det(*line2))
        x = det(d, x_diff) / div
        y = det(d, y_diff) / div

        # additional checks for line segment
        x_rang = (line1[0][0], line1[1][0])
        y_rang = (line1[0][1], line1[1][1])

        if min(x_rang) < x < max(x_rang) and min(y_rang) < y < max(y_rang):
            return x, y
        return None

    # -------  Transaction methods for Neo4j  ------- #
    @staticmethod
    def _get_crn_data(tx, crn):
        result = tx.run(
            "MATCH (c:Course)<-[:SectionOf]-(s:Section)<-[:MeetsFor]-(m:Meeting)-[:LocatedAt]->(b:Building) "
            "WHERE s.crn = $crn "
            "RETURN c, s, m, b",
            crn=crn)
        json_ret = {'crn': crn, 'dept': None, 'course_num': None, 'meetings': []}
        for record in result.records():
            course = record['c']
            json_ret['dept'] = course.get('dept')
            json_ret['course_num'] = course.get('num')

            meeting = record['m']
            building = record['b']
            json_ret['meetings'].append(
                {
                    'building': building.get('name'),
                    'room': meeting.get('room'),
                    'start': meeting.get('start'),
                    'end': meeting.get('end'),
                    'days': meeting.get('days')
                })
        return json_ret

    @staticmethod
    def _count_nodes(tx):
        result = tx.run("MATCH (a) "
                        "RETURN a")
        return str(len([i for i in result.records()]))

    @staticmethod
    def _add_course(tx, dept, num):
        tx.run(
            "CREATE (c:Course { dept: $dept, num: $num }) ",
            dept=dept, num=num)

    @staticmethod
    def _add_section(tx, dept, num, crn):
        tx.run(
            "MATCH (c:Course) WHERE c.dept = $dept AND c.num = $num "
            "CREATE (s:Section { crn: $crn }) "
            "CREATE (s)-[:SectionOf]->(c)",
            dept=dept, num=num, crn=crn)

    @staticmethod
    def _add_meeting(tx, crn, start, end, building, room, days):
        tx.run(
            "MATCH (s:Section) WHERE s.crn = $crn "
            "CREATE (m:Meeting { room: $room, start: $start, end: $end, days: $days }) "
            "MERGE (b:Building { name: $building }) "
            "CREATE (m)-[:MeetsFor]->(s) "
            "CREATE (m)-[:LocatedAt]->(b)",
            crn=crn, room=room, start=start, end=end, building=building, days=days)

    @staticmethod
    def _delete_all(tx):
        tx.run(
            "MATCH (a) "
            "DETACH DELETE a ")


def get_graph_db() -> Neo4jInterface:
    """
    Create an connection with neo4j database for each request.
    :return: The neo4j database (An instance of Neo4jInterface)
    """
    if 'graph_db' not in g:
        g.graph_db = Neo4jInterface(current_app.config['GRAPH_DB']['url'], current_app.config['GRAPH_DB']['username'],
                                    current_app.config['GRAPH_DB']['pswd'])
    return g.graph_db


def close_graph_db(e=None):
    """
    Close the current connection with neo4j database for each request
    :param e: Unknown error parameter
    :return: None
    """
    try:
        g.pop('graph_db', None).close()
    except AttributeError:
        return


def register_graph_db(app):
    app.teardown_appcontext(close_graph_db)


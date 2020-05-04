from neo4j import GraphDatabase
from flask import current_app, g
import urllib.request
import json

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
    def get_intersection(self, steps1, steps2):
        """
        Finds an intersections between 2 paths
        :param steps1, steps2: array of steps (see 'steps' key in result of get_directions())
        :return: { 
            'lat': 40.1036517, 
            'long': -88.2279429 
        }
        All return fields are NULL if the paths do not intersect
        """
        for s1 in steps1:
            s1_p1 = (s1['from']['lat'], s1['from']['long'])
            s1_p2 = (s1['to']['lat'], s1['to']['long'])
            for s2 in steps2:
                s2_p1 = (s2['from']['lat'], s2['from']['long'])
                s2_p2 = (s2['to']['lat'], s2['to']['long'])
                p = LineTools.line_segment_intersection(s1_p1, s1_p2, s2_p1, s2_p2)
                if p is not None:
                    return { 'lat': p[0], 'long': p[1] }
        return { 'lat': None, 'long': None }

    def get_directions(self, building_from, building_to):
        """
        Finds a list of gps cords between building_from and building_to
        :param building_from, building_to: building name strings (ex. 'Siebel Center for Comp Sci')
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
        json_ret = { 'steps': [], 'start_address': None, 'start_location': None, 'end_address': None, 'end_location': None, 'success': False }
        try:
            with open('google_backend.key', 'r') as f:
                api_key = f.read()
        except Exception as e:
            raise(Exception('Unable to read Google Maps API Key for the backend.\nPlease save this key in "server/google_backend.key"'))

        # URL spacing # TODO add ",+UIUC" for localization?
        origin = building_from.replace(' ', '+')
        destination = building_to.replace(' ', '+')

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
                json_ret['steps'].append( {
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
        except:
            json_ret['success'] = False
            print('BAD RESPONSE FROM GOOGLE MAPS')  # bad api key, bad internet, or Google json missing attributes 
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
                    'end': '11:50 AM'
                }
            ]}
        All fields except 'crn' are populated with NULLs if the course not found
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

    def add_meeting(self, crn, start, end, building, room):
        with self._driver.session() as session:
            session.write_transaction(self._add_meeting, str(crn), start, end, building, str(room))

    # -------  DELETE FROM NEO4J  ------- #
    def delete_all(self):
        with self._driver.session() as session:
            session.write_transaction(self._delete_all)

    # close the driver
    def close(self):
        self._driver.close()


    # internal helper methods:
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
                    'end': meeting.get('end')
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
    def _add_meeting(tx, crn, start, end, building, room):
        tx.run(
            "MATCH (s:Section) WHERE s.crn = $crn "
            "CREATE (m:Meeting { room: $room, start: $start, end: $end }) "
            "MERGE (b:Building { name: $building }) "
            "CREATE (m)-[:MeetsFor]->(s) "
            "CREATE (m)-[:LocatedAt]->(b)",
            crn=crn, room=room, start=start, end=end, building=building)

    @staticmethod
    def _delete_all(tx):
        tx.run(
            "MATCH (a) "
            "DETACH DELETE a ")

class LineTools:
    @staticmethod
    def slope(a, b):
        '''
        :param a, b: (x,y) cordinate tuples
        :return: slope (number)
        '''
        # slope = (y2 - y1) / (x2 - x1)
        dy = b[1] - a[1]
        dx = b[0] - a[0]
        if dx == 0:
            return 999999
        return dy / dx

    @staticmethod
    def yintercept(a, slope):
        '''
        :param a: (x,y) cordinate tuple
        :param slope: number
        :return: y value (number)
        '''
        # yintercept = y - mx
        return a[1] - slope*a[0]

    @staticmethod
    def line_intersection(a, b, c, d):
        '''
        :param a,b,c,d: (x,y) cordinate tuples
        :return: (x,y) cordinate intersection of the lines ab and cd, or None if no intersection
        '''
        # y = mx + b
        # Y = MX + B
        # (x=X) = (B - b) / (m - M)
        slope1 = LineTools.slope(a, b)
        yint1 = LineTools.yintercept(a, slope1)
        slope2 = LineTools.slope(c, d)
        yint2 = LineTools.yintercept(c, slope2)

        if slope1 == slope2: # parallel
            if yint1 == yint2:  # same line
                return a
            return None

        x = (yint2 - yint1) / (slope1 - slope2)
        y = slope1 * x + yint1
        return (x, y)

    @staticmethod
    def line_segment_intersection(a1, a2, b1, b2):
        '''
        :param a1,a2,b1,b2: (x,y) cordinate tuples (segment is from a1 to a2, and b1 to b2)
        :return: (x,y) cordinate intersection of line segments ab and cd, or None if no intersection
        '''
        x_rang = a1[0], a2[0]
        y_rang = a1[1], a2[1]
        p = LineTools.line_intersection(a1, a2, b1, b2)
        if p is None:
            return None
        if x_rang[0] < p[0] < x_rang[1] and y_rang[0] < p[1] < y_rang[1]:
            return p
        return None


def get_graph_db():
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

'''
Initialize an interface with: Neo4j_Interface(URI, USER, PW)
example: 
    db = Neo4j_Interface('bolt://localhost:7687', 'neo4j', 'password')
    db.add_course("CS", 411)

See available functions in the Neo4j_Interface() class.
Parameters are always strings, but ints should be internally converted to ints.

For ER diagram, see:
https://wiki.illinois.edu/wiki/display/CS411AASP20/ShortAndSimpleName+-+ER+Design
NOTE: user and prereqOf not implemented yet
TODO: update ER diagram with digital version and normalized capitalization


'''

from neo4j import GraphDatabase
from flask import current_app, g


class Neo4j_Interface():

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    # TODO:
    # course -> get info
    # course -> get sections
    # crn (section) -> get meetings

    # -------  GET DATA FROM NEO4J  ------- #
    def get_crn_data(self, crn):
        with self._driver.session() as session:
            return session.write_transaction(self._methods._get_crn_data, str(crn))

    def count_nodes(self):
        with self._driver.session() as session:
            return session.write_transaction(self._methods._count_nodes)

    # -------  ADD DATA TO NEO4J  ------- #
    def add_course(self, dept, num):
        with self._driver.session() as session:
            session.write_transaction(self._methods._add_course, dept, str(num))

    def add_section(self, dept, num, crn):
        with self._driver.session() as session:
            session.write_transaction(self._methods._add_section, dept, str(num), str(crn))

    def add_meeting(self, crn, start, end, building, room):
        with self._driver.session() as session:
            session.write_transaction(self._methods._add_meeting, str(crn), start, end, building, str(room))

    # -------  DELETE FROM NEO4J  ------- #
    def delete_all(self):
        with self._driver.session() as session:
            session.write_transaction(self._methods._delete_all)

    # close the driver
    def close(self):
        self._driver.close()

    # internal helper methods
    class _methods():

        @staticmethod
        def _get_crn_data(tx, crn):
            result = tx.run(
                "MATCH (c:Course)<-[:SectionOf]-(s:Section)<-[:MeetsFor]-(m:Meeting)-[:LocatedAt]->(b:Building) "
                "WHERE s.crn = $crn "
                "RETURN c, s, m, b",
                crn=crn)
            json = {'crn': crn, 'dept': None, 'course_num': None, 'meetings': []}
            for record in result.records():
                course = record['c']
                json['dept'] = course.get('dept')
                json['course_num'] = course.get('num')

                meeting = record['m']
                building = record['b']
                json['meetings'].append(
                    {
                        'building': building.get('name'),
                        'room': meeting.get('room'),
                        'start': meeting.get('start'),
                        'end': meeting.get('end')
                    })
            return json

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


def get_graph_db():
    if 'graph_db' not in g:
        g.graph_db = Neo4j_Interface('bolt://localhost:7687', 'neo4j', 'password')
    return g.graph_db


def close_graph_db(e=None):
    try:
        g.pop('graph_db', None).close()
    except AttributeError:
        return


def register_graph_db(app):
    app.teardown_appcontext(close_graph_db)


if __name__ == "__main__":
    # test code for starting from a naked neo4j database

    # db = Neo4j_Interface('bolt://localhost:7687', 'neo4j', 'password')

    # db.delete_all()
    # db.add_course("CS", 225)

    # db.add_course("CS", 411)
    # db.add_section("CS", 411, 61802)

    # db.add_meeting(61802, "9:00pm", "11:00pm", "Siebel", 214)
    # db.add_meeting(61802, "8:00pm", "9:00pm", "ECEB", 214)

    # db.add_section("CS", 411, 61869)
    # db.add_meeting(61869, "1:00pm", "2:00pm", "Siebel", 214)

    # print(db.count_nodes())
    # print(db.get_crn(62102))

    pass

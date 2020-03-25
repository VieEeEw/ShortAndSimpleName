
from neo4j import GraphDatabase

URI = 'bolt://localhost:7687'
USER = 'neo4j'
PW = 'password'

class Neo4j_Interface():

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    def close(self):
        self._driver.close()

    def delete_all(self):
        with self._driver.session() as session:
            session.write_transaction(self._methods._delete_all)

    def count_nodes(self):
        with self._driver.session() as session:
            session.write_transaction(self._methods._count_nodes)

    def add_course(self, dept, num):
        with self._driver.session() as session:
            session.write_transaction(self._methods._add_course, dept, num)

    def add_section(self, dept, num, crn):
        with self._driver.session() as session:
            session.write_transaction(self._methods._add_section, dept, num, crn)

    def add_meeting(self, crn, start, end, building, room):
        with self._driver.session() as session:
            session.write_transaction(self._methods._add_meeting, crn, start, end, building, room)

    # TODO:
    # course -> get info
    # course -> get sections
    # crn (section) -> get meetings

    class _methods():
        
        @staticmethod
        def _delete_all(tx):
            tx.run(
                "MATCH (a) "
                "DETACH DELETE a ")         

        @staticmethod
        def _count_nodes(tx):
            result = tx.run("MATCH (a) "
                            "RETURN a")
            print(f'num of nodes: {len([i for i in result.records()])}')

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
                "CREATE (m)-[:locatedAt]->(b)",
                crn=crn, room=room, start=start, end=end, building=building)


if __name__ == "__main__":
    db = Neo4j_Interface(URI, USER, PW)

    db.delete_all()
    # db.add_course("CS", 225)

    # db.add_course("CS", 411)
    # db.add_section("CS", 411, 61802)

    # db.add_meeting(61802, "9:00pm", "11:00pm", "Siebel", 214)
    # db.add_meeting(61802, "8:00pm", "9:00pm", "ECEB", 214)

    # db.add_section("CS", 411, 61869)
    # db.add_meeting(61869, "1:00pm", "2:00pm", "Siebel", 214)

    db.count_nodes()

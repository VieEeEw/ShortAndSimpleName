
from neo4j import GraphDatabase


class Neo4j_Interface():

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    def close(self):
        self._driver.close()

    def print_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._methods._create_and_return_greeting, message)
            print(greeting)

    def delete_all_nodes(self):
        with self._driver.session() as session:
            session.write_transaction(self._methods._delete_all_nodes)

    def select_all_nodes(self):
        with self._driver.session() as session:
            session.write_transaction(self._methods._select_all_nodes)

    class _methods():
        
        @staticmethod
        def _delete_all_nodes(tx):
            tx.run("MATCH (a)"
                    "DELETE (a)")         

        @staticmethod
        def _create_and_return_greeting(tx, message):
            result = tx.run("CREATE (a:Greeting {message: $message}) "
                            "RETURN a.message", 
                            message=message)
            return result.single()[0]

        @staticmethod
        def _select_all_nodes(tx):
            result = tx.run("MATCH (a) "
                            "RETURN a")
            print(f'num of nodes: {len([i for i in result.records()])}')


if __name__ == "__main__":
    db = Neo4j_Interface('bolt://localhost:7687', 'neo4j', 'password')
    db.delete_all_nodes()
    db.print_greeting("hellow!")
    db.print_greeting("hellow!")
    db.select_all_nodes()

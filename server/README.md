# USAGE
First get into the project directory\
`pip install -r pip-requirements.txt OR conda install --file conda-requirements.txt`\
`SET FLASK_APP=server`\
`SET FLASK_ENV=development`\
(If on linux system, use export instead of set)\
At first run, initialize relational database by running the following command\
`flask init-db`\
See [First-time Neo4j Setup](#First-time Neo4j Setup) below.\
Then run the following command to start the server\
`flask run`\
Follow the appearing instructions to access the website.



### First-time Neo4j Setup

A Neo4j server needs to be running locally on your machine.

Download Neo4j at https://neo4j.com/download/ (you may need to create an account)

Using the downloaded application, create a new project/graph with:

* username = neo4j

* password = password

Press the start button.

From the `server` directory, run in bash/terminal:

```bash
python3 json_to_neo4j.py bolt://localhost:7687 neo4j password
```

NOTE: this will take several minutes to execute.



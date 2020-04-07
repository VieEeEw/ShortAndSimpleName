# USAGE
First get into the project directory\
`python3 -m pip install --user virtualenv`\
Make a virtual environment: `python3 -m venv 411env`\
Work on the virtual environment: `source 411env/bin/activate`\
`pip install -r pip-requirements.txt OR conda install --file conda-requirements.txt`\
`SET FLASK_APP=server`\
`SET FLASK_ENV=development`\
(If on linux system, use export instead of set)\
See **First-time Neo4j Setup** below.\
At first run, initialize relational database by running the following command\
`flask init-db`\
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





### BUGS

NOTE: this seems to be fixed by the use of virtual environments

If `flask run` produces a website that crashes and complains about a neo4j module that doesn't exist, run (on Linux)

```
pip install -r pip-requirements.txt
python3 -c "import server.__init__ as s; s.create_app().run()"
```

This will use the Python3 executable associated with pip.
 You may need to replace pip with pip3 above, depending on how you configured your system.



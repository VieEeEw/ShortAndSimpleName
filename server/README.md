# USAGE
First get into the project directory
## Virtual Environment
### virtualenv with pip
Make sure `virtualenv` is installed with pip corresponding to the python you want to use(python3.7 or above recommended),
say the python (executable) file is named as `python`\
Inside the project directory, run `python -m virtualenv <virtualenv_name>` to make a virtual environment inside ./<virtualenv_name>, using `venv` here.\
Activate the virtualenv:\
Windows: `venv/Scripts/activate.bat\`
Linux/Unix: `source ./venv/bin/activate`.\
After activating the virtual environment, run the following command to install the required packages\
`pip install -r pip-requirements.txt`
### Anaconda
Strongly recommend using anaconda!\
First have [anaconda](https://www.anaconda.com/) installed. Add conda to path in its installation console.\
Run `conda create --name <env> --file conda-requirements.txt` to build a environment naming <env>, using `env` here.\
Activate conda virtual environment: `conda activate env`\
### Letting [PyCharm](https://www.jetbrains.com/pycharm/) doing these
PyCharm is an IDE that provides extremely powerful support for virtual environment, considering using PyCharm is a good idea.



### Obtaining the Google Maps API key

In the `server` directory, create the file: `google_backend.key`.

Go to the "random" chat on slack and copy the backend key into it.



## Running the server
***Be sure to finish setting up the virtual environment and activate it before going in this step***\
First, in config.py file, set your neo4j url, username and password in GRAPH_DB dictionary variable.\
Set two variables in terminal(shell)
`SET FLASK_APP=server` \
`SET FLASK_ENV=development`(if in development mode)\
(Switch `SET` to `export` on Linux/Unix OS)\
At first run, initialize the relational database by running the following command\
`flask init-db` (See **First-time Neo4j Setup** below)\
Before run the server, you can run a pre-test `flask test-server`.\
Then run the following command to start the server\
`flask run`\
If the database has been initialized, run `run-server.bat` or `./run-server.sh` 



### First-time Neo4j Setup (Importing data)

A Neo4j server needs to be running locally on your machine.

Download [Neo4j Desktop](https://neo4j.com/download/) (you may need to create an account)

Using the downloaded application, create a new project/graph with:

* username = neo4j

* password = password

Press the start button.

From the `server` directory, run in bash/terminal:

```bash
python3 json_to_neo4j.py bolt://localhost:7687 neo4j password
```

NOTE: this will take several minutes to execute.



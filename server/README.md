#USAGE
First get into the project directory\
`pip install -r pip-requirements.txt` or\
`conda install --file conda-requirements.txt` (see comments in conda-requirements.txt if created env from file)\
`SET FLASK_APP=server` \
`SET FLASK_ENV=development`\
(If on linux system, use `export` instead of `SET`)\
Be sure to activate the environment before the following commands.\
At first run, initialize database (relational database done, neo4j in progress) by running the following command\
`flask init-db`\
Then run the following command to start the server\
`flask run`\
Follow the appearing instructions to access the website.
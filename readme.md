# EDM System Automation Framework

This software is a Python package which allows to automate [EDM System](https://github.com/alecxcode/edm) workflows. For instance, the following workflows could be done with Python scripts:
* create a task, document, or post other data
* get a task, document, or other data from the system and submit it elsewhere
* collect data from other sources (e.g. from chats, databases, queues collect incoming messages representing tasks, documents, etc.), and post necessary objects to the system
* analyze data and make decisions
* other similar workflows

## Automated testing
Another goal of this software is to provide the complete automated integration testing for EDM System.

## How to use
In order to connect to the system the program will try to open `connect.txt` file. If the file does not exist it will be created with default content. See `get_conn_data_from_file()` for details.

For automation purposes import required modules and functions from this package, create your business logic and (micro)services, then use with running EDM System server.

For integration testing install and launch EDM System on you computer, install requirements (see `requirements.txt`), download this repository, and run: `python3 run.py`
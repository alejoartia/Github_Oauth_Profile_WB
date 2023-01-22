# Execution: 

## to run it locally , in the root of you project:
- in the root path of the project
- create virtual environment:
    - python3 -m virtualenv <name_of_virtual_env>
    - source <name_of_virtual_env>/bin/activate
    - or use poetry or pipenv as you prefer
- be sure you are in the 'main' branch
- run:
  uvicorn app.index:app --host 0.0.0.0 --port 15400 --reload


## To run with docker compose.  be sure you have docker installed:
- be sure you are in the main branch
- docker-compose up -d 


## You will be also to see the app deployed at:
- https://wolf-and-badger-profile-app.herokuapp.com/

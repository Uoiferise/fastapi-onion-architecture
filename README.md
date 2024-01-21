# FastAPI Onion Architecture example

### Python 3.11
### First thing to do:
- Create a virtual environment using the command: `python -m venv venv`
- Activate virtual environment
    - For Windows, you need to run the following command: `venv\Scripts\activate`
    - For Linux systems, you need to run the following command: `source venv/bin/activate`
- Check pip: `pip list`
- Next you need to install poetry: `pip install poetry`
- Next download all libraries: `poetry install`


### Launching the application
  - Using python: `python -m src`
  - Using uvicorn: `uvicorn --port 8000 --host 127.0.0.1 src.main:app --reload`


### Alembic commands:
  - `alembic init -t async alembic`
  - `alembic revision --autogenerate -m 'initial'`
  - `alembic upgrade head`
  - `alembic downgrade -1`


### Pytest commands:
  - `pytest --maxfail=1 -vv -p no:warnings`
  - `pytest --maxfail=1 -vv -p no:warnings -k 'TestCaseName'`
  - `pytest --maxfail=1 -vv -p no:warnings --ignore=PathName`

### Setting up environment variables:
**.env**
```
MODE=DEV
DB_USER=postgres
DB_PASS=postgres
DB_HOST=localhost
DB_PORT=5433
DB_NAME=dev_db
```
- The parameters must match the file `docker-compose.development.yaml`, if you plan to build the database in Docker.
  - For building container: `docker-compose -f docker-compose.development.yaml up --build`

**.test.env**

```
MODE=TEST
DB_USER=postgres
DB_PASS=postgres
DB_HOST=localhost
DB_PORT=5434
DB_NAME=test_db
```
- The parameters must match the file `docker-compose.test.yaml`, if you plan to build the database in Docker.
-   - For building container: `docker-compose -f docker-compose.test.yaml up --build`

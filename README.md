# FastAPI Onion Architecture example

## Description ✨
This project is intended to demonstrate a possible implementation of the onion architecture using the FastAPI.
The Unit of Work pattern was chosen as a basis,
more details about the advantages of this approach can be read *[here](https://www.cosmicpython.com/book/chapter_06_uow.html)*.
This project also implements an example of isolated tests using Pytest.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-FB3C01?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.108-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.5-3776AB?style=for-the-badge&logo=pydantic&logoColor=white)
![pytest-asyncio](https://img.shields.io/badge/pytest--asyncio-0.21-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

## Table of contents
1) [Quick start](#quick_start)
2) [Project structure](#project_structure)

## <a id="quick_start">Quick start</a> 🚀
- Create a virtual environment using the command: `python -m venv venv`
- Activate virtual environment
    - For Windows, you need to run the following command: `venv\Scripts\activate`
    - For Linux systems, you need to run the following command: `source venv/bin/activate`
- Check pip: `pip list`
- Next you need to install poetry: `pip install poetry`
- Next download all libraries: `poetry install`

### Setting up environment variables:
**.env**
```
MODE=DEV
DB_USER=postgres
DB_PASS=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dev_db
```

**.test.env**

```
MODE=TEST
DB_USER=postgres
DB_PASS=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=test_db
```

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
  - `make test`

### Ruff commands:
  - `ruff check . --config=pyproject.toml`
  - `make lint`

### Make commands:
```bash
make api
```
```bash
make lint
```
```bash
make test
```

## <a id="project_structure">Project structure</a> 📂
Here is an example of a basic project structure for a single microservice.
Also collected are general recommendations for the location of various entities.

The standard structure is as follows:
```
.
├── alembic
|   ├── versions
|   └── ...
|
├── src
|   ├── api
|   |   └── v1
|   |       ├── routers
|   |       |   └── users.py
|   |       └── services
|   |           └── users.py
|   |
|   ├── database
|   |   └── ...
|   |
|   ├── models
|   |   └── users.py
|   |
|   ├── repositories
|   |   └── users.py
|   |
|   ├── schemas
|   |   └── users.py
|   |
|   ├── utils
|   |   └── ...
|   |
|   ├── config.py
|   ├── main.py
|   └── metadata.py
|
├── tests
|   ├── fixtures
|   |   ├── db_mocks
|   |   |   └── ...
|   |   ├── testing_cases
|   |   |   └── ...
|   |   └── ...
|   |
|   ├── unit
|   |   ├── api
|   |   |   └── ...
|   |   └── ...
|   |
|   ├── integration
|   |   └── ...
|   |
|   ├── migration
|   |   └── ...
|   |
|   ├── conftest.py
|   ├── constants.py
|   └── utils.py
|
├── .test.env 
.
```

### Advantages of the Unit of Work (UoW) Pattern
Unit of Work (UoW) is a pattern used to group database operations into a single transactional context. It manages transactions and tracks changes to save them to the database consistently.

Key advantages:
- **Data integrity:**
  - All operations are grouped into a transaction, ensuring either full completion of all changes or a rollback in case of an error.
- **Performance improvement:**
  - UoW minimizes the number of database queries by batching them before execution. This reduces overhead when interacting with the database.
- **Object state management:**
  - Tracking added, modified, and deleted objects within one transaction simplifies data synchronization between the application and the database.
- **Clean code:**
  - Separates transaction management logic from business logic, making the code more readable and modular.
- **Ease of testing:**
  - UoW transactions simplify the creation of isolated tests, as changes can be easily rolled back.
- **Extensibility:**
  - Complex operations can be added without modifying core business logic, since Unit of Work encapsulates transaction management.

### Project Structure Analysis
The provided structure represents a typical project layout using FastAPI or a similar framework. It separates application logic by responsibility, making the system easier to scale and maintain.

Structure sections:
- **alembic:**
  - Contains files for managing database migrations.
  - `versions` — a folder with migration scripts, each representing changes to the DB schema.
- **app:**
  - The main application directory.
  - `api/v1`:
    - Stores API request handlers.
    - `routers/users.py` — routes defining endpoints for interacting with the User entity.
    - `services/users.py` — logic serving the routes. Typically, this is where business logic resides.
  - `database`:
    - Components for connecting to the database (e.g., SQLAlchemy Session, initialization functions).
  - `models`:
    - Definitions of ORM models (e.g., SQLAlchemy).
    - `users.py` — model for the users table.
  - `repositories`:
    - Classes for database access, providing methods for CRUD operations.
    - `users.py` — repository for the User entity.
  - `schemas`:
    - Definitions of Pydantic schemas for data validation.
    - `users.py` — input/output schemas (e.g., `UserCreate`, `UserResponse`).
  - `utils`:
    - Utility functions, e.g., for password hashing, email sending, etc.
  - **Top-level files:**
    - `config.py` — configuration parameters for the application (e.g., database settings, environment variables).
    - `main.py` — the entry point of the application. Usually creates the FastAPI app and includes the routers.
    - `metadata.py` — contains shared metadata for Swagger documentation.

- **tests:**
  - Main directory for all project tests, including fixtures, unit and integration tests, and helpers.
  - `fixtures`:
    - Stores fixtures and data required for running tests.
    - `db_mocks` — contains fixtures and mock data for testing database interactions.
    - `testing_cases` — contains prepared data and scenarios used in tests to simulate different situations.
  - `unit`:
    - Directory for unit tests. These tests cover individual modules of the application.
    - The internal structure mirrors the main project structure for easier test navigation.
  - `integration`:
    - Contains integration tests that verify interactions between different parts of the system, such as between API and the database.
  - `migration`:
    - Contains tests for validating the correctness of database migrations, ensuring schema changes can be applied and rolled back properly.
  - `conftest.py` — defines common fixtures available for all tests in the project. For example, test DB connection, test users, or environment setup.
  - `constants.py` — contains constants used in tests, such as test data, error codes, or URLs.
  - `utils.py` — helper functions and classes that simplify test writing, such as data generators or test runners.
- **.test.env:**
  - File storing environment variables used for running tests.

### How Do the Components Interact?
1) **Request:** A user sends an HTTP request, which is received by the router (`api/v1/routers/users.py`).
2) **Route handling:** The router forwards the request to the service layer (`api/v1/services/users.py`), where business logic is executed.
3) **Database operations:** The service calls the repository (`repositories/users.py`) to perform database operations via the ORM model (`models/users.py`).
4) **Response:** The result is transformed into a Pydantic schema (`schemas/users.py`) and returned as JSON.
5) **Supporting components:** Utilities (`utils`) or configuration files (`config`, etc.) are used across all levels.

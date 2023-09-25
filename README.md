# MicroTwitter

## Project goal
* ***Implement the backend of a microblogging service***

<div style="text-align: center;">
  <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white" alt="Postgres">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Twitter-%231DA1F2.svg?style=for-the-badge&logo=Twitter&logoColor=white" alt="Twitter">
  <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Docker_Compose-2496ED.svg?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Compose">
  <img src="https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx">
  <img src="https://img.shields.io/badge/Pydantic-2.3.0-3399CC.svg?style=for-the-badge" alt="Pydantic">
  <img src="https://img.shields.io/badge/Uvicorn-0.23.2-4CBB17.svg?style=for-the-badge" alt="Uvicorn">
  <img src="https://img.shields.io/badge/Loguru-0.7.2-00AEEF.svg?style=for-the-badge" alt="Loguru">
  <img src="https://img.shields.io/badge/Pytest-7.4.2-0A9EDC.svg?style=for-the-badge" alt="Pytest">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0.21-336791?style=for-the-badge" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/Alembic-1.12.0-F9A03C.svg?style=for-the-badge&logo=alembic&logoColor=white" alt="Alembic">
</div>




## **Docker-Compose**
  1. You need to rename the file .env.template to .env and, if necessary, modify the variables.
  2. In the root folder, run the ***command***: ```docker-compose up ``` or ```docker-compose up -d```
  3.  You can find all the test users in the file```alembic/versions/65272ae975a2_add_test_user.py```

***Here they are anyway:***
```python
    {"username": "testuser1", "api_key": "test"},
    {"username": "testuser2", "api_key": "test2"},
    {"username": "testuser3", "api_key": "test3"}
```

***The backend is designed so that you can only see the tweets of the user you are following***

## **Manual Configuration**

### Step 1: Prerequisites

Before you begin, make sure you have the following prerequisites installed on your system:

- **Python 3.11.5**
- **PostgreSQL 15.4**

### Step 2: Cloning the Repository

- Clone the project repository to your computer
- ``git clone https://github.com/r00tk3y/fastapi-Twitter``
- Enter the repository:  ``cd fastapi-Twitter``

### Step 3: Creating and Activating a Virtual Environment

To isolate project dependencies and avoid conflicts with system libraries, it's recommended to create and activate a virtual environment. Follow these steps:

1. Create a virtual environment in the project's root folder:

   ```bash
   python -m venv venv
2. Activate the virtual environment based on your operating system:
    * ***Windows***
   ```bash
    venv\Scripts\activate.bat
   ```
   * ***Linux***
    ```bash
    source venv/bin/activate
    ```

### Step 4: Installing Dependencies

After activating the virtual environment, install the project dependencies using the package manager for your application stack:
- For python use `pip`:
  * ***Dependencies for the production environment:***
   ```bash
   pip install -r requirements.txt
    ```
  * ***Dependencies for the development environmen***
  ```bash
  pip install -r requirements.dev.txt
  ```
  These dependencies may include code analysis tools (linters) and additional libraries for testing.




### Step 5: Alembic migrations

 In the folder `src` Enter the command in the terminal:

   ```bash
   alembic upgrade head
   ```

### Step 6: Renaming and Adjusting the Configuration template
Rename the configuration template file from .env.template to .env in the project's root directory:
```bash
mv .env.template .env
```
2.  ``POSTGRES_HOST=localhost`` adjust this value, otherwise you will get gaia socket errors


### Step 7: Starting the Server with Uvicorn

To run your server using Uvicorn, follow these steps::

1. Ensure that you have activated the virtual environment as indicated in "Step 3."

2. Start your application using Uvicorn in the root directory:
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload 
    ```


### Step 8: Running Tests Using Pytest

1. Navigate to the `src/tests` folder

2. Run tests via

   ```bash
   pytest
   ```
   **or for detailed output**
   ```bash
   pytest -s

## Inserting Data and Establishing Relationships in the Database

***You can modify this in the alembic/versions/_add_test_user.py folder***
In this step, we will add initial data to the database and establish relationships between users.

### Inserting Data into the Users Table


To begin with, we will insert data into the users' table. In the example below, we use the `op.bulk_insert` operation to insert multiple users into the `users_table`. Each user has a username `(username)` and an API key `(api_key)`. These values will already be added to the database if you completed Step 5.

```python
op.bulk_insert(
    users_table,
    [
        {"username": "testuser1", "api_key": "test"},
        {"username": "testuser2", "api_key": "test2"},
        {"username": "testuser3", "api_key": "test3"},
    ],
)
```
### Establishing Relationships Between Users (Followers and Following

Often in applications, there are relationships between users, such as "followers" and "following." For this purpose, we create a separate table called user_to_user that will store information about who is following whom.
```python
users_to_users_table = sa.table(
    "user_to_user",
    sa.column("follower_id", sa.Integer),
    sa.column("following_id", sa.Integer),
)

```
Then, we use `op.bulk_insert` to add subscription records. In the example below, user with `follower_id` `1` is following user with `following_id` `3`, and vice versa.
```python
op.bulk_insert(
    users_to_users_table,
    [
        {"follower_id": 1, "following_id": 3},
        {"follower_id": 3, "following_id": 1},
    ],
)
```

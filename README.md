# FastAPI PostgreSQL And MongoDb


## Features

- Set up FastAPI with PostgreSQL and MongoDB integration.
- Define SQLAlchemy models for the PostgreSQL database.
- pydantic validation 
- Use `python-dotenv` for managing environment variables.

## Getting Started

### Prerequisites

- Python 
- PostgreSQL database server
- MongoDB database server

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/muhammedaslam312/fast-api-test-mongodb.git
   cd fast-api-test-mongodb

2. Create a Virtual Environment:

   ```bash
   python -m venv venv
   #for windows
   venv\Scripts\activate

3. Install Dependencies:

   ```bash
   pip install -r requirements.txt

4. Set up your PostgreSQL and MongoDB databases and create a .env file in the project root directory with the following content:

   ```bash
   #add this in .env 
   #set up postgres
   DATABASE_URL=postgresql://yourusername:yourpassword@localhost/database_name

   #Mongo_db setup
   #create a database name is - profiles
   #create a collection name is - profile



5. Run the FastAPI application:

    ```bash
   uvicorn main:app --reload

6. Access the API documentation at http://localhost:8000/docs in your browser. You can use the interactive documentation to test the API endpoints.

    ```bash
    #routes of projects
   /register1/ - create user by using Postgres and Mongodb
   /register2/ - create user by using Postgres(with two table)
   /user/{id}/ - get user details of both created user by using id





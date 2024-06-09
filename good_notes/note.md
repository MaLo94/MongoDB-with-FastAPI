# Best Practices for Connecting MongoDB using Motor in FastAPI
## Introduction
Hello. I have a question: What are the best practices for connecting to a database in FastAPI?

To provide some context, I want to write code to connect to a MongoDB database using Motor. My idea is to create a single connection and use it in all the controllers that need it through Dependency Injection, but I am not quite sure how to do it. So let me show you a simple code example to illustrate this idea in a nutshell:

## Code Example
`database.py`
```python
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import dotenv_values

class Database:
    _client: AsyncIOMotorClient | None = None
    _db: AsyncIOMotorDatabase | None = None

    @staticmethod
    def connect() -> None:
        config = dotenv_values(".env")
        Database._client = AsyncIOMotorClient(config["ATLAS_URI"])
        Database._db = Database._client[config["DB_NAME"]]

    @staticmethod
    def close() -> None:
        if Database._client is not None:
            Database._client.close()
        else:
            raise ConnectionError("Client not connected")

    @staticmethod
    def get_db() -> AsyncIOMotorDatabase:
        if Database._db is not None:
            return Database._db
        else:
            raise ConnectionError("Database not connected")
```

`main.py`
```python
from fastapi import FastAPI, Depends
import uvicorn
from database import Database
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorDatabase

@asynccontextmanager
async def lifespan(app: FastAPI):
    Database.connect()
    yield
    Database.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def main(db: AsyncIOMotorDatabase = Depends(Database.get_db)):
    await db["books"].insert_one({"hello": "world"})
    return "Done"

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
```
As you can see, I have a `Database` class that is designed to manage the database connection. In `main.py`, within the lifespan function, we start the connection to the MongoDB database before the app starts running and close it when the app stops. Finally, as an example, we have a small endpoint that obtains the database instance through Dependency Injection and creates a simple document in a collection called 'books'.

## Future Improvements
The idea is to divide the code in the future into Models, Controllers, and Services to create better code. However, this isn't the focus of the current question, so I've chosen not to provide an example code.

## Feedback and Suggestions
I would like to know what you think about my solution. Are there any ways to improve it? Am I following the best practices? Can you identify any potential issues? Any suggestions are welcome. If you have another approach, feel free to share it.

Thank you so much for reading
check : [source](https://www.reddit.com/r/learnpython/comments/1cxl7pj/best_practices_for_connecting_mongodb_using_motor/)
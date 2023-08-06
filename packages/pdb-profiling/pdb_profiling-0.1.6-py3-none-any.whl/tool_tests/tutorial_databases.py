# @Created Date: 2020-05-26 09:29:07 pm
# @Filename: tutorial_databases.py
# @Email:  1730416009@stu.suda.edu.cn
# @Author: ZeFeng Zhu
# @Last Modified: 2020-05-26 09:29:27 pm
# @Copyright (c) 2020 MinghuiGroup, Soochow University
import asyncio
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateTable
from databases import Database
from time import perf_counter

'''
Reference
---------

* <https://www.encode.io/databases>
'''

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String(length=100)),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)


async def main():
    database = Database('sqlite:///./db/encode_db_test.db')

    # Establish the connection pool
    await database.connect()
    # Create a table.
    # engine = sqlalchemy.create_engine(str(database.url))
    # metadata.create_all(engine)
    query = """CREATE TABLE notes (id INTEGER PRIMARY KEY, text VARCHAR(100), completed BOOLEAN)"""
    await database.execute(query=query)

    # Execute
    query = notes.insert()
    values = {"text": "example1", "completed": True}
    await database.execute(query=query, values=values)
    '''
    # Execute
    query = "INSERT INTO notes(text, completed) VALUES (:text, :completed)"
    values = {"text": "example1", "completed": True}
    await database.execute(query=query, values=values)
    '''

    # Execute many
    query = notes.insert()
    values = [
        {"text": "example2", "completed": False},
        {"text": "example3", "completed": True},
    ]*100
    start = perf_counter()
    await database.execute_many(query=query, values=values)
    print(perf_counter()-start)

    '''
    # Execute many
    query = "INSERT INTO notes(text, completed) VALUES (:text, :completed)"
    values = [
        {"text": "example2", "completed": False},
        {"text": "example3", "completed": True},
    ]
    await database.execute_many(query=query, values=values)
    '''

    # Fetch multiple rows
    query = notes.select()
    rows = await database.fetch_all(query=query)
    print(rows, type(rows))
    '''
    # Fetch multiple rows
    query = "SELECT * FROM notes WHERE completed = :completed"
    rows = await database.fetch_all(query=query, values={"completed": True})

    # Run a database query.
    query = "SELECT * FROM HighScores"
    rows = await database.fetch_all(query=query)
    print('High Scores:', rows)
    '''

    # Fetch single row
    query = notes.select()
    row = await database.fetch_one(query=query)
    print(row, type(row))
    '''
    # Fetch single row
    query = "SELECT * FROM notes WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": 1})
    '''

    # Fetch single value, defaults to `column=0`.
    query = notes.select()
    value = await database.fetch_val(query=query)
    print(value, type(value))

    # Fetch multiple rows without loading them all into memory at once
    query = notes.select()
    async for row in database.iterate(query=query):
        print('iter', row, type(row))

    # Close all connection in the connection pool
    await database.disconnect()
    

asyncio.get_event_loop().run_until_complete(main())

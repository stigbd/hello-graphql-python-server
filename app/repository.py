"""The repository module."""

import csv
import sqlite3
from pathlib import Path


def create_tables_and_load(filename: str) -> None:
    """Create tables and load database from csv file."""
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    # Create tables and load data from csv file:
    cursor.execute("CREATE TABLE IF NOT EXISTS authors (id INTEGER PRIMARY KEY, name TEXT, birth_year INTEGER)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS books "
        "(id INTEGER PRIMARY KEY, author TEXT, title TEXT, year INTEGER, publisher TEXT)"
    )
    # Delete all rows in the tables and load data from csv file:
    cursor.execute("DELETE FROM authors")
    with Path("data/authors.csv").open() as file:
        reader = csv.reader(file, delimiter=",")
        # Skip the header row
        next(reader)
        for row in reader:
            cursor.execute("INSERT INTO authors (name, birth_year) VALUES (?,?)", (row[0], row[1]))
    cursor.execute("DELETE FROM books")
    with Path("data/books.csv").open() as file:
        reader = csv.reader(file, delimiter=",")
        # Skip the header row
        next(reader)
        for row in reader:
            cursor.execute(
                "INSERT INTO books (author, title, year, publisher) VALUES (?,?,?,?)",
                (
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                ),
            )
    connection.commit()

"""GraphQL schema for the books and authors database."""

import sqlite3

import strawberry


@strawberry.type(description="The book type.")
class Book:
    """The book type."""

    title: str
    author: str
    year: int
    publisher: str = "Scribner"


def get_books_by_author(author: str) -> list[Book]:
    """Get all books by author."""
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM books WHERE author = ?;", (author,))
    books = res.fetchall()

    return [Book(title=book[2], author=book[1], year=book[3], publisher=book[4]) for book in books]


@strawberry.type
class Author:
    """The author type."""

    name: str
    birth_year: int
    books: list[Book]


def get_authors() -> list[Author]:
    """Get all authors."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    res = cursor.execute("SELECT * FROM authors")
    authors = res.fetchall()
    return [Author(name=author[1], birth_year=author[2], books=get_books_by_author(author[1])) for author in authors]


def get_books() -> list[Book]:
    """Get all books."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    res = cursor.execute("SELECT * FROM books")
    books = res.fetchall()

    return [Book(title=book[2], author=book[1], year=book[3], publisher=book[4]) for book in books]


@strawberry.type
class Query:
    """The query type."""

    books: list[Book] = strawberry.field(resolver=get_books)
    authors: list[Author] = strawberry.field(resolver=get_authors)


schema = strawberry.Schema(query=Query)

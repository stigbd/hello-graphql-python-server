"""The main API module."""

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from .graphql import schema
from .repository import create_tables_and_load

graphql_app = GraphQLRouter(schema=schema)

app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    """Create tables and load data from csv files."""
    create_tables_and_load("data/database.db")


app.include_router(graphql_app, prefix="/graphql")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from typing import List

Connection = sqlite3.Connection


def initialize(connection: str) -> sqlite3.Connection:
    """
    Connect to database and create table if is not exists
    """
    conn = sqlite3.connect(connection)

    create_table(conn)
    return conn


def create_table(conn: sqlite3.Connection):
    """
    Create table in DB with column for timestamp and column for name
    """
    with conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS documents (timestamp int, name text)")


def finalize(conn: sqlite3.Connection):
    """
    Close connection to DB
    """
    conn.close()


def nonexists(conn: sqlite3.Connection, candidates: List[str]) -> List[str]:
    """
    Find candidates from candidates list which is not exists yet in DB.
    """
    statement = "SELECT name FROM documents WHERE name IN ({})".format(
        ", ".join(['?'] * len(candidates)))
    with conn:
        exists_candidates = conn.execute(statement, candidates).fetchall()
    return list(set(candidates).difference(set(map(lambda x: x[0],
                                                   exists_candidates))))

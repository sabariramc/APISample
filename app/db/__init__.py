#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 02-Aug-2020
"""

from flask import current_app, g
import sqlite3


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def execute_query(query, params):
    db = get_db()
    cur = db.cursor()
    cur.execute(query, params)
    result_itr = cur.fetchall()
    if cur.description:
        header_list = [x[0] for x in cur.description]
        result_list = []
        for result in result_itr:
            temp = {}
            for column_name, column_value in zip(header_list, result):
                temp[column_name] = column_value
            result_list.append(temp)
        return result_list


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('db/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()

"""Useful commands.

Classes:
QueueItem
WorkItem

Functions:
clear_queue - Clear the queue.
clear_work - Clear the table of work.
task_items - Info about items in the queue.
work_items - Info about items in the table of work.
"""

from collections import namedtuple
import pickle
import sqlite3
import traceback

from .config import DB_PATH, QUEUE_TABLENAME, SCHEMA, WORK_TABLENAME
from .utils import echo


QueueItem = namedtuple('QueueItem', SCHEMA[QUEUE_TABLENAME].keys())
WorkItem = namedtuple('WorkItem', SCHEMA[WORK_TABLENAME].keys())


def clear_queue():
    """Clear the task queue."""
    con = sqlite3.connect(str(DB_PATH))
    with con:
        con.execute(
            f"""
            DELETE FROM {QUEUE_TABLENAME}
            """
        )
    con.close()
    echo("Cleared the queue.")


def clear_work():
    """Clear the table of work."""
    con = sqlite3.connect(str(DB_PATH))
    with con:
        con.execute(
            f"""
            DELETE FROM {WORK_TABLENAME}
            """
        )
    con.close()
    echo("Cleared table of work.")


def task_items(max_entries=None):
    """Information about the items in the task queue. Returns a
    generator of QueueItems.

    Keyword arguments:
    max_entries - (int) (Default: None) Maximum number of items to
        return. Default is to return all entries.
    """
    con = sqlite3.connect(str(DB_PATH))
    with con:
        c = con.execute(
            f"""
            SELECT task_id, queue_name, position, published, args, kwargs
            FROM {QUEUE_TABLENAME}
            ORDER BY position DESC
            """
        )
    if max_entries:
        items = map(QueueItem._make, c.fetchmany(size=max_entries))
    else:
        items = map(QueueItem._make, c.fetchall())
    con.close()
    return items


def work_items(max_entries=None):
    """Information about the items in the work queue. Returns a
    generator of WorkItems.

    Keyword arguments:
    max_entries - (int) (Default: None) Maximum number of items to
        return. Default is to return all entries.
    """
    con = sqlite3.connect(str(DB_PATH))
    with con:
        c = con.execute(
            f"""
            SELECT
                task_id, queue_name, started, status,
                exc_type, exc_value, exc_traceback
            FROM {WORK_TABLENAME}
            ORDER BY started ASC
            """
        )
    if max_entries:
        entries = c.fetchmany(size=max_entries)
    else:
        entries = c.fetchall()
    con.close()
    for row in entries:
        exc_type, exc_value = tuple(pickle.loads(bin_) for bin_ in row[-3:-1])
        exc_tb = ''.join(pickle.loads(row[-1]).format())
        yield WorkItem(*row[:-3], exc_type, exc_value, exc_tb)

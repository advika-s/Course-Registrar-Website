#!/usr/bin/env python

#-----------------------------------------------------------------------
# regdb.py
# Author: Alice Lee, Advika Srivastava
#-----------------------------------------------------------------------

import sys
import contextlib
import sqlite3

#-----------------------------------------------------------------------

DATABASE_URL = 'file:reg.sqlite?mode=ro'

def _replace_wild(query):
    '''Takes string query as input. Replaces characters that are by
    default treated as wildcard characters in SQL by preceding them with
    black slash characters. Returns editted string query.
    '''
    i = 0
    while i < len(query):
        if query[i] == '%':
            query = query[:i] + '\\' + query[i:]
            i += 2
        elif query[i] == '_':
            query = query[:i] + '\\' + query[i:]
            i += 2
        i += 1
    return query

def database(dept, number, area, title):
    '''Takes strings dept, number, area, title as input. Executes SQL
    statements. Throws database related exceptions, if any. Returns
    list rows and exit status 0 if successful.
    '''
    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None,
            uri=True) as connection:

            with contextlib.closing(connection.cursor()) as cursor:
                # create query string to get necessary info
                stmt_str = "SELECT classid, classes.courseid, "
                stmt_str += "crosslistings.courseid, courses.courseid, "
                stmt_str += "crosslistings.dept, "
                stmt_str += "crosslistings.coursenum, "
                stmt_str += "courses.area, courses.title "
                stmt_str += "FROM classes, crosslistings, courses "
                stmt_str += "WHERE classes.courseid = courses.courseid "
                stmt_str += "AND crosslistings.courseid "
                stmt_str += "= courses.courseid "

                # store variables to be used in cursor.execute
                bindings = []
                if dept is not None:
                    stmt_str += "AND lower(crosslistings.dept) LIKE ? "
                    dept = _replace_wild(dept)
                    bindings.append('%'+dept+'%')
                if number is not None:
                    stmt_str += "AND lower(crosslistings.coursenum) "
                    stmt_str += "LIKE ? "
                    number = _replace_wild(number)
                    bindings.append('%'+number+'%')
                if area is not None:
                    stmt_str += "AND lower(courses.area) LIKE ? "
                    area = _replace_wild(area)
                    bindings.append('%'+area+'%')
                if title is not None:
                    stmt_str += "AND lower(courses.title) LIKE ? "
                    title = _replace_wild(title)
                    bindings.append('%'+title+'%')
                if len(bindings) != 0:
                    stmt_str += "ESCAPE '\\' "

                stmt_str += "ORDER BY crosslistings.dept, "
                stmt_str += "crosslistings.coursenum, "
                stmt_str += "classes.classid ASC; "
                cursor.execute(stmt_str, bindings)

                rows = []
                row = cursor.fetchone()

                while row is not None:
                    rows.append(row)
                    row = cursor.fetchone()
                return [False, rows]

    # handle database related errors
    except Exception as ex:
        print(sys.argv[0] + ': ' + str(ex), file=sys.stderr)
        # boolean: is it a database error?
        return [True, 'A server error occurred. Please contact '
            + 'the system administrator.']

    sys.exit(0)

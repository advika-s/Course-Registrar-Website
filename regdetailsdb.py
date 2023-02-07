#-----------------------------------------------------------------------
# regdetailsdb.py
# Author: Alice Lee, Advika Srivastava
#-----------------------------------------------------------------------

import sys
import contextlib
import sqlite3

#-----------------------------------------------------------------------

DATABASE_URL = 'file:reg.sqlite?mode=ro'

def database(classid):
    '''Takes int classid as input. Executes SQL statements. Throws
    database related exceptions, if any. Returns exit status 0 if
    successful.
    '''
    try:
        with sqlite3.connect(DATABASE_URL, isolation_level=None,
            uri=True) as connection:

            with contextlib.closing(connection.cursor()) as cursor:
                stmt_str = "SELECT * "
                stmt_str += "FROM classes, courses, crosslistings "
                stmt_str += "WHERE classes.classid = ? "
                stmt_str += "AND classes.courseid = "
                stmt_str += "crosslistings.courseid "
                stmt_str += "AND crosslistings.courseid = "
                stmt_str += "courses.courseid "
                stmt_str += "ORDER BY crosslistings.dept, "
                stmt_str += "crosslistings.coursenum"
                cursor.execute(stmt_str, [classid])
                row1 = cursor.fetchone()

                # if there is no class with classid
                if row1 is None:
                    # first boolean: is it a database error?
                    # second boolean: is it a classid error?
                    return [False, True,
                    'no class with classid ' + str(classid)
                    + ' exists']

                temp1 = row1
                crsdict = {}
                dept = []
                num = []

                # get all cross listings, without duplicates
                # temp1[13] = crosslistings.dept
                # temp1[14] = crosslistings.coursenum
                # dictionary keys = dept + coursenum, value = 1
                while temp1 is not None:
                    # if it is the first time encountering dept and num,
                    # add to lists and dict
                    if temp1[13] + temp1[14] not in crsdict:
                        dept.append(temp1[13])
                        num.append(temp1[14])
                        crsdict[temp1[13] + temp1[14]] = 1
                    temp1 = cursor.fetchone()

                stmt_str = "SELECT * "
                stmt_str += "FROM coursesprofs, profs "
                stmt_str += "WHERE coursesprofs.courseid = ? "
                stmt_str += "AND coursesprofs.profid = profs.profid"

                # row1[7] = courses.courseid
                cursor.execute(stmt_str, [row1[7]])
                row2 = cursor.fetchone()

                temp2 = row2
                prof = []
                profdict = {}

                # get all professor names, without duplicates
                # temp2[3] = profs.profname
                # dictionary keys = profname, vlaue = 1
                while temp2 is not None:
                    if temp2[3] not in profdict:
                        prof.append(temp2[3])
                        profdict[temp2[3]] = 1
                    temp2 = cursor.fetchone()
                prof.sort()

                return row1, dept, num, prof, classid

    # handle database related errors
    except Exception as ex:
        print(sys.argv[0] + ': ' + str(ex), file=sys.stderr)
        # first boolean: is it a database error?
        # second boolean: is it a classid error?
        return [True, False, 'A server error occurred. Please contact '
            + 'the system administrator.']

    sys.exit(0)

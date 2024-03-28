import mysql.connector

import connect

connection = None
dbconn = None


def DBConnect():
    global dbconn
    global connection
    if dbconn == None:
        connection = mysql.connector.connect(user=connect.dbuser, password=connect.dbpass, host=connect.dbhost,
                                             database=connect.dbname, autocommit=True)
        dbconn = connection.cursor()
        return dbconn
    else:
        if connection.is_connected():
            return dbconn
        else:
            connection = None
            dbconn = None
            return DBConnect()


def DBOperator(sqlCommands):
    cur = DBConnect()
    cur.execute(sqlCommands)
    if (cur.with_rows == False):
        return []
    select_result = cur.fetchall()
    column_names = [i[0] for i in cur.description]
    dbconn.close()
    connection.close()
    return [dict(zip(column_names, row)) for row in select_result]


#  return select_result
def DBOperatorInsertedId(sqlCommands):
    print(sqlCommands)
    cur = DBConnect()
    cur.execute(sqlCommands)
    select_result = cur.lastrowid
    print("lastrowId: %s" % select_result)
    dbconn.close()
    connection.close()
    return select_result


def DBOperatorFetchOne(sqlCommands):
    print(sqlCommands)
    cur = DBConnect()
    cur.execute(sqlCommands)
    select_result = cur.fetchone()
    dbconn.close()
    connection.close()
    return select_result


def DBOperator_search(sqlCommands, searchtext_tuple):
    cur = DBConnect()
    rows_affected = cur.execute(sqlCommands, searchtext_tuple)
    if (cur.with_rows == False):
        return []
    select_result = cur.fetchall()
    dbconn.close()
    connection.close()
    return select_result


def DBOperator_update(sqlCommands):
    print(sqlCommands)
    cur = DBConnect()
    cur.execute(sqlCommands)
    rows_affected = cur.rowcount
    dbconn.close()
    connection.close()
    return rows_affected

#!/usr/bin/env python

import mysql.connector
import sys

import configurator


_connection = {}  # Dictionary of Database connections
_error      = {}  # Dictionary of Database last errors


def connect(dbname):
    """ Find the configuration of a given Database and connect in it. """
    config = configurator.load_config("config/database.conf", {})
    if not "monitor" in config:
        return False
    dbconfig = config["monitor"]


    try:
        _connection[dbname] = mysql.connector.connect(**dbconfig)
        _error[dbname] = ""
        return True
    except mysql.connector.Error as error:
        _connection[dbname] = None
        _error[dbname] = error

    return False


def query(dbname, query, values = ()):
    """ Execute a Query on a Database and return its Cursor. """
    if not dbname in _connection.keys() or _connection[dbname] == None:
        return []

    _error[dbname] = None
    try:
        cursor = _connection[dbname].cursor()
        cursor.execute(query, values)
        return cursor
    except mysql.connector.Error as error:
        _error[dbname] = error

    return []
        
def commit(dbname):
    if not dbname in _connection.keys() or _connection[dbname] == None:
        return []

    _connection[dbname].commit()



def get_error(dbname):
    """ Return the last error of a given Database. """
    if dbname in _error.keys():
        return _error[dbname]
    
    return False


def close(connection):
    """ Close the Database Connection or the Database Cursor. """
    if isinstance(connection, basestring) and connection in _connection.keys():
        connection = _connection[connection]

    try:
        connection.close()
    except:
        None


def main(argv):
    """
    The function to be executed on a standalone call of the program.
    Used to test the function of the script.
    """
    if not connect("monitor"):
        print "{}".format(get_error("monitor"))


    result = query("monitor", "SELECT 1, 2, 3 FROM DUAL;")
    if not get_error("monitor"):
        for row in result:
            print row
    else:
        print "error", get_error("monitor")
    close(result)


    result = query("monitor", "CREATE TABLE tb_dummy_droppable (id bigint auto_increment, string varchar(255), number int, primary key (id));")
    if not get_error("monitor"):
        commit("monitor")
        print result
    else:
        print get_error("monitor")
    close(result)


    result = query("monitor", "INSERT INTO tb_dummy_droppable VALUES (NULL, 'string1', 1),(NULL, 'string2', 2)")
    if not get_error("monitor"):
        print result
        commit("monitor")
    else:
        print get_error("monitor")
    close(result)


    result = query("monitor", "SELECT * FROM tb_dummy_droppable;")
    if not get_error("monitor"):
        print result
        for row in result:
            print row
    else:
        print get_error("monitor")
    close(result)


    result = query("monitor", "SELECT * FROM tb_dummy_droppable WHERE string = %s and number = %s", ("string2", 2))
    if not get_error("monitor"):
        print result
        for row in result:
            print row
    else:
        print get_error("monitor")
    close(result)


    result = query("monitor", "DROP TABLE tb_dummy_droppable;")
    if not get_error("monitor"):
        print result
    else:
        print get_error("monitor")
    close(result)


    close("monitor")


if __name__ == "__main__":
    main(sys.argv[1:])

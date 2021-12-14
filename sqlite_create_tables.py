import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file
    :parm db_file: database file
    :return: Connection object or None
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement 
    :parm conn: Connection object
    :parm create_table_sql: CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r'companies.db'

    sql_create_candidates_table = """ CREATE TABLE IF NOT EXISTS candidates (
                                            ticker text NOT NULL PRIMARY KEY,
                                            name text NOT NULL,
                                            sector text,
                                            industry text,
                                            fcf_yield float,
                                            momentum float
                                            ); """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_candidates_table)
    else:
        print('Error cannot create the database connection.')


if __name__ == '__main__':
    main()

from getpass import getpass
from logging import ERROR
from mysql.connector import connect, Error

# try:
#     with connect(
#         host="localhost",
#         user=input("Enter username: "),
#         password=getpass("Enter password: "),
#     ) as connection:
#         show_db_query = "SHOW DATABASES"
#         with connection.cursor() as cursor:
#             cursor.execute(show_db_query)
#             for db in cursor:
#                 print(db)
# except Error as e:
#     print(e)
# try:
#     with connect(
#         host="localhost",
#         user=input("Enter username: "),
#         password=getpass("Enter password: "),
#     ) as connection:
#         create_candidates_table_query = """
#         CREATE TABLE inv_cand(
#             ticker VARCHAR(4) PRIMARY KEY
#             sector VARCHAR(20)
#             industry VARCHAR(20)
#             fcf_yield DECIMAL(5,4)
#             momentum_12mo DECIMAL(5,4)
#         )
#         """
#         with connection.cursor() as cursor:
#             cursor.execute(create_candidates_table_query)
#             connection.commit()
# except:
#     pass

try:
    with connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
    ) as connection:
        show_table_query = "DESCRIBE inv_cand"
        with connection.cursor as cursor:
            cursor.execute(show_table_query)
            result = cursor.fetchall()
            for row in result:
                print(row)
except Error as e:
    print(e)

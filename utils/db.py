import pymysql

def get_db_connection():

    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="smart_library1",
        cursorclass=pymysql.cursors.DictCursor
    )

    return connection
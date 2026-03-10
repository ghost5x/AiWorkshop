import pymysql
def get_conn():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Pass123!",
        database="test_ninja",
        cursorclass= pymysql.cursors.DictCursor
    )



import pymysql
def get_conn():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Pass123!",
        database="AI_WORKSHOP",
        cursorclass= pymysql.cursors.DictCursor
    )



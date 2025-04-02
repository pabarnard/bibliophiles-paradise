import os, pymysql.cursors

DB_PORT = 3306

def connect_to_db(db_name, query : str, data : dict=None):
    db_connection = pymysql.connect(
        host="localhost", # 127.0.0.1
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=db_name,
        port=DB_PORT,
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )
    result = None
    with db_connection.cursor() as cursor: # Context managing for our database connection
        try:
            result = cursor.execute(query,data)
            if query.lower().find("select") >= 0: # Grab data only with SELECT queries
                result = cursor.fetchall()
            elif query.lower().find("insert") >= 0 or query.lower().find("update") >= 0 or query.lower().find("delete") >= 0:
                db_connection.commit() # Save changes to database
            else:
                raise ValueError("Invalid query")
        except Exception as e:
            # This will eventually be logged
            print("An issue arose: ",e)
        finally:
            cursor.close() # Close connection at last no matter what
    return result


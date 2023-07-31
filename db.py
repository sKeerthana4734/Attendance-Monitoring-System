import mysql
import mysql.connector
import mysql.connector as mysql

HOST = "127.0.0.1"  # or "domain.com"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "ams"
# this is the user you create
USER = "root"
# user password
PASSWORD = "4321"


def signin(username, password):
    try:
        db_connection = mysql.connect(
            host=HOST, database=DATABASE, user=USER, password=PASSWORD, connection_timeout=60000)
        print("Connected to:", db_connection.get_server_info())
        mycursor = db_connection.cursor()
        sql = "select password from users where username = "+"'"+username+"';"
        mycursor.execute(sql)
        # db_connection.commit()
        res = mycursor.fetchone()
        print(res[0])
        if res[0] == password:
            return 1
        else:
            return 0

    except mysql.Error as err:
        # toaster.show_toast("Error", "Please Enter the accurate details")
        print(err)
        print("Error Code:", err.errno)
        print("SQLSTATE", err.sqlstate)
        print("Message", err.msg)


signin('Barath', 'barath23')

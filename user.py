from reminder import *
import prettytable

def printAllUsers(db):
    db.execute("SELECT * FROM User")
    rows = db.fetchall()
    table = ""
    if len(rows) > 0:
        table = prettytable.PrettyTable(["username", "name", "password"])
        for row in rows:
            table.add_row(row)

    print(table)
    return

def getUserName(db, username):
    db.execute("SELECT name FROM User WHERE username=?", (username,))
    return db.fetchone()[0]

def loginUser(db, user):
    db.execute("SELECT * FROM User WHERE username=? AND password=?", user)
    rows = db.fetchall()
    if len(rows) > 0:
        return True
    else:
        return False

def registerUser(db, user):
    sql = ''' INSERT INTO User(username,name,password) VALUES(?,?,?) '''
    db.execute(sql, user)
    return

def login(db):
    authenticated = False
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Read username and password from database
    # Try to authenticate, if successful set authenticated to True
    user = (username, password)
    logged_in = loginUser(db, user)

    if logged_in:
        authenticated = True
        print("You successfully logged in!")
        name = getUserName(db, username)
        print("Thanks for logging in, " + name + "!")
        getTodaysReminders(db, username)
    else:
        print("Login failed!")
    return authenticated, username

def register(db, conn):
    authenticated = False
    username = input("Enter username: ")
    name = input("Enter name: ")
    password = input("Enter password: ")
    new_user = (username, name, password)
    registerUser(db, new_user)
    conn.commit()
    if db.lastrowid < 1:
        print("Registration failed!")
    else:
        authenticated = True
        print("You've successfully registered!")
    return authenticated, username
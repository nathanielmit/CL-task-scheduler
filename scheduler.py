#!/usr/bin/env python
import datetime
import sys, os
import time
import sqlite3
import uuid
import prettytable


def getAllTask(db, task):
    db.execute("SELECT * FROM Event WHERE username=?", (task,))
    rows = db.fetchall()
    if len(rows) > 0:
        return rows
    else:
        return 0


def deleteTask(conn, event_id):
    sql = 'DELETE FROM Event WHERE eventID=?'
    cur = conn.cursor()
    cur.execute(sql, (event_id,))
    conn.commit()
    return True


def createTask(conn, task):
    sql = ''' INSERT OR IGNORE INTO Event(eventID, username, title, location, time, date, bold, description)
              VALUES(?,?,?,?,?,?,?,?) '''
    curr = conn.cursor()
    curr.execute(sql, task)
    conn.commit()
    return True


def loginUer(db, user):
    db.execute("SELECT * FROM Users WHERE username=? AND passwordHash=?", user)
    rows = db.fetchall()

    if len(rows) > 0:
        return True
    else:
        return False


def registerUser(conn, user):
    sql = ''' INSERT OR IGNORE INTO Users(username,name,email,passwordHash)
              VALUES(?,?,?,?) '''
    curr = conn.cursor()
    curr.execute(sql, user)
    conn.commit()
    return True


def convertTimeToPythonFormat(userTime):
    # takes user's mm/dd/yyyy hh:mm and turns it into a python time format
    return


def convertTimeToUserFormat(pythonTime):
    return


def createTables(db):
    db.execute('''CREATE TABLE IF NOT EXISTS Users (
        username text PRIMARY KEY,
        name text NOT NULL,
        password text NOT NULL
        );''')

    db.execute('''CREATE TABLE IF NOT EXISTS Event (
        eventID text PRIMARY KEY,
        username text,
        title text,
        location text,
        datetime text,
        description text
        ); ''')

    db.execute('''CREATE TABLE IF NOT EXISTS Calendar (
        dateID text PRIMARY KEY,
        calendarDate text,
        monthNo int,
        dayOfWeek int
        );''')

    return


def main():
    conn = sqlite3.connect('taskScheduler.db')
    db = conn.cursor()
    createTables(db)
    authenticated = False
    username = None
    while not authenticated:
        print("Would you like to login or register?")
        userInput = input("type 'login' or 'register'")
        if userInput == "login":
            username = input("Enter username:")
            password = input("Enter password:")

            # Read username and password from database
            # Try to authenticate, if successful set authenticated to True
            user = (username, password)
            logged_in = loginUer(db, user)
            if logged_in:
                authenticated = True
                print("You successfully logged in!")
            else:
                print("Login failed!")

        if userInput == "register":
            username = input("Enter username:")
            email = input("Enter email:")
            # Check to make sure username isn't taken
            name = input("Enter name:")
            password = input("Enter password:")
            # Store information in database
            # Makes a User object and insert to Users table
            # Tells user if registration was successful
            new_user = (username, name, email, password)
            registered = registerUser(conn, new_user)
            if registered:
                authenticated = True
                print("You've successfully registered!")
            else:
                print("Registration failed!")

    userInput = input("What do you like to do?")
    while userInput != "quit":
        if userInput == "list tasks":
            print("list tasks")
            task = (username)
            rows = getAllTask(db, task)

            if len(rows) > 0:
                table = prettytable.PrettyTable(["eventID", "username", "title", "location", "time", "date", "bold",
                                                 "description"])

                for i in range(len(rows)):
                    row = []
                    curr_row = rows[i]
                    for j in range(len(curr_row)):
                        row.append(curr_row[j])
                    table.add_row(row)

                print(table)
            else:
                print("You have no task! Please add some task")

        if userInput == "create task":
            print("create task")
            event_id = str(uuid.uuid1())
            title = input("Title: ")
            location = input("Location: ")

            # Gotta set this the right way
            curr_time = "Test time"
            curr_date = "Test date"
            userInput = input("Is this task important? y or n")

            bold = False
            if userInput == "y":
                bold = True

            description = input("Description: ")

            task = (event_id, username, title, location, curr_time, curr_date, bold, description)
            successful = createTask(conn, task)

            if successful:
                print("Successfully created task")
            else:
                print("Fail to create task")

        if userInput == "delete task":
            print("delete task")
            event_id = input("Type event id: ")
            deleted = deleteTask(conn, event_id)
            if deleted:
                print("Successfully deleted!")
            else:
                print("Fail to delete!")

        if userInput == "help":
            print("help")

        userInput = input("What do you like to do?")

    return


if __name__ == '__main__':
    main()

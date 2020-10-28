#!/usr/bin/env python
import sys, os
import time
import sqlite3


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
        if userInput == "create task":
            print("create task")
        if userInput == "delete task":
            print("delete task")
        if userInput == "help":
            print("help")

    return


if __name__ == '__main__':
    main()

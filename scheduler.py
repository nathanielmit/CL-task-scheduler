#!/usr/bin/env python
import datetime
import sys, os
import time
import sqlite3
import uuid
import prettytable

# TODO: DISPLAY REMINDERS WHEN USERS LOG IN
# TODO: DISPLAY WELCOME TO USER WHEN THEY LOG IN
# TODO: Test all reminder functionality

def getAllReminders(db, username):
    db.execute("SELECT * FROM Reminder WHERE username=?", (username,))
    return(db.fetchall())

def printReminders(db, username):
    rows = getAllReminders(db, username)
    table = ""
    if len(rows) > 0:
        table = prettytable.PrettyTable(["taskID", "username", "title", "datetime","description"])
        for row in rows:
            table.add_row(row)

    print(table)
    return

def getTodaysReminders(db, username):
    db.execute("SELECT * FROM Reminder WHERE username=?", (username,))
    # yourdatetime.date() == datetime.today().date()
    rows = db.fetchAll()
    for row in rows:
        print(row)
    return

def createReminder(db, reminder):
    sql = ''' INSERT INTO Reminder(name, datetime)
              VALUES(?,?,?,?,?) '''
    db.execute(sql, reminder)
    return

def deleteReminder(db, reminderToDelete):
    sql = ''' DELETE FROM Reminder WHERE username=? AND title=? '''
    result = db.execute(sql, taskToDelete)
    if result.rowcount > 0:
        return True
    else:
        return False

def getAllTask(db, username):
    db.execute("SELECT * FROM Task WHERE username=?", (username,))
    return(db.fetchall())

def printTasks(db, username):
    rows = getAllTask(db, username)
    table = ""
    if len(rows) > 0:
        table = prettytable.PrettyTable(["taskID", "username", "title", "datetime","description"])
        for row in rows:
            table.add_row(row)

    print(table)
    return

def deleteTask(db, taskToDelete):
    sql = ''' DELETE FROM Task WHERE username=? AND title=? '''
    result = db.execute(sql, taskToDelete)
    if result.rowcount > 0:
        return True
    else:
        return False


def createTask(db, task):
    sql = ''' INSERT INTO Task(taskID, username, title, datetime, description)
              VALUES(?,?,?,?,?) '''
    db.execute(sql, task)
    return


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

def createTables(db):
    db.execute('''CREATE TABLE IF NOT EXISTS User (
        username text PRIMARY KEY,
        name text NOT NULL,
        password text NOT NULL
        );''')

    db.execute('''CREATE TABLE IF NOT EXISTS Task (
        taskID text PRIMARY KEY,
        username text,
        title text,
        datetime date,
        description text,
        CONSTRAINT unq UNIQUE (username, title)
        ); ''')

    db.execute('''CREATE TABLE IF NOT EXISTS Reminder (
        reminderID integer PRIMARY KEY AUTOINCREMENT,
        name text, 
        datetime date
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
        userInput = input("type 'login' or 'register'\n")
        if userInput == "login":
            username = input("Enter username: ")
            password = input("Enter password: ")

            # Read username and password from database
            # Try to authenticate, if successful set authenticated to True
            user = (username, password)
            logged_in = loginUser(db, user)
            conn.commit()
            if logged_in:
                authenticated = True
                print("You successfully logged in!")
            else:
                print("Login failed!")

        if userInput == "register":
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

    userInput = input("What would you like to do?\n")
    while userInput != "quit":
        # Print all user tasks
        if userInput == "list tasks":
            printTasks(db, username)
        
        # Create task
        if userInput == "create task":
            task_id = str(uuid.uuid1())
            title = input("Title: ")
            date = datetime.datetime.strptime(input("Enter date and time (mm/dd/yyyy HH:MM): "), "%m/%d/%Y %H:%M")
            description = input("Description: ")

            task = (task_id, username, title, date, description)
            createTask(db, task)
            print("Successfully created task")

        # Delete a task
        if userInput == "delete task":
            # Get tasks to print
            print("Your tasks:\n")
            printTasks(db, username)

            taskName = input("Enter name of task to delete: ")
            print("Going to delete: ", username, taskName)
            taskToDelete = (username, taskName)
            deleted = deleteTask(db, taskToDelete)
            conn.commit()
            if deleted:
                print("Successfully deleted!")
            else:
                print("Failed to delete!")
        # Print all user reminders
        if userInput == "list reminders":
            printReminders(db, username)
        
        # Create task
        if userInput == "create reminder":
            name = input("Title: ")
            date = datetime.datetime.strptime(input("Enter date and time (mm/dd/yyyy HH:MM): "), "%m/%d/%Y %H:%M")

            reminder = (name, date)
            createReminder(db, reminder)
            print("Successfully created reminder")

        # Delete a task
        if userInput == "delete reminder":
            # Get tasks to print
            print("Your tasks:\n")
            printReminders(db, username)

            reminderName = input("Enter name of reminder to delete: ")
            reminderToDelete = (username, reminderName)
            deleted = deleteReminder(db, reminderToDelete)
            conn.commit()
            if deleted:
                print("Successfully deleted!")
            else:
                print("Failed to delete!")
        if userInput == "help":
            print("commands:\nlist tasks, create task, delete task")

        userInput = input("What would you like to do?\n")
    db.close()
    return


if __name__ == '__main__':
    main()

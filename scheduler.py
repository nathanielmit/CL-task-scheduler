#!/usr/bin/env python
import datetime
import sys, os
import time
import sqlite3
import uuid
import prettytable

from reminder import *
from task import *
from user import *

def createExampleData(db, conn):
    # Create 10 users
    for i in range(10):
        registerUser(db, ("username"+str(i), "name"+str(i), "password"+str(i)))

    # Create 10 tasks
    for i in range(10):
        createTask(db, (str(uuid.uuid1()), "username"+str(i), "Title num "+str(i), "10/30/2020 12:30", "Example description num "+str(i)))

    # Create 10 reminders
    for i in range(10):
        createReminder(db, ("username"+str(i), "Reminder number "+str(i), "10/30/2020 12:30"))

    conn.commit()
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
        username,
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
    exData = input("Create example data?")
    if exData == 'y':
        createExampleData(db, conn)

    while not authenticated:
        print("Would you like to login or register?")
        userInput = input("type 'login' or 'register'\n")
        if userInput == "login":
            authenticated, username = login(db)
        if userInput == "register":
            authenticated, username = register(db, conn)

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
            conn.commit()
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
        
        if userInput == "list all users":
            printAllUsers(db)

        if userInput == "list all reminders":
            printAllReminders(db)

        if userInput == "list all tasks":
            printAllTasks(db)

        # Create task
        if userInput == "create reminder":
            name = input("Name: ")
            date = datetime.datetime.strptime(input("Enter date and time (mm/dd/yyyy HH:MM): "), "%m/%d/%Y %H:%M")

            reminder = (username, name, date)
            createReminder(db, reminder)
            conn.commit()
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
            print("commands:\nlist tasks, create task, delete task, list all tasks, list all reminders, list all users:")

        userInput = input("What would you like to do?\n")
    db.close()
    return


if __name__ == '__main__':
    main()
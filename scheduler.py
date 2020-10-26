#!/usr/bin/env python
import sys,os
import time
import sqlite3

def convertTimeToPythonFormat(userTime):
    # takes user's mm/dd/yyyy hh:mm and turns it into a python time format
    return

def convertTimeToUserFormat(pythonTime):

    return

def createTables(db):

    db.execute( '''CREATE TABLE IF NOT EXISTS Users (
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

    db.execute( '''CREATE TABLE IF NOT EXISTS Calendar (
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
    while authenticated != True:
        print("Would you like to login or register?")
        userInput = input("type 'login' or 'register'")
        if userInput == "login":
            username = input("Enter username:")
            password = input("Enter password:")
            # try to authenticate, if successful set authenticated to True


        if userInput == "register":
            username = input("Enter username:")
            # Check to make sure username isn't taken
            name = input("Enter name:")
            password = input("Enter password:")
            # Store information in database
            authenticated = True
        

    userInput = ""
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

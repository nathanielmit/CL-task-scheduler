import prettytable

def getUserReminders(db, username):
    db.execute("SELECT * FROM Reminder WHERE username=?", (username,))
    return(db.fetchall())

def printReminders(db, username):
    rows = getUserReminders(db, username)
    table = ""
    if len(rows) > 0:
        table = prettytable.PrettyTable(["taskID", "username", "name", "datetime"])
        for row in rows:
            table.add_row(row)

    print(table)
    return

def printAllReminders(db):
    db.execute("SELECT * FROM Reminder")
    rows = db.fetchall()
    table = ""
    if len(rows) > 0:
        table = prettytable.PrettyTable(["taskID", "username", "name", "datetime"])
        for row in rows:
            table.add_row(row)

    print(table)
    return

def getTodaysReminders(db, username):
    db.execute("SELECT * FROM Reminder WHERE username=?", (username,))
    # yourdatetime.date() == datetime.today().date()
    rows = db.fetchall()
    if len(rows) > 0:
        print("Your reminders for today:")
    for row in rows:
        print(row[2],"at",row[3])
    return

def createReminder(db, reminder):
    sql = ''' INSERT INTO Reminder(username, name, datetime)
              VALUES(?,?,?) '''
    db.execute(sql, reminder)
    return

def deleteReminder(db, reminderToDelete):
    sql = ''' DELETE FROM Reminder WHERE username=? AND name=? '''
    result = db.execute(sql, reminderToDelete)
    if result.rowcount > 0:
        return True
    else:
        return False
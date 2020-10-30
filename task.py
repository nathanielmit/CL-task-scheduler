import prettytable

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

def printAllTasks(db):
    db.execute("SELECT * FROM Task")
    rows = db.fetchall()
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
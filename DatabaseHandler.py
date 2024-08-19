"""
FILE NAME - DatabaseHandler.py
PROGRAMMER - Angel Parra
DATE - 01/08/2024
DESCRIPTION -
NAMING CONVENTIONS - all variables use camel case eg - helloWorld - and all functions
    and classes pascal case on each word eg - ToListBoxFormat -
"""
import sqlite3
import pandas as pd
import argon2.exceptions
from argon2._password_hasher import PasswordHasher

databaseFilePath = 'finance management.db'
hasher = PasswordHasher(time_cost=10)


def ExecuteSQLScripts(returnRows: bool, *args: str, **kwargs):
    """
    Executes SQL scripts on the database.
    :param returnRows: Boolean indicating if the function should return rows from the query.
    :param args: SQL query strings to execute.
    :param kwargs: Optional keyword arguments for parameterized queries.
    :return: List of rows if returnRows is True, otherwise None.
    """
    conn = sqlite3.connect(databaseFilePath)
    c = conn.cursor()
    try:
        if len(kwargs) > 0:
            for value in kwargs.values():
                c.execute(args[0], value)
        else:
            for i in args:
                c.execute(i)
        conn.commit()
        if returnRows:
            rows = c.fetchall()
            c.close()
            conn.close()
            return rows
    except Exception as e:
        c.close()
        conn.close()
        raise e
    c.close()
    conn.close()
    return None


# Create tables
ExecuteSQLScripts(False,
                  '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    factorQ INTEGER NOT NULL,
    factorA TEXT NOT NULL
)
''',
                  '''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''',
                  '''
CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    amount REAL NOT NULL,
    end_date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''',
                  '''
CREATE TABLE IF NOT EXISTS investments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''',
                  '''
CREATE TABLE IF NOT EXISTS goal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL,
    amount REAL,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')


def CheckUser(username, password):
    """
    Checks if a user exists and verifies the password.
    :param username: The username of the user.
    :param password: The password of the user.
    :return: True if the user exists and the password is correct, otherwise False.
    """
    rows = ExecuteSQLScripts(True, "SELECT * FROM users WHERE username = ?", value=(username,))
    if not rows:
        return False
    try:
        hasher.verify(rows[0][3], password)
        return True
    except argon2.exceptions.VerifyMismatchError as e:
        print(e)
        return False
    except argon2.exceptions.InvalidHashError as e:
        print(e)
        return False


def CheckTwoFactor(username, twoFactorQ, twoFactorA):
    """
    Checks the two-factor authentication question and answer for a user.
    :param username: The username of the user.
    :param twoFactorQ: The security question.
    :param twoFactorA: The answer to the security question.
    :return: True if the question and answer are correct, otherwise False.
    """
    rows = ExecuteSQLScripts(True, "SELECT factorQ, factorA FROM users WHERE username = ?", value=(username,))
    if not rows:
        return False
    stored_q = rows[0][0]
    stored_a = rows[0][1]
    if stored_q != twoFactorQ:
        return False
    try:
        hasher.verify(stored_a, twoFactorA.lower().strip())
        return True
    except argon2.exceptions.VerifyMismatchError:
        return False
    except argon2.exceptions.InvalidHashError as e:
        print(e)
        return False


def ChangePassword(username, new_password):
    """
    Changes the password for a user.
    :param username: The username of the user.
    :param new_password: The new password for the user.
    :return: True if the password was changed successfully, otherwise False.
    """
    hashed_new_password = hasher.hash(new_password)
    try:
        ExecuteSQLScripts(False, "UPDATE users SET password = ? WHERE username = ?",
                          value=(hashed_new_password, username))
        return True
    except Exception as e:
        print(e)
        return False


def PullGoalsData(user_id):
    """
    Retrieves goals data for a user.
    :param user_id: The ID of the user.
    :return: DataFrame containing the goal's data.
    """
    conn = sqlite3.connect(databaseFilePath)
    query = '''
        SELECT goal.name, goal.description, goal.date, goal.amount,goal.id
        FROM users
        INNER JOIN goal ON users.id = goal.user_id
        WHERE users.id = ?
    '''
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    return df


def PullTransactionsData(user_id):
    """
    Retrieves transactions data for a user.
    :param user_id: The ID of the user.
    :return: DataFrame containing the transactions data.
    """
    conn = sqlite3.connect(databaseFilePath)
    query = '''
        SELECT transactions.amount, transactions.date, transactions.description, transactions.id
        FROM users
        INNER JOIN transactions ON users.id = transactions.user_id
        WHERE users.id = ?
    '''
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    return df


def PullBudgetsData(user_id):
    """
    Retrieves budgets data for a user.
    :param user_id: The ID of the user.
    :return: DataFrame containing the budget's data.
    """
    conn = sqlite3.connect(databaseFilePath)
    query = '''
        SELECT budgets.name, budgets.amount, budgets.end_date, budgets.id
        FROM users
        INNER JOIN budgets ON users.id = budgets.user_id
        WHERE users.id = ?
    '''
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    return df


def PullInvestmentsData(user_id):
    """
    Retrieves investments data for a user.
    :param user_id: The ID of the user.
    :return: DataFrame containing the investments data.
    """
    conn = sqlite3.connect(databaseFilePath)
    query = '''
        SELECT investments.name, investments.date, investments.id
        FROM users
        INNER JOIN investments ON users.id = investments.user_id
        WHERE users.id = ?
    '''
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    return df


def PullUsersData(username):
    """
    Retrieves data for a specific user.
    :param username: The username of the user.
    :return: Data retrieved from the database for the user.
    """
    query = '''
        SELECT * FROM users WHERE username = ?
    '''
    data = ExecuteSQLScripts(True, query, value=(username,))
    return data


def AddUser(username, name, password, factorQ, factorA):
    """
    Adds a new user to the database.
    :param username: The username of the new user.
    :param name: The name of the new user.
    :param password: The password of the new user.
    :param factorQ: The security question for the new user.
    :param factorA: The answer to the security question.
    """
    query = '''
    INSERT INTO users (username, name, password, factorQ, factorA)
    VALUES (?, ?, ?, ?, ?)
    '''
    ExecuteSQLScripts(False, query,
                      value=(username, name, hasher.hash(password), factorQ, hasher.hash(factorA.lower().strip())))


def AddTransaction(user_id, amount, date, description):
    """
    Adds a new transaction for a user.
    :param user_id: The ID of the user.
    :param amount: The amount of the transaction.
    :param date: The date of the transaction.
    :param description: The description of the transaction.
    """
    query = '''
    INSERT INTO transactions (user_id, amount, date, description)
    VALUES (?, ?, ?, ?)
    '''
    ExecuteSQLScripts(False, query, value=(user_id, amount, date, description))


def AddBudget(user_id, name, amount, end_date):
    """
    Adds a new budget for a user.
    :param user_id: The ID of the user.
    :param name: The name of the budget.
    :param amount: The amount of the budget.
    :param end_date: The end date of the budget.
    """
    query = '''
    INSERT INTO budgets (user_id, name, amount, end_date)
    VALUES (?, ?, ?, ?)
    '''
    ExecuteSQLScripts(False, query, value=(user_id, name, amount, end_date))


def AddInvestment(user_id, name, date):
    """
    Adds a new investment for a user.
    :param user_id: The ID of the user.
    :param name: The name of the investment.
    :param date: The date of the investment.
    """
    query = '''
    INSERT INTO investments (user_id, name, date)
    VALUES (?, ?, ?)
    '''
    ExecuteSQLScripts(False, query, value=(user_id, name, date))


def AddGoal(user_id, name, description, date, amount):
    """
    Adds a new goal for a user.
    :param user_id: The ID of the user.
    :param name: The name of the goal.
    :param description: The description of the goal.
    :param date: The date of the goal.
    :param amount: The amount of the goal.
    """
    query = '''
    INSERT INTO goal (user_id, name, description, date, amount)
    VALUES (?, ?, ?, ?, ?)
    '''
    ExecuteSQLScripts(False, query, value=(user_id, name, description, date, amount))


def DeleteGoal(goal_id: int):
    """
    Deletes a goal from the database.
    :param goal_id: The ID of the goal to be deleted.
    """
    try:
        ExecuteSQLScripts(False, "DELETE FROM goal WHERE id = ?", values=(goal_id,))
    except sqlite3.Error as e:
        print(f"Error deleting goal: {e}")


def DeleteTransaction(transactionID: int):
    """
    Deletes a transaction from the database.
    :param transactionID: The ID of the transaction to be deleted.
    """
    try:
        ExecuteSQLScripts(False, "DELETE FROM transactions WHERE id = ?", values=(transactionID,))
    except sqlite3.Error as e:
        print(f"Error deleting transaction: {e}")
    except Exception as e:
        print(e)

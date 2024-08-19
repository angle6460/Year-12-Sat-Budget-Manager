# Budget Management Application
## Table of Contents
- [Description](#description)
- [Files and Their Roles](#files-and-their-roles)
  - [Budget Manager.py](#budget-managerpy)
  - [DatabaseHandler.py](#databasehandlerpy)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Starting the Program](#starting-the-program)
  - [Getting Started](#getting-started)
- [Forgot Password](#forgot-password)
## Description
This is a budget management application designed to help users manage their finances by tracking transactions, managing budgets, and visualizing financial data. The application includes functionalities for user account management, data visualization, and database operations.

## Files and Their Roles
### Budget Manager.py
- Role: Main application script.
- Description: Manages user account data, adds new data, sorts data, and displays data. It also includes functionality for data visualization.
- Dependencies:
  - sqlite3
  - CTkToolTip
  - pandas
  - DatabaseHandler
  - PIL
  - tkinter
  - customtkinter
  - datetime
  - re
  - matplotlib
  - images folder
- Classes:
  - CustomPlot: A class to create and manage a custom plot using `matplotlib` within a Tkinter application.
  - User: A class for a user with their associated financial data.
  - SignInPage: A class to create the Sign-In Page for the application.
  - CreateAccountPage: A class to create the Create Account Page for the application.
  - MainPage: The Main page of the Application.

### DatabaseHandler.py
- Role: Handles database operations.
- Description: Executes SQL scripts and sets up the necessary database structure. Manages user accounts, goals, transactions, investments and budgets.
- Dependencies:
  - sqlite3
  - pandas
  - argon2


## Getting Started
### Prerequisites
Ensure you have the following dependencies installed:
- sqlite3
- CTkToolTip
- pandas
- PIL
- tkinter
- customtkinter
- matplotlib
- argon2
- images folder

You can install the Python dependencies using pip in your cmd:
```pip install sqlite3 pandas pillow tkinter customtkinter matplotlib argon2 CTkToolTip```

The images folder should be included in the installation.

### Starting the program
Run the 'Budget Manager.py' file in however way you would like, ensuring you have a python version that is compatible with python 3.11
Happy financing!

### Getting started
If this is your first time loading up the software then most likely you'll need to sign up
1. Click on the 'create one' button. This will take you to a create account page
2. Fill out the fields (username, password, name)
3. Choose your security question. This question will be used to verify your identity in case you have forgotten your password
4. Fill out the two factor answer (this is YOUR answer to the question you've selected above)
5. Click Create. Your account has been created By now you've successfully created an account
Now sign in by filling the required fields and then clicking Login. This will take you to the main page of the program

Now you're in
From here you can see multiple tabs in this order
1. **Home:** This is the landing page when you sign in. It displays your current account balance and your next goal's date. You can also change the view of the program to light or dark mode or to use system settings(default). There is also a logout button if you want to sign in as a different user
2. **Goals:** In this tab, you can add or remove financial goals. They have a name, description(optional), day and money attached to it. You can sort the goals by using the radio button below the table
3. **Balance:** In this tab, you can add transactions. They will be automatically assigned as income or expense. You can add with date, amount and description(optional), and sort the incomes/expenses
4. **Statistics:** In this tab, it will load the transaction data you have entered and display them in a graph. The visualisation will show you how your account TOTAL balance has changed over the dates you have entered.
5. **Investment Tracking:** WIP
6. **Budgeting:** WIP

Congrats!
You can now use the program with ease.
Happy financing!


### Forgot Password
Forgot your password? No Problem
1. Click reset password
2. Enter your username and the press continue
3. Enter the question you chose when you signed up and the answer to that said question.
4. Enter your new password And with any luck your password will be changed. The program will notify you if the password has been changed.

Now go and try sign in.
Happy financing!




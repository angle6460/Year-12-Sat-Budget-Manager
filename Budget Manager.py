"""PROGRAMMER - Angel Parra DATE - 01/08/2024 DESCRIPTION - Page to; display all user account data, to add new user
data and save that data, and to sort the data. NAMING CONVENTIONS - All variables use camelCase (e.g., helloWorld)
and all functions and classes use PascalCase (e.g., ToListBoxFormat).

Some other notes about the conventions of the code.
  When creating labels and buttons that don't require it to be called again, it doesn't create a variable assigned to it
    (e.g.,
        customtkinter.CTkLabel('params').grid('params')
        will be used over the:
        self.label = custom.CTkLabel('params')
        self.label.grid('params')
    )
    This is done so variable aren't unnecessarily created for widgets that won't be called up again
    However widget such as entry and combobox will as they need to be called again to read their values
"""
import sqlite3
from CTkToolTip import CTkToolTip
import pandas as pd
import DatabaseHandler
from PIL import Image
from tkinter import messagebox
import tkinter.ttk
import customtkinter
from datetime import datetime
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CustomPlot:
    """
    A class to create and manage a custom plot using matplotlib within a Tkinter application.
    """

    def __init__(self, parent: tkinter.Widget, title: str, xLabel: str, yLabel: str, width: int = 3, height: int = 3):
        """
        Initializes the CustomPlot with given parameters and creates an initial plot.
        :param parent: The parent widget to contain the plot.
        :param title: The title of the plot.
        :param xLabel: The label for the x-axis.
        :param yLabel: The label for the y-axis.
        :param width: The width of the plot (default is 3).
        :param height: The height of the plot (default is 3).
        """

        self.fig, self.ax = plt.subplots(figsize=(width, height))
        self.ax.set_title(title, fontsize=6)
        self.ax.set_xlabel(xLabel, fontsize=1)
        self.ax.set_ylabel(yLabel, fontsize=3)

        # Adjust tick parameters
        self.ax.tick_params(axis='both', which='major', labelsize=8)
        self.ax.tick_params(axis='both', which='minor', labelsize=6)

        # Create a canvas and add the plot to it
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().grid(row=1, column=0)

        # Initial plot
        df = pd.DataFrame({
            'date': pd.to_datetime(['2021-12-12', '2021-12-12', '2021-12-12', '2021-12-12']),
            'amount': [100.0, 1000.0, -1000.0, -1000.0]
        })
        self.line, = self.ax.plot(df['date'], df['amount'])
        self.fig.autofmt_xdate()  # Rotate and align the tick labels, so they look better.

    def UpdatePlot(self, df, x, y):
        """
        Updates the plot with new data.
        :param df: The DataFrame containing the new data.
        :param x: The column name for the x-axis data.
        :param y: The column name for the y-axis data.
        :return:
        """
        # Update the plot
        self.line.set_xdata(df[x])
        self.line.set_ydata(df[y])
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.autofmt_xdate()  # Rotate and align the tick labels, so they look better.
        self.canvas.draw()


class User:
    """
    A class for a user with their associated financial data.
    """

    def __init__(self):
        """Initializes a User object with default values and empty DataFrames."""
        self.id: int = -1
        self.name: str = ''
        self.goals: pd.DataFrame = pd.DataFrame()
        self.transactions: pd.DataFrame = pd.DataFrame()
        self.investments: pd.DataFrame = pd.DataFrame()
        self.budgets: pd.DataFrame = pd.DataFrame()

    def EmptyData(self):
        """Resets all user data to default values and empty DataFrames."""
        self.id: int = -1
        self.name: str = ''
        self.goals: pd.DataFrame = pd.DataFrame()
        self.transactions: pd.DataFrame = pd.DataFrame()
        self.investments: pd.DataFrame = pd.DataFrame()
        self.budgets: pd.DataFrame = pd.DataFrame()

    def LoadData(self, username: str):
        """
        Loads all user data based on the provided username.
        :param username: The username of the user to load data for.
        """
        self.LoadUserData(username)
        self.LoadGoalData()
        self.LoadTransactionData()
        self.LoadInvestmentData()
        self.LoadBudgetData()

    def LoadUserData(self, username: str):
        """
        Loads basic user data from the database.
        :param username: The username of the user to load data for.
        """
        self.id, self.name, username, password, factorQ, factorA = DatabaseHandler.PullUsersData(username)[0]

    def LoadGoalData(self):
        """Loads the user's financial goals from the database."""
        self.goals = DatabaseHandler.PullGoalsData(self.id)

    def LoadTransactionData(self):
        """Loads the user's transactions from the database."""
        self.transactions = DatabaseHandler.PullTransactionsData(self.id)

    def LoadInvestmentData(self):
        """Loads the user's investments from the database."""
        self.investments = DatabaseHandler.PullInvestmentsData(self.id)

    def LoadBudgetData(self):
        """Loads the user's budgets from the database."""
        self.budgets = DatabaseHandler.PullBudgetsData(self.id)


class SignInPage(customtkinter.CTkToplevel):
    """A class to create the Sign-In Page for the application."""

    def __init__(self, mainPage):
        """
        Initializes the SignInPage with the main page of the application.
        :param mainPage: The main window of the application.
        """

        super().__init__()
        self.geometry('550x700')
        self.mainWindow = mainPage
        self.createAccountWindow: CreateAccountPage = None
        # set a protocol of when the window closes, call the OnClose function
        self.protocol("WM_DELETE_WINDOW", self.OnClose)

        self.title('SavvySaver Sign in')
        # create the sign in frame and create new acc frame
        self.signInFrame = customtkinter.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height())
        self.signInFrame.grid(row=0, column=0, sticky="nsew")
        self.resetPasswordFrame = customtkinter.CTkFrame(self, width=self.winfo_width(),
                                                         height=self.winfo_height() - 20)
        self.resetPasswordFrame.grid(row=0, column=0, sticky="nsew")
        self.resetPasswordFrame2 = customtkinter.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height())
        self.resetPasswordFrame2.grid(row=0, column=0, sticky="nsew")
        self.signInFrame.tkraise()  # the signin page on top

        customtkinter.CTkLabel(self.signInFrame, text='Sign In', font=customtkinter.CTkFont(size=40)).grid(row=0,
                                                                                                           column=0,
                                                                                                           columnspan=2,
                                                                                                           pady=(5, 70))
        self.usernameEntry = customtkinter.CTkEntry(self.signInFrame, placeholder_text='Username:',
                                                    font=customtkinter.CTkFont(size=30), width=200)
        self.usernameEntry.grid(
            row=1, column=0, padx=20)
        self.passwordEntry = customtkinter.CTkEntry(self.signInFrame, placeholder_text='Password:',
                                                    font=customtkinter.CTkFont(size=30), width=200)
        self.passwordEntry.grid(
            row=2, column=0, padx=20)
        customtkinter.CTkButton(self.signInFrame, text='Login', command=self.SignIn,
                                font=customtkinter.CTkFont(size=20)).grid(row=1, column=1, rowspan=2,
                                                                          sticky='news', padx=20,
                                                                          pady=20)
        customtkinter.CTkLabel(self.signInFrame, text='No Account?', font=customtkinter.CTkFont(size=20)).grid(row=3,
                                                                                                               column=0,
                                                                                                               pady=(
                                                                                                                   20,
                                                                                                                   10))
        customtkinter.CTkLabel(self.signInFrame, text='Forgot Password?', font=customtkinter.CTkFont(size=20)).grid(
            row=4, column=0, pady=(10, 20))
        customtkinter.CTkButton(self.signInFrame, text='Create One', command=self.CreateAccount,
                                font=customtkinter.CTkFont(size=20)).grid(row=3, column=1,
                                                                          pady=(20, 10))
        customtkinter.CTkButton(self.signInFrame, text='Reset Password', command=self.OpenResetPassword,
                                font=customtkinter.CTkFont(size=20)).grid(row=4,
                                                                          column=1,
                                                                          pady=(10, 20))
        customtkinter.CTkLabel(self.resetPasswordFrame, text='Reset Account\nPassword',
                               font=customtkinter.CTkFont(size=40)).grid(row=0,
                                                                         column=0,
                                                                         columnspan=2,
                                                                         pady=(5, 70))
        self.resetPasswordEntry = customtkinter.CTkEntry(self.resetPasswordFrame, placeholder_text='Username:',
                                                         font=customtkinter.CTkFont(size=40), width=200)
        self.resetPasswordEntry.grid(row=1, column=0)
        customtkinter.CTkButton(self.resetPasswordFrame, text='Continue', command=self.OpenResetPassword2,
                                font=customtkinter.CTkFont(size=20)).grid(row=2, column=0)
        customtkinter.CTkButton(self.resetPasswordFrame, text='Return', command=self.OpenSignIn,
                                font=customtkinter.CTkFont(size=20)).grid(row=3, column=1)
        # second page of two factor
        customtkinter.CTkLabel(self.resetPasswordFrame2, font=customtkinter.CTkFont(size=40),
                               text='Enter Two\nFact Authentication').grid(row=0, column=0, columnspan=2)
        self.twoFactorQuestions = ['What was your first pet',
                                   'Who was your favourite movie character',
                                   'What was your first address',
                                   'Name of your first love']
        self.twoFactorQCombo = customtkinter.CTkComboBox(self.resetPasswordFrame2, values=self.twoFactorQuestions,
                                                         font=customtkinter.CTkFont(size=20))
        self.twoFactorQCombo.grid(row=1, column=0, columnspan=2)
        self.twoFactorAEntry = customtkinter.CTkEntry(self.resetPasswordFrame2, placeholder_text='Two Factor Answer',
                                                      font=customtkinter.CTkFont(size=20))
        self.twoFactorAEntry.grid(row=2, column=0, columnspan=2)
        self.newPasswordEntry = customtkinter.CTkEntry(self.resetPasswordFrame2, placeholder_text='New Password',
                                                       font=customtkinter.CTkFont(size=20))
        self.newPasswordEntry.grid(row=3, column=0, columnspan=2)
        customtkinter.CTkButton(self.resetPasswordFrame2, text='Create', command=self.ResetPassword,
                                font=customtkinter.CTkFont(size=20)).grid(row=4, column=0)
        customtkinter.CTkButton(self.resetPasswordFrame2, text='Return', command=self.OpenResetPassword,
                                font=customtkinter.CTkFont(size=20)).grid(row=4, column=1)

    def OnClose(self):
        """Destroys the main window when the sign-in page is closed."""
        self.mainWindow.destroy()

    def SignIn(self):
        """Handles the sign-in process."""
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        if not DatabaseHandler.CheckUser(username, password):
            # Failed the sign in
            messagebox.showerror('Error', "Couldn't sign in")
            return

        # Sign-in successful
        self.mainWindow.LogIn(username)

    def OpenResetPassword(self):
        """Opens the first part of the password reset frame."""
        self.resetPasswordFrame.tkraise()

    def OpenResetPassword2(self):
        """Opens the second part of the password reset frame."""
        # Verifies that user put in username
        if self.resetPasswordEntry.get().strip() == '':
            self.resetPasswordEntry.configure(border_color='red')
            return
        self.resetPasswordEntry.configure(border_color='grey')
        self.resetPasswordFrame2.tkraise()  # opens the next part of the reset password pages

    def ResetPassword(self):
        """Handles the password reset process."""
        # Get all information from GUI
        username = self.resetPasswordEntry.get()
        question = self.twoFactorQCombo.get()
        answer = self.twoFactorAEntry.get()
        newPassword = self.newPasswordEntry.get()

        passed = True
        # Verify that the fields are filled in
        if question not in self.twoFactorQuestions:
            self.twoFactorQCombo.configure(border_color='red')
            passed = False
        else:
            self.twoFactorQCombo.configure(border_color='grey')
        if answer == '':
            self.twoFactorAEntry.configure(border_color='red')
            passed = False
        else:
            self.twoFactorAEntry.configure(border_color='grey')
        if newPassword == '':
            self.newPasswordEntry.configure(border_color='red')
            passed = False
        else:
            self.newPasswordEntry.configure(border_color='grey')
        if not passed:  # If at least one of the entries fail
            return
        # Get the question in int form. this is because that is what's saved in the db
        num = 0
        for i in range(len(self.twoFactorQuestions)):
            if question == self.twoFactorQuestions[i]:
                num = i
                break

        # Use database handler functions to change password
        if not DatabaseHandler.CheckTwoFactor(username, num, answer):
            messagebox.showerror('Failed', "Couldn't verify your details.")
            return
        if not DatabaseHandler.ChangePassword(username, newPassword):
            messagebox.showerror('Error', "Couldn't change password")
            return
        # Success
        messagebox.showinfo('Success', 'Password successfully changed.')
        self.OpenSignIn()

    def OpenSignIn(self):
        """Opens the sign in frame"""
        self.signInFrame.tkraise()

    def CreateAccount(self):
        """Opens the create account window"""
        if self.createAccountWindow is None or not self.createAccountWindow.winfo_exists():
            self.createAccountWindow = CreateAccountPage(self)
            self.withdraw()
        else:
            self.createAccountWindow.focus()

    def CloseCreateAccount(self):
        """Handles the destruction of the create account window"""
        self.createAccountWindow.destroy()
        self.deiconify()  # Show this window again


class CreateAccountPage(customtkinter.CTkToplevel):
    """
    A class to create the Create Account Page for the application.
    """

    def __init__(self, signInPage: SignInPage):
        """
        Initializes the create account page of the application.
        :param signInPage: The sign-in window of the application
        """
        super().__init__()
        self.geometry('700x800')
        self.signInWindow = signInPage
        self.protocol("WM_DELETE_WINDOW", self.signInWindow.OnClose)

        customtkinter.CTkLabel(self, text='New Account', font=customtkinter.CTkFont(size=40)).grid(row=0, column=0,
                                                                                                   columnspan=2,
                                                                                                   sticky='news',
                                                                                                   padx=20, pady=20)
        self.usernameEntry = customtkinter.CTkEntry(self, placeholder_text='Username:',
                                                    font=customtkinter.CTkFont(size=20), width=250)
        self.usernameEntry.grid(row=1, column=0, padx=10, pady=10)
        self.passwordEntry = customtkinter.CTkEntry(self, placeholder_text='Password:',
                                                    font=customtkinter.CTkFont(size=20), width=250)
        self.passwordEntry.grid(row=2, column=0, padx=10, pady=10)
        self.nameEntry = customtkinter.CTkEntry(self, placeholder_text='Name:', font=customtkinter.CTkFont(size=20),
                                                width=250)
        self.nameEntry.grid(row=3, column=0, padx=10, pady=10)
        self.twoFactAnsEntry = customtkinter.CTkEntry(self, placeholder_text='Two Factor Answer:',
                                                      font=customtkinter.CTkFont(size=20), width=250)
        self.twoFactAnsEntry.grid(row=2, column=1, padx=10, pady=10)
        self.twoFactorQuestions = ['What was the name of your first pet',
                                   'Who was your favourite movie character',
                                   'What was your first address',
                                   'What was the name of your first love']
        self.twoFactQuesCombo = customtkinter.CTkComboBox(self, values=self.twoFactorQuestions,
                                                          font=customtkinter.CTkFont(size=20), width=400)
        self.twoFactQuesCombo.grid(row=1, column=1, padx=10, pady=10)
        customtkinter.CTkButton(self, command=self.signInWindow.CloseCreateAccount, text='Back',
                                font=customtkinter.CTkFont(size=20)).grid(row=4, column=0, padx=10, pady=10)
        customtkinter.CTkButton(self, command=self.Create, text='Create', font=customtkinter.CTkFont(size=20)).grid(
            row=3, column=1, padx=10, pady=10)
        customtkinter.CTkLabel(self, text='By clicking I accept the\nterms and conditions').grid(row=4, column=1)

    def Create(self):
        """Handles the creation of a new user into a database"""
        RED = 'Red'
        GREY = 'Grey'

        # Get all data from the GUI
        name = self.nameEntry.get()
        password = self.passwordEntry.get()
        username = self.usernameEntry.get()
        twoFactorQuestion = self.twoFactQuesCombo.get()
        twoFactorAnswer = self.twoFactAnsEntry.get()

        passed = True  # Verify that the fields are filled in
        if name.strip() == '':
            passed = False
            self.nameEntry.configure(border_color=RED)
        else:
            self.nameEntry.configure(border_color=GREY)
        if password.strip() == '':
            passed = False
            self.passwordEntry.configure(border_color=RED)
        else:
            self.passwordEntry.configure(border_color=GREY)
        if username.strip() == '':
            passed = False
            self.usernameEntry.configure(border_color=RED)
        else:
            self.usernameEntry.configure(border_color=GREY)
        if twoFactorAnswer.strip() == '':
            passed = False
            self.twoFactAnsEntry.configure(border_color=RED)
        else:
            self.twoFactAnsEntry.configure(border_color=GREY)
        if twoFactorQuestion not in self.twoFactorQuestions:
            passed = False
            self.twoFactQuesCombo.configure(border_color=RED)
        else:
            self.twoFactQuesCombo.configure(border_color=GREY)
        if not passed:
            return

        # Get the two factor question in int form. This is done because in the database it is saved as an int
        num = 0
        for i in range(len(self.twoFactorQuestions)):
            if twoFactorQuestion == self.twoFactorQuestions[i]:
                num = i
                break
        try:  # Try to add the user into the database
            DatabaseHandler.AddUser(username, name, password, num, twoFactorAnswer)
            messagebox.showinfo('Success', 'User created')
        except sqlite3.IntegrityError:  # This exception will be thrown if the username is taken
            # Show error message that the username is taken
            messagebox.showerror(title="Error", message="Username Already Taken\nPlease Try Again.")


class MainPage(customtkinter.CTk):
    """
    The Main page of the Application.
    It will automatically close this window and open the sign in window on initialisation
    """

    def __init__(self):
        """Initialises the Main page. Then creates the sign in window and hides the main window"""
        super().__init__()
        self.geometry("1100x700")
        self.resizable(False, False)

        self.user = User()

        # configure sidebar
        """
        Here buttons will be assigned to a variable compared to the default that won't. 
        This is because the CTkToolTip widget needs the widget to know where to be assigned
        """
        self.sidebarFrame = customtkinter.CTkFrame(self, width=140, height=1100, corner_radius=0)
        self.sidebarFrame.grid(row=0, column=0, sticky='nsew')

        # When loading the images, two are loaded. The first is the light mode and second is dark mode
        homeImage = customtkinter.CTkImage(Image.open('images/icons/lightMode/HomeIcon.png'),
                                           Image.open('images/icons/darkMode/HomeIconDarkMode.png'), (50, 50))
        self.homeButton = customtkinter.CTkButton(self.sidebarFrame, text='', command=self.HomeSelected,
                                                  image=homeImage,
                                                  fg_color="transparent")
        self.homeButton.grid(row=0, column=0, pady=(5, 67 / 2))
        CTkToolTip(self.homeButton, 'Home')

        goalsImage = customtkinter.CTkImage(Image.open('images/icons/lightMode/GoalsIcon.png'),
                                            Image.open('images/icons/darkMode/GoalsIconDarkMode.png'), (50, 50))
        self.goalsButton = customtkinter.CTkButton(self.sidebarFrame, text='', command=self.GoalsSelected,
                                                   image=goalsImage, fg_color='transparent')
        self.goalsButton.grid(row=1, column=0, pady=67 / 2)
        CTkToolTip(self.goalsButton, 'Goals')

        balanceIcon = customtkinter.CTkImage(Image.open('images/icons/lightMode/BalanceIcon.png'),
                                             Image.open('images/icons/darkMode/BalanceIconDarkMode.png'), (50, 50))
        self.balanceButton = customtkinter.CTkButton(self.sidebarFrame, text='', command=self.CashFlowSelected,
                                                     image=balanceIcon, fg_color='transparent')
        self.balanceButton.grid(row=2, column=0, pady=67 / 2)

        CTkToolTip(self.balanceButton, 'Balance')
        statsIcon = customtkinter.CTkImage(Image.open('images/icons/lightMode/StatsIcon.png'),
                                           Image.open('images/icons/darkMode/StatsIconDarkMode.png'), (50, 50))
        self.statsButton = customtkinter.CTkButton(self.sidebarFrame, text='', command=self.StatisticsSelected,
                                                   image=statsIcon, fg_color='transparent')
        self.statsButton.grid(row=3, column=0, pady=67 / 2)
        CTkToolTip(self.statsButton, 'Statistics')

        investmentsIcon = customtkinter.CTkImage(Image.open('images/icons/lightMode/InvestmentsIcon.png'),
                                                 Image.open('images/icons/darkMode/InvestmentsIconDarkMode.png'),
                                                 (50, 50))
        self.investmentsButton = customtkinter.CTkButton(self.sidebarFrame, text='', command=self.InvestmentsSelected,
                                                         image=investmentsIcon, fg_color='transparent')
        self.investmentsButton.grid(row=4, column=0, pady=67 / 2)
        CTkToolTip(self.investmentsButton, 'Investment Tracking')

        budgetIcon = customtkinter.CTkImage(Image.open('images/icons/lightMode/BudgetsIcon.png'),
                                            Image.open('images/icons/darkMode/BudgetsIconDarkMode.png'), (50, 50))
        self.budgetButton = customtkinter.CTkButton(self.sidebarFrame, text='', command=self.BudgetSelected,
                                                    image=budgetIcon, fg_color='transparent')
        self.budgetButton.grid(row=5, column=0, pady=(67 / 2, 5))
        CTkToolTip(self.budgetButton, 'Budgeting')

        # Configure Home Frame with all widgets needed
        self.homeFrame = customtkinter.CTkFrame(self)

        self.homeFrame.grid(row=0, column=1, padx=10, pady=10, sticky='news')
        self.nameLabel = customtkinter.CTkLabel(self.homeFrame, font=customtkinter.CTkFont(size=40),
                                                text='Welcome NAME')
        self.nameLabel.grid(row=0, column=0, columnspan=2, sticky='')
        customtkinter.CTkLabel(self.homeFrame, text="Today's overview").grid(row=1, column=0, padx=10, pady=(40, 10))
        self.balanceLabel = customtkinter.CTkLabel(self.homeFrame, text='Balance:\n$0000')
        self.balanceLabel.grid(row=2, column=0)
        self.nextGoalLabel = customtkinter.CTkLabel(self.homeFrame, text='Next Goal:\nGOAL')
        self.nextGoalLabel.grid(row=2, column=1)
        customtkinter.CTkOptionMenu(self.homeFrame, values=["System", "Light", "Dark"],
                                    command=self.ChangeAppearanceModeEvent).grid(row=6, column=1, padx=20,
                                                                                 pady=(10, 10))
        self.ChangeAppearanceModeEvent('System')
        customtkinter.CTkButton(self.homeFrame, command=self.LogOut, text='Log Out').grid(row=6, column=2)

        # Configure Goals Frame with all widgets needed
        self.goalsFrame = customtkinter.CTkFrame(self)
        self.goalsFrame.grid(row=0, column=1, padx=10, pady=10, sticky='news')
        customtkinter.CTkLabel(self.goalsFrame, font=customtkinter.CTkFont(size=40), text='Goals Board').grid(row=0,
                                                                                                              column=0,
                                                                                                              columnspan=3,
                                                                                                              pady=10)
        customtkinter.CTkLabel(self.goalsFrame, font=customtkinter.CTkFont(size=20), text='Goals List').grid(row=1,
                                                                                                             column=0,
                                                                                                             columnspan=4,
                                                                                                             pady=(
                                                                                                                 10, 0))

        # Treeview Customisation (theme colors are selected)
        bg_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])

        treeStyle = tkinter.ttk.Style()
        treeStyle.theme_use('default')
        treeStyle.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color,
                            borderwidth=0)
        treeStyle.map('Treeview', background=[('selected', bg_color)], foreground=[('selected', selected_color)])
        self.bind("<<TreeviewSelect>>", lambda event: self.focus_set())
        self.goalsTable = tkinter.ttk.Treeview(self.goalsFrame)  # configure  the goals table
        self.goalsTable['columns'] = ('Name', 'Description', 'Date', 'Money')
        self.goalsTable.column('#0', width=0, minwidth=0)
        self.goalsTable.column('Name', width=70, minwidth=25)
        self.goalsTable.column('Description', width=100, minwidth=25)
        self.goalsTable.column('Date', width=70, anchor='center', minwidth=25)
        self.goalsTable.column('Money', width=70, minwidth=25)
        self.goalsTable.heading('Name', text='Name')
        self.goalsTable.heading('Description', text='Description')
        self.goalsTable.heading('Date', text='Date')
        self.goalsTable.heading('Money', text='Money')
        self.goalsTable.grid(row=2, column=0, columnspan=4, padx=20, pady=20)

        self.goalSortBy = tkinter.IntVar(value=5)
        customtkinter.CTkRadioButton(self.goalsFrame, text='Date', width=70, command=self.SortGoals,
                                     variable=self.goalSortBy, value=0).grid(row=3, column=0)
        customtkinter.CTkRadioButton(self.goalsFrame, text='Money', width=70, command=self.SortGoals,
                                     variable=self.goalSortBy, value=1).grid(row=3, column=1)
        customtkinter.CTkRadioButton(self.goalsFrame, text='Name', width=70, command=self.SortGoals,
                                     variable=self.goalSortBy, value=2).grid(row=3, column=2)
        customtkinter.CTkRadioButton(self.goalsFrame, text='Default', width=70, command=self.SortGoals,
                                     variable=self.goalSortBy, value=3).grid(row=3, column=3)
        tkinter.ttk.Separator(self.goalsFrame, orient='vertical').grid(column=4, row=1, rowspan=3, sticky='ns')
        customtkinter.CTkLabel(self.goalsFrame, text='Add New').grid(row=1, column=5)
        self.newGoalEntryFrame = customtkinter.CTkFrame(self.goalsFrame)
        self.newGoalEntryFrame.grid(row=2, column=5)
        self.nameGoalEntry = customtkinter.CTkEntry(self.newGoalEntryFrame, placeholder_text='Name')
        self.nameGoalEntry.grid(row=0, column=0)
        self.dateGoalEntry = customtkinter.CTkEntry(self.newGoalEntryFrame, placeholder_text='Date "YY/MM/DD"')
        self.dateGoalEntry.grid(row=0, column=1)
        self.descriptionGoalEntry = customtkinter.CTkEntry(self.newGoalEntryFrame, placeholder_text='Description')
        self.descriptionGoalEntry.grid(row=1, column=0, columnspan=2)
        self.moneyGoalEntry = customtkinter.CTkEntry(self.newGoalEntryFrame, placeholder_text='Money')
        self.moneyGoalEntry.grid(row=3, column=0)
        customtkinter.CTkButton(self.goalsFrame, text='Create', command=self.AddNewGoal).grid(row=4, column=5)
        customtkinter.CTkButton(self.goalsFrame, text='Delete Selected', command=self.DeleteSelectedGoal).grid(row=4,
                                                                                                               column=3)

        # configure cash flow page
        self.transactionsFrame = customtkinter.CTkFrame(self)
        self.transactionsFrame.grid(row=0, column=1, padx=10, pady=10, sticky='news')
        customtkinter.CTkLabel(self.transactionsFrame, font=customtkinter.CTkFont(size=40), text='Cash Flow').grid(
            row=0, column=0, columnspan=3, rowspan=3)
        self.netCashLabel = customtkinter.CTkLabel(self.transactionsFrame, font=customtkinter.CTkFont(size=20))
        self.netCashLabel.grid(row=3, column=0, columnspan=4, sticky='w')

        customtkinter.CTkLabel(self.transactionsFrame, font=customtkinter.CTkFont(size=20), text='Add New').grid(row=0,
                                                                                                                 column=3,
                                                                                                                 columnspan=2)
        customtkinter.CTkButton(self.transactionsFrame, text='Add', command=self.AddNewTransaction).grid(row=1,
                                                                                                         column=3,
                                                                                                         rowspan=3)
        self.dateTransactionEntry = customtkinter.CTkEntry(self.transactionsFrame, placeholder_text='Date "YY/MM/DD"')
        self.dateTransactionEntry.grid(row=1, column=4)
        self.moneyTransactionEntry = customtkinter.CTkEntry(self.transactionsFrame, placeholder_text='Amount')
        self.moneyTransactionEntry.grid(row=2, column=4)
        self.descriptionTransactionEntry = customtkinter.CTkEntry(self.transactionsFrame,
                                                                  placeholder_text='Description')
        self.descriptionTransactionEntry.grid(row=3, column=4)

        tkinter.ttk.Separator(self.transactionsFrame, orient='horizontal').grid(column=0, row=4, columnspan=6,
                                                                                sticky='we')
        customtkinter.CTkLabel(self.transactionsFrame, font=customtkinter.CTkFont(size=20), text='Incomes').grid(row=5,
                                                                                                                 column=0)
        customtkinter.CTkLabel(self.transactionsFrame, font=customtkinter.CTkFont(size=20), text='Expenses').grid(row=5,
                                                                                                                  column=3)

        self.incomeLabel = customtkinter.CTkLabel(self.transactionsFrame, font=customtkinter.CTkFont(size=20), text='$')
        self.incomeLabel.grid(row=6, column=0)
        self.expenseLabel = customtkinter.CTkLabel(self.transactionsFrame, font=customtkinter.CTkFont(size=20),
                                                   text='$')
        self.expenseLabel.grid(row=6, column=3)

        self.incomeTable = tkinter.ttk.Treeview(self.transactionsFrame)
        self.incomeTable['columns'] = ('Date', 'Amount', 'Description')
        self.incomeTable.column('#0', width=0, minwidth=0)
        self.incomeTable.column('Date', width=70, minwidth=25)
        self.incomeTable.column('Description', width=100, minwidth=25)
        self.incomeTable.column('Amount', width=70, anchor='center', minwidth=25)
        self.incomeTable.heading('Date', text='Date')
        self.incomeTable.heading('Description', text='Description')
        self.incomeTable.heading('Amount', text='Amount')
        self.incomeTable.grid(row=7, column=0, columnspan=3, padx=20, pady=20)
        self.incomeVariable = tkinter.IntVar(value=2)
        customtkinter.CTkRadioButton(self.transactionsFrame, variable=self.incomeVariable, value=0,
                                     command=self.LoadTransactions, text='Date').grid(row=8, column=0)
        customtkinter.CTkRadioButton(self.transactionsFrame, variable=self.incomeVariable, value=1,
                                     command=self.LoadTransactions, text='Amount').grid(row=8, column=1)
        customtkinter.CTkButton(self.transactionsFrame, text='Delete Selected', command=self.DeleteSelectedIncome).grid(
            row=9, column=2)

        self.expenseTable = tkinter.ttk.Treeview(self.transactionsFrame)
        self.expenseTable['columns'] = ('Date', 'Amount', 'Description')
        self.expenseTable.column('#0', width=0, minwidth=0)
        self.expenseTable.column('Date', width=70, minwidth=25)
        self.expenseTable.column('Description', width=100, minwidth=25)
        self.expenseTable.column('Amount', width=70, anchor='center', minwidth=25)
        self.expenseTable.heading('Date', text='Date')
        self.expenseTable.heading('Description', text='Description')
        self.expenseTable.heading('Amount', text='Amount')
        self.expenseTable.grid(row=7, column=3, columnspan=3, padx=20, pady=20)
        self.expenseVariable = tkinter.IntVar(value=2)
        customtkinter.CTkRadioButton(self.transactionsFrame, variable=self.expenseVariable, value=0,
                                     command=self.LoadTransactions, text='Date').grid(row=8, column=3)
        customtkinter.CTkRadioButton(self.transactionsFrame, variable=self.expenseVariable, value=1,
                                     command=self.LoadTransactions, text='Amount').grid(row=8, column=4)
        customtkinter.CTkButton(self.transactionsFrame, text='Delete Selected',
                                command=self.DeleteSelectedExpense).grid(
            row=9, column=5)

        # configure statistics page
        self.statisticsFrame = customtkinter.CTkFrame(self)
        self.statisticsFrame.grid(row=0, column=1, padx=10, pady=10, sticky='news')
        customtkinter.CTkLabel(self.statisticsFrame, text='Statistics Page', font=customtkinter.CTkFont(size=20)).grid(
            row=0, column=0)

        self.transactionsPlot = CustomPlot(self.statisticsFrame, "Plot 1", "Date", "Amount")

        # configure investments page
        self.investmentsFrame = customtkinter.CTkFrame(self)
        self.investmentsFrame.grid(row=0, column=1, padx=10, pady=10, sticky='news')
        customtkinter.CTkLabel(self.investmentsFrame, text='Investments Page',
                               font=customtkinter.CTkFont(size=20)).grid(row=0, column=0)

        # configure budgets page
        self.budgetsFrame = customtkinter.CTkFrame(self)
        self.budgetsFrame.grid(row=0, column=1, padx=10, pady=10, sticky='news')
        customtkinter.CTkLabel(self.budgetsFrame, text='Budgets Page', font=customtkinter.CTkFont(size=20)).grid(row=0,
                                                                                                                 column=0)

        self.signInWindow: SignInPage = None
        self.LogOut()

    def HomeSelected(self):
        """
        Handles the event when the Home button is selected.
        Loads the Home frame and updates button states.
        :return:
        """
        self.LoadHome()
        self.homeFrame.tkraise()
        self.homeButton.configure(state='disabled', fg_color=('grey', '#494949'))
        self.goalsButton.configure(state='normal', fg_color='transparent')
        self.balanceButton.configure(state='normal', fg_color='transparent')
        self.statsButton.configure(state='normal', fg_color='transparent')
        self.investmentsButton.configure(state='normal', fg_color='transparent')
        self.budgetButton.configure(state='normal', fg_color='transparent')

    def LoadHome(self):
        """
        Loads the Home frame with user-specific data.
        Configures the welcome label and the next goal label.
        :return:
        """
        name = self.user.name
        self.nameLabel.configure(text=f'Welcome {name.title()}')
        self.LoadTransactions()  # we load transaction data here because it will change the balance label in it
        df = self.user.goals.copy()
        df['date'] = pd.to_datetime(df['date'], format='%y/%m/%d')
        today = pd.Timestamp(datetime.now().date())
        df = df[df['date'] >= today]
        df['difference'] = (df['date'] - today).abs()
        if not df.empty and not df['difference'].empty:
            closest_date_index = df['difference'].idxmin()
            closest_date = df.loc[closest_date_index, 'date'].date()
            self.nextGoalLabel.configure(text=f'Next Goal:\n{closest_date}')
        else:
            self.nextGoalLabel.configure(text=f'Next Goal:\nNONE')

    def GoalsSelected(self):
        """
        Handles the event when the Goals button is selected.
        Loads the Goals frame and updates button states.
        :return:
        """
        self.LoadGoals()
        self.goalsFrame.tkraise()
        self.homeButton.configure(state='normal', fg_color='transparent')
        self.goalsButton.configure(state='disabled', fg_color=('grey', '#494949'))
        self.balanceButton.configure(state='normal', fg_color='transparent')
        self.statsButton.configure(state='normal', fg_color='transparent')
        self.investmentsButton.configure(state='normal', fg_color='transparent')
        self.budgetButton.configure(state='normal', fg_color='transparent')

    def LoadGoals(self):
        """
        Loads the Goals frame with user-specific goals data.
        Clears existing data in the Treeview and inserts new goals.
        :return:
        """
        for i in self.goalsTable.get_children():
            self.goalsTable.delete(i)
        for index, row in self.user.goals.iterrows():
            self.goalsTable.insert('', 'end', iid=index,
                                   values=(row['name'], row['description'], row['date'], row['amount']))

    def CashFlowSelected(self):
        """
        Handles the event when the Cash Flow button is selected.
        Loads the Transactions frame and updates button states.
        :return:
        """
        self.expenseVariable.set(2)
        self.incomeVariable.set(2)
        self.LoadTransactions()
        self.transactionsFrame.tkraise()
        self.homeButton.configure(state='normal', fg_color='transparent')
        self.goalsButton.configure(state='normal', fg_color='transparent')
        self.balanceButton.configure(state='disabled', fg_color=('grey', '#494949'))
        self.statsButton.configure(state='normal', fg_color='transparent')
        self.investmentsButton.configure(state='normal', fg_color='transparent')
        self.budgetButton.configure(state='normal', fg_color='transparent')

    def StatisticsSelected(self):
        """
        Handles the event when the Statistics button is selected.
        Loads the Statistics frame and updates button states.
        :return:
        """
        self.LoadStatistics()
        self.statisticsFrame.tkraise()
        self.homeButton.configure(state='normal', fg_color='transparent')
        self.goalsButton.configure(state='normal', fg_color='transparent')
        self.balanceButton.configure(state='normal', fg_color='transparent')
        self.statsButton.configure(state='disabled', fg_color=('grey', '#494949'))
        self.investmentsButton.configure(state='normal', fg_color='transparent')
        self.budgetButton.configure(state='normal', fg_color='transparent')

    def LoadStatistics(self):
        """
        Loads the Statistics frame with updated cash flow data.
        :return:
        """
        self.UpdateCashFlowPlot()

    def InvestmentsSelected(self):
        """
        Handles the event when the Investments button is selected.
        Loads the Investments frame and updates button states.
        :return:
        """
        self.investmentsFrame.tkraise()
        self.homeButton.configure(state='normal', fg_color='transparent')
        self.goalsButton.configure(state='normal', fg_color='transparent')
        self.balanceButton.configure(state='normal', fg_color='transparent')
        self.statsButton.configure(state='normal', fg_color='transparent')
        self.investmentsButton.configure(state='disabled', fg_color=('grey', '#494949'))
        self.budgetButton.configure(state='normal', fg_color='transparent')

    def BudgetSelected(self):
        """
        Handles the event when the Budget button is selected.
        Loads the Budget frame and updates button states.
        :return:
        """
        self.budgetsFrame.tkraise()
        self.homeButton.configure(state='normal', fg_color='transparent')
        self.goalsButton.configure(state='normal', fg_color='transparent')
        self.balanceButton.configure(state='normal', fg_color='transparent')
        self.statsButton.configure(state='normal', fg_color='transparent')
        self.investmentsButton.configure(state='normal', fg_color='transparent')
        self.budgetButton.configure(state='disabled', fg_color=('grey', '#494949'))

    def LogOut(self):
        """
        Logs out the current user.
        Clears user data and opens the sign-in window.
        :return:
        """
        self.user.EmptyData()
        if self.signInWindow is None or not self.signInWindow.winfo_exists():
            self.signInWindow = SignInPage(self)
            self.withdraw()
        else:
            self.signInWindow.focus()

    def LogIn(self, username):
        """
        Logs in a user with the given username.
        Loads user data and displays the Home frame.
        :param username: The username of the user to log in.
        :return:
        """
        self.signInWindow.destroy()
        self.deiconify()
        self.user.LoadData(username)
        self.goalSortBy.set(3)
        self.HomeSelected()

    def ChangeAppearanceModeEvent(self, new_appearance_mode: str):
        """
        Changes the appearance mode of the application.
        :param new_appearance_mode: The new appearance mode to set.
        :return:
        """
        customtkinter.set_appearance_mode(new_appearance_mode)

    def AddNewGoal(self):
        """
        Adds a new goal for the user.
        Validates input and updates the goals list.
        :return:
        """
        passed = True
        name = self.nameGoalEntry.get().strip()
        date = self.dateGoalEntry.get().strip()
        description = self.descriptionGoalEntry.get().strip()
        money = self.moneyGoalEntry.get().strip()
        if name == '':
            passed = False
            self.nameGoalEntry.configure(border_color='Red')
        else:
            self.nameGoalEntry.configure(border_color='grey')
        if date == '' or not IsValidDate(date):
            passed = False
            self.dateGoalEntry.configure(border_color='red')
        else:
            self.dateGoalEntry.configure(border_color='grey')
        if not IsValidCurrency(money):
            passed = False
            self.moneyGoalEntry.configure(border_color='red')
        else:
            self.moneyGoalEntry.configure(border_color='grey')
        if not passed:
            return
        money = money.replace('$', '')
        DatabaseHandler.AddGoal(self.user.id, name, description, date, money)
        self.user.LoadGoalData()
        self.LoadGoals()

    def DeleteSelectedGoal(self):
        """
        Deletes the selected goal from the user's goals list.
        Updates the goals list after deletion.
        :return:
        """
        selected_item = self.goalsTable.selection()
        if selected_item:
            selected_iid = selected_item[0]
            goal_row = self.user.goals.loc[int(selected_iid)]
            goal_id = int(goal_row['id'])
            DatabaseHandler.DeleteGoal(goal_id)
            self.user.LoadGoalData()
            self.LoadGoals()

    def SortGoals(self):
        """
        Sorts the user's goals based on the selected sorting criterion.
        :return:
        """
        self.user.LoadGoalData()
        sortInt = self.goalSortBy.get()
        if sortInt == 3 or sortInt == 5:
            self.LoadGoals()
            return
        sortColumn = ''
        if sortInt == 0:
            sortColumn = 'date'
        elif sortInt == 1:
            sortColumn = 'amount'
        elif sortInt == 2:
            sortColumn = 'name'
        self.user.goals.sort_values(by=[sortColumn.lower()], inplace=True)
        self.LoadGoals()

    def AddNewTransaction(self):
        """
        Adds a new transaction for the user.
        Validates input and updates the transactions list.
        :return:
        """
        passed = True
        date = self.dateTransactionEntry.get().strip()
        description = self.descriptionTransactionEntry.get().strip()
        money = self.moneyTransactionEntry.get().strip()
        if date == '' or not IsValidDate(date):
            passed = False
            self.dateTransactionEntry.configure(border_color='red')
        else:
            self.dateTransactionEntry.configure(border_color='grey')
        if not IsValidCurrency(money, True):
            passed = False
            self.moneyTransactionEntry.configure(border_color='red')
        else:
            self.moneyTransactionEntry.configure(border_color='grey')
        if not passed:
            return
        money = money.replace('$', '')
        DatabaseHandler.AddTransaction(self.user.id, money, date, description)
        self.user.LoadTransactionData()
        self.LoadTransactions()

    def LoadTransactions(self):
        """
        Loads the user's transactions into the respective Treeviews.
        Clears existing data and inserts new transactions.
        :return:
        """
        for i in self.incomeTable.get_children():
            self.incomeTable.delete(i)
        for i in self.expenseTable.get_children():
            self.expenseTable.delete(i)
        self.incomeDf = self.user.transactions[self.user.transactions['amount'] > 0].copy()
        self.expenseDf = self.user.transactions[self.user.transactions['amount'] < 0].copy()
        if self.incomeVariable.get() == 0:
            self.incomeDf.sort_values(by=['date'], inplace=True)
        elif self.incomeVariable.get() == 1:
            self.incomeDf.sort_values(by=['amount'], inplace=True)
        if self.expenseVariable.get() == 0:
            self.expenseDf.sort_values(by=['date'], inplace=True)
        elif self.expenseVariable.get() == 1:
            self.expenseDf.sort_values(by=['amount'], inplace=True)
        for index, row in self.incomeDf.iterrows():
            self.incomeTable.insert('', 'end', iid=index, values=(row['date'], row['amount'], row['description']))
        for index, row in self.expenseDf.iterrows():
            self.expenseTable.insert('', 'end', iid=index, values=(row['date'], row['amount'], row['description']))
        totalIncome = self.incomeDf['amount'].sum()
        totalExpenses = self.expenseDf['amount'].sum()
        net_cash = totalIncome + totalExpenses
        self.incomeLabel.configure(text=f'${totalIncome:.2f}')
        self.expenseLabel.configure(text=f'${totalExpenses:.2f}')
        self.netCashLabel.configure(text=f"Net Cash: ${net_cash:.2f}")
        self.balanceLabel.configure(text=f'Balance:\n${net_cash:.2f}')

    def DeleteSelectedIncome(self):
        """
        Deletes the selected income transaction from the user's transactions list.
        Updates the transactions list after deletion.
        :return:
        """
        selected_item = self.incomeTable.selection()
        if selected_item:
            selected_iid = selected_item[0]
            incomeRow = self.incomeDf.loc[int(selected_iid)]
            incomeId = int(incomeRow['id'])
            DatabaseHandler.DeleteTransaction(incomeId)
            self.user.LoadTransactionData()
            self.LoadTransactions()

    def DeleteSelectedExpense(self):
        """
        Deletes the selected expense transaction from the user's transactions list.
        Updates the transactions list after deletion.
        :return:
        """
        selected_item = self.expenseTable.selection()
        if selected_item:
            selected_iid = selected_item[0]
            expenseRow = self.expenseDf.loc[int(selected_iid)]
            expenseId = int(expenseRow['id'])
            DatabaseHandler.DeleteTransaction(expenseId)
            self.user.LoadTransactionData()
            self.LoadTransactions()

    def UpdateCashFlowPlot(self):
        """
        Updates the cash flow plot with the user's transaction data.
        :return:
        """
        df = self.user.transactions.copy()
        df['date'] = pd.to_datetime(df['date'], format='%y/%m/%d')
        df.sort_values(by=['date'], inplace=True)
        total_over_time_df = df.groupby('date')[
            'amount'].sum().reset_index()  # Combine all the rows that have the same date and sum the amount
        total_over_time_df['cumulative_total'] = total_over_time_df['amount'].cumsum()  # Get the cumulative total
        self.transactionsPlot.UpdatePlot(total_over_time_df, 'date', 'cumulative_total')


def IsValidDate(dateString: str):
    """
    Validates if the provided date string is in the correct format.
    :param dateString: The date string to validate.
    :return: True if the date string is valid, False otherwise.
    """
    try:
        # Attempt to parse the date string
        datetime.strptime(dateString, '%y/%m/%d')
        return True
    except ValueError:
        # If a ValueError is raised, the date string is not valid
        return False


def IsValidCurrency(amountString: str, allowNegative: bool = False):
    """
    Validates if the provided currency string is in the correct format.
    :param amountString: The currency string to validate.
    :param allowNegative: Boolean to allow negative amounts.
    :return: True if the currency string is valid, False otherwise.
    """
    # Define a regex pattern for currency validation
    if allowNegative:
        pattern = re.compile(r'^-?\$?\d+(\.\d{2})?$')  # Has the -? matches an optional negative sign
    else:
        pattern = re.compile(r'^\$?\d+(\.\d{2})?$')
    # ^ and $ denote the start and end of the string, respectively.
    # \$? matches an optional dollar sign.
    # \d+ matches one or more digits.
    # (\.\d{2})? matches an optional decimal point followed by exactly two digits.

    # Match the pattern with the provided string
    if pattern.match(amountString):
        return True
    else:
        return False


app = MainPage()

app.mainloop()

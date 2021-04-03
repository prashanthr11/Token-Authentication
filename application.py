# Importing Modules and stuff

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from sqlite3 import *
from datetime import *

# Configure application
app = Flask(__name__)


# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to the database
cur = connect("Project.db")


# This the path for our homepage
@app.route("/", methods=["GET", "POST"])
def homepage():  # Returns the homepage(starting page)
    return render_template("homepage.html")


def verifyToken(token, now):
    """
    In this function, we are going to fetch all the users with the given tokenid. If there is only one user we just return true else false in all other cases.
    """
    try:
        rows = cur.execute("SELECT UserID FROM Users where UserID IN(SELECT UserID FROM Tokens where TokenID = ?)",
                           (token,))
        rows = rows.fetchall()
        if len(rows) == 1:
            return True
        if len(rows) > 1:
            render_template('error.html', message='More than one user with the same Token Id')
        return False
    except Error as e:
        render_template('error.html', message=f'{e}')
        return False


def getUsername(uid):
    """
    Query and return the DB for the username on basis of userid.
    """
    return cur.execute("SELECT Username FROM Users WHERE UserID = ?", (uid,))


def generateToken(timenow):
    """
    Utility function for adding time(Expiry).
    """
    return timenow + timedelta(days=30)  # The Token validity is assuming for 30 days


def storeToken(token, expirydate, uid):
    """
    Insert tokenid, userid, expirydate into the tokens table.
    """
    params = (token, uid, expirydate)
    cur.execute("INSERT INTO Tokens (TokenID, UserID, EXPIRYDATE) VALUES(?, ?, ?)", params)
    cur.commit()
    return token


def isvalidtoken(uid, token):
    """
    This function check for validity of the token. If Token is outdated return False else True
    """
    try:
        timenow = datetime.now().strftime("%m/%d/%Y, %H:%M:%S").replace(',', '')
        rows = cur.execute("SELECT EXPIRYDATE FROM Tokens where TokenID = ? AND UserID = ?", (token, uid))
        rows = rows.fetchall()
        for row in rows[0]:
            if row < timenow:  # comparison between string returns True if the Token is not expired else False.
                return False
        return True
    except Error as e:
        render_template('error.html', message=f'{e}')
        return False


def updateToken(token, uid):
    """
    Insert the data into the Tokens table.
    """
    try:
        rows = cur.execute("UPDATE Tokens SET EXPIRYDATE = ? WHERE TokenID = ? AND UserID = ?)",
                           (generateToken(datetime.now()), token, uid))
        cur.commit()
        return True
    except Error as e:
        render_template('error.html', message=f'{e}')
        return False


@app.route("/check", methods=["GET", "POST"])
def getUserDate():
    """
    It Supports both Post and Get requests.
    While the request is Get, We redirect to the homepage which asks the user to enter the Username, Userid and Token.
    On the otherhand, We take the inputs and check if the userid is already present in our database. If so, we check for his token expiry date.
    Else, we insert the details in our db (Both in users and tokens tables) and returns the token number.
    """
    if request.method == 'POST':
        User_ID, Token, name = request.form.get('User ID'), request.form.get('token'), request.form.get('name')
        presentTime = datetime.now()  # Time at present.
        if verifyToken(Token, presentTime):  # If User id is found in our DB.
            if isvalidtoken(User_ID, Token):
                user = getUsername(
                    User_ID).fetchall()  # Fetch the details(userid and username) of the user form users table.
                return render_template('error.html',
                                       message=f'Hello, {user[0]}!! Your Token is Not Expired Yet!')  # if token is not expired yet.
            else:
                updateToken(Token, User_ID)
                return render_template('error.html', message='Your Token is updated!')
        else:  # New User so Insert details of the user into the db
            try:
                params = (User_ID, name)
                cur.execute("INSERT INTO Users (UserID, Username) VALUES(?, ?)", params)  # If new user, insert into db.
                cur.commit()
                Expiry = generateToken(presentTime).strftime("%m/%d/%Y, %H:%M:%S").replace(',',
                                                                                           '')  # converting into string from datetime object for incompatability for storing the data in db.
                storeToken(Token, Expiry, User_ID)  # Insert the Expiry date and tokenid, userid in tokens table.
                return render_template('error.html',
                                       message=f'Hello, {name}!! Your Token is {Token}.')  # At last, return the token as the user is new user.
            except Error as e:  # If the enterd UserID is already exists.
                return render_template('error.html',
                                       message=f'UserID is already exists. Try changing with other UserID.')
    else:
        return render_template('homepage.html')  # This fires when the request is get itself.

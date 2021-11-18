import os
import sqlite3



def InitializeDB(dbFile='/shop.db'):
    connection = sqlite3.connect(os.getcwd() + dbFile)
    #create tables
    connection.execute('''CREATE TABLE IF NOT EXISTS User
    (fName           TEXT    NOT NULL,
     lName           TEXT    NOT NULL,
     username           TEXT    NOT NULL,
     password           TEXT    NOT NULL,
     creditCard           TEXT    NULL,
     shippingAddr           TEXT    NULL,
     billingAddr           TEXT    NULL,
     CONSTRAINT UC_User UNIQUE (fName, lName, username, password),
     UNIQUE(username));''')
    connection.execute('''CREATE TABLE IF NOT EXISTS Movie
     (serial         TEXT    NOT NULL,
     title           TEXT    NOT NULL,
     price           REAL    NOT NULL,
     rating          TEXT    NULL,
     genre           TEXT    NULL,
     quantity        INTEGER    NOT NULL,
     CONSTRAINT UC_Movie UNIQUE (serial, title, price, quantity));''')

    connection.execute('''CREATE TABLE IF NOT EXISTS Cart
     (userID     INTEGER    NOT NULL,
      ordered    INTEGER  DEFAULT 0  NOT NULL,
     FOREIGN KEY(userID) REFERENCES User(rowid));''')

    connection.execute('''CREATE TABLE IF NOT EXISTS CartItem
     (cartID     INTEGER    NOT NULL,
      movieID    INTEGER    NOT NULL,
      quantity   INTEGER    NOT NULL,
      FOREIGN KEY(movieID) REFERENCES Movie(rowid),
     FOREIGN KEY(cartID) REFERENCES Cart(rowid));''')

    
    return connection
    
InitializeDB()
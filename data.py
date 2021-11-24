import os
import sqlite3



def InitializeDB(dbFile='/shop.db'):
    connection = sqlite3.connect(os.getcwd() + dbFile)
    #create tables
    connection.execute('''CREATE TABLE IF NOT EXISTS Account
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
     CONSTRAINT UC_Movie UNIQUE (serial, title));''')

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

    try:
        connection.execute("INSERT INTO Movie VALUES ('197278', 'The Shawshank Redemption', 19.99, 'R', 'Drama', 75)")
        connection.execute("INSERT INTO Movie VALUES ('142389', 'The Godfather', 25.49, 'R', 'Crime, Drama', 45)")
        connection.execute("INSERT INTO Movie VALUES ('239847', 'Inception', 15.69, 'PG-13', 'Action, Adventure, Sci-Fi', 123)")
    except:
        pass
        

    return connection
    
InitializeDB()
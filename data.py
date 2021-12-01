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
      total    REAL  DEFAULT 0  NOT NULL,
     FOREIGN KEY(userID) REFERENCES User(rowid));''')

    connection.execute('''CREATE TABLE IF NOT EXISTS CartItem
     (cartID     INTEGER    NOT NULL,
      movieID    INTEGER    NOT NULL,
      title      TEXT       NOT NULL,
      quantity   INTEGER    NOT NULL,
      FOREIGN KEY(movieID) REFERENCES Movie(rowid),
     FOREIGN KEY(cartID) REFERENCES Cart(rowid));''')

    try:
        connection.execute("INSERT INTO Movie VALUES ('197278', 'The Shawshank Redemption', 19.99, 'R', 'Drama', 200)")
        connection.execute("INSERT INTO Movie VALUES ('142389', 'The Godfather', 24.99, 'R', 'Crime, Drama', 200)")
        connection.execute("INSERT INTO Movie VALUES ('239847', 'Inception', 14.99, 'PG-13', 'Action, Adventure, Sci-Fi',200)")
        connection.execute("INSERT INTO Movie VALUES ('927123', 'Goodfellas', 17.99, 'R', 'Crime', 200)")
        connection.execute("INSERT INTO Movie VALUES ('435915', 'No Time To Die', 14.99, 'PG-13', 'Action, Adventure, Comedy', 200)")
        connection.execute("INSERT INTO Movie VALUES ('716252', 'Halloween', 18.99, 'R', 'Horror, Thriller, Crime', 200)")
        connection.execute("INSERT INTO Movie VALUES ('502710', 'Us', 14.99, 'R', 'Horror, Mystery, Thriller', 200)")
        connection.execute("INSERT INTO Movie VALUES ('572567', 'Free Guy', 10.99, 'PG-13', 'Action, Adventure, Comedy', 200)")
        connection.execute("INSERT INTO Movie VALUES ('348941', 'Life', 9.99, 'R', ' Comedy, Crime, Drama', 200)")
        connection.execute("INSERT INTO Movie VALUES ('825674', 'King Richard', 19.99, 'Biography', 'Drama, Sport,', 200)")
        connection.execute("INSERT INTO Movie VALUES ('681086', 'Love and Basketball', 9.99, 'Romance', 'Drama, Sport,', 200)")
        connection.execute("INSERT INTO Account VALUES ('adam', 'test', 'adam', 'pass', '4455 4544 2324 4524', '210 Highway 12', '210 Highway 12')")
        connection.execute("INSERT INTO Account VALUES ('Ollie', 'Bland', 'OTB8', '1234', '1111 2222 3333 4444', '1900 School Blvd', '1900 School Blvd')")

    except:
        pass
        

    return connection
    
InitializeDB()

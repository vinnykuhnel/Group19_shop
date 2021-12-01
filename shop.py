import os
import sqlite3
from sqlite3.dbapi2 import Connection, Cursor, paramstyle
from dataclasses import dataclass
from typing import List
from data import InitializeDB

connection = InitializeDB()


@dataclass
class cartclass:
    def __init__(self, pk, userID, ordered, total):
        # primary key of cart id in db
        cartclass.pk = pk
        cartclass.userID = userID
        # 1 or 0 to represent ordered status
        cartclass.ordered = ordered
        cartclass.total = total


@dataclass
# represents an entry in the cart item database table
class cartitemclass:
    def __init__(self, pk, cartID, movieID, title, quantity):
        # primary key of DB entry
        self.pk = pk
        # cart the entry corresponds to
        self.cartID = cartID
        # movie referenced by cart entry
        self.movieID = movieID
        # title of movie
        self.title = title
        # quantity of movies
        self.quantity = quantity


@dataclass
class accountclass:
    def __init__(self, id, fName, lName, username, password, creditCard, shippingAddr, billingAddr):
        accountclass.id = id
        accountclass.fName = fName
        accountclass.lName = lName
        accountclass.username = username
        accountclass.password = password
        accountclass.creditCard = creditCard
        accountclass.shippingAddr = shippingAddr
        accountclass.billingAddr = billingAddr


@dataclass
class movieclass:
    def __init__(self, pk, serial, title, price, rating, genre, quantity):
        self.pk = pk
        self.serial = serial
        self.title = title
        self.price = price
        self.rating = rating
        self.genre = genre
        self.quantity = quantity


class inventory:
    def __init__(self):
        self.inventory: movieclass = []

    def UpdateInventoryList(self):
        self.inventory.clear()
        # SQL Query to get all avalable movies
        result = connection.execute("SELECT rowid, * FROM Movie").fetchall()
        for item in result:
            movie = movieclass(item[0], item[1], item[2], item[3], item[4], item[5], item[6])
            self.inventory.append(movie)

    def viewInventory(self):

        for item in self.inventory:
            print("Serial: " + item.serial)
            print("Title: " + item.title)
            print("Price: " + str(item.price))
            print("Rating: " + item.rating)
            print("Genre: " + item.genre)
            print("Quantity: " + str(item.quantity),"\n")

    def updateInventory(self, pk, quantity, remove=False):
        movie = None
        for item in self.inventory:
            if item.pk == pk:
                movie = item
                break

        if remove:
            # SQL statement to decrease item's quantity by quantity parameter
            tuple = (movie.quantity - quantity, movie.pk)
            queryStr = '''UPDATE Movie SET quantity = ? WHERE rowid=?'''
            connection.execute(queryStr, tuple)
            connection.commit()
            return (movie.price * quantity)
        else:
            # May not be needed, discuss with group
            # SQL statement to increase item's quantity by quantity parameter
            return 0

    def checkInventory(self, movieName, quantity):
        movieCheck = None
        for item in self.inventory:
            if item.title == movieName:
                movieCheck = item
        if movieCheck:
            if movieCheck.quantity >= quantity:
                return movieCheck.pk
        return 0

class cart:
    def __init__(self):
        self.entries: cartitemclass = []
        self.cart: cartclass = None

    def assignCart(self, userID):
        # check for a current non-ordered cart corresponding to user
        tuple = (userID, 0)
        queryStr = '''SELECT rowid, * FROM Cart WHERE userID=? AND ordered=?'''
        result = connection.execute(queryStr, tuple).fetchone()
        if result:
            self.cart = cartclass(result[0], result[1], result[2], result[3])

        else:

            self.newCart(userID)
        self.getItems()

    def newCart(self, userID):
        # create a new cart for certain user
        tuple = (userID, 0, 0)
        queryStr = '''INSERT INTO Cart VALUES (?, ?, ?)'''
        connection.execute(queryStr, tuple)
        connection.commit()
        result = connection.execute("SELECT last_insert_rowid();").fetchone()

        self.cart = cartclass(result[0], userID, 0, 0)

    def getItems(self):
        self.entries: cartitemclass = []
        # Add all entries in Cart Items table to list
        tuple = (self.cart.pk,)
        queryStr = '''SELECT rowid, * FROM CartItem WHERE cartID=?'''
        result = connection.execute(queryStr, tuple).fetchall()
        for item in result:
            self.entries.append(cartitemclass(item[0], item[1], item[2], item[3], item[4]))

    def viewCart(self):
        # display items in current cart
        print("\nItems in your Cart: ")
        for i in self.entries:
            print("Entry Num: " + str(i.pk) + " Title: " + i.title + " Quantity: " + str(i.quantity))
        print("\n")
    def addToCart(self, movieID, movieTitle, quantity):

        if movieID > 0:
            # SQL statement to add a entry in cart item table
            tuple = (self.cart.pk, movieID, movieTitle, quantity)
            queryStr = '''INSERT INTO CartItem VALUES (?, ?, ?, ?)'''
            connection.execute(queryStr, tuple)
            connection.commit()
            return True

        else:
            return False

    def removeFromCart(self, itemID):

        connection.execute("DELETE FROM CartItem WHERE rowid=?", (itemID,))
        connection.commit()

    def checkout(self, total):
        connection.execute('''UPDATE Cart SET ordered = 1, total = ? WHERE rowid=?''', (total, self.cart.pk))
        connection.commit()
        self.entries.clear()


class account():
    def __init__(self):
        self.account: accountclass = None

    def createAccount(self, fName, lName, username, password, creditCard, shippingAddr, billingAddr):
        # insert new account in db
        tuple = (fName, lName, username, password, creditCard, shippingAddr, billingAddr)
        queryStr = '''INSERT INTO Account VALUES (?, ?, ?, ?, ?, ?, ?)'''
        try:
            connection.execute(queryStr, tuple)
            connection.commit()
        except:
            pass

    def deleteAccount(self):
        connection.execute("DELETE FROM Account WHERE rowid=?", (self.account.id,))
        connection.commit()

    def editShippingInfo(self):
        newAddr = input(str("Enter your new Shipping Address: "))
        newBillingAddr = input(str("Enter your new Billing Address: "))
        tuple = (newAddr, newBillingAddr, self.account.id)
        connection.execute('''UPDATE Account SET shippingAddr = ?, billingAddr = ? WHERE rowid=?''', tuple)
        connection.commit()
        self.account.shippingAddr = newAddr
        self.account.billingAddr = newBillingAddr

        # SQL statement to update address in database

    def editPaymentInfo(self):
        newCard = input(str("Enter your new payment info: "))
        tuple = (newCard, self.account.id)
        connection.execute('''UPDATE Account SET creditCard = ? WHERE rowid=?''', tuple)
        connection.commit()
        self.account.creditCard = newCard

    def editPassword(self):
        newPassword = input(str("Enter your new Password: "))
        tuple = (newPassword, self.account.id)
        connection.execute('''UPDATE Account SET password = ? WHERE rowid=?''', tuple)
        connection.commit()
        self.account.password = newPassword

    def authenticate(usernameEntered, enteredPassword):
        # query for usernames record
        queryStr = '''SELECT rowid, * FROM Account WHERE username=?'''
        result = connection.execute(queryStr, (usernameEntered,)).fetchone()

        if result:
            if result[4] == enteredPassword:
                account = accountclass(result[0], result[1], result[2], result[3], result[4], result[5], result[6],
                                       result[7])
                return account
            else:
                return None


class orderHistory:
    def addToOrderHistory():
        # SQL statement to make a new cart
        # SQL statement to update current cart to new cart
        return 0

    def displayOrderHistory(self, userID):
        carts = connection.execute('''SELECT rowid, total FROM Cart WHERE userID=?''', (userID,)).fetchall()
        # SQL statement to retrieve all of the orders
        for item in carts:
            cart = connection.execute('''SELECT * FROM CartItem WHERE cartID=?''', (item[0],)).fetchall()
            for i in cart:
                print("Order #: " + str(i[0]) + " Title: " + i[2] + "  Quantity: " + str(i[3]))
            if cart:
                print("TOTAL: " + str(item[1]))


def parser(string, movies: inventory, orders: orderHistory, userCart: cart, user: account, session: bool):
    # Initialize or update the cart/inventory user will be working with
    userCart.assignCart(user.account.id)
    movies.UpdateInventoryList()

    # match typed command to action
    if string == "View items":
        movies.viewInventory()
    elif string == "View cart":
        userCart.viewCart()
    elif string == "Add cart item":

        movieName = input(str("Enter the title of the movie that you would like to add: "))
        quantity = int(input("Enter the number of copies of {} that you would like to purchase:  ".format(movieName)))

        if userCart.addToCart(movies.checkInventory(movieName, quantity), movieName, quantity):
            print("\nThe movie title '{}' was successfully added to cart with a quantity of {}!\n".format(movieName,quantity))
        else:
            print("\nError! You did not enter either a valid title or quantity. Please try again.\n")

    elif string == "Remove from cart":
        for i in self.entries:
            print("Entry Num: " + str(i.pk) + " Title: " + i.title + " Quantity: " + str(i.quantity))
        print("\n")
        cartID = input(str("\nEnter cart Num you would like to remove: "))
        userCart.removeFromCart(cartID)
    elif string == "Checkout":
        validCart = True
        total = 0
        for item in userCart.entries:
            if movies.checkInventory(item.title, item.quantity) > 0:
                continue
            else:
                validCart = False
        if validCart:
            for item in userCart.entries:
                # Update number in inventory
                total += movies.updateInventory(item.movieID, item.quantity, True)
            # change cart entry to ordered
            print("Checkout successful. The total of all movies in the cart was ", total, ".\n")
            userCart.checkout(total)
    elif string == "Add order to history":
        orders.addOrderHistory()
    elif string == "View order history":
        orders.displayOrderHistory(user.account.id)
        print("\n")
    elif string == "Edit account":
        user.editPassword()
        user.editPaymentInfo()
        user.editShippingInfo()
        print("\n")
    elif string == "Delete account":
        user.deleteAccount()
        session = False
    elif string == "Logout":
        session = False
    else:
        print("Error! You enter an invail command. Please try again.\n")
    return movies, orders, userCart, user, session


def main():
    while 1:
        movies = inventory()
        orders = orderHistory()
        userCart = cart()
        user: account = None

        print("Welcome to The Movie Shop!")
        while 1:
            loginChoice = input(str("Would you like to login or create an account? "))
            if loginChoice == 'login':
                username = input(str("Please enter your username: \n"))
                password = input(str("Please enter your password: \n"))

                acc: accountclass = account.authenticate(username, password)
                user = account()
                user.account = acc
                if user.account:
                    break
                else:
                    print("Error! The username and password combination does not exist. \nPlease try again or create an account. \n")
                    continue
            elif loginChoice == 'create an account':
                fName = input(str("Please enter your first name: "))
                lName = input(str("Please enter your last name: "))
                username = input(str("Please enter a new username: "))
                password = input(str("Please enter a password: "))
                creditCard = input(str("Please enter your credit/debit card number: "))
                shippingAddr = input(str("Please enter your Shipping Address: "))
                billingAddr = input(str("Please enter your Billing Addrress: "))
                user = account()
                user.createAccount(fName, lName, username, password, creditCard, shippingAddr, billingAddr)
                continue
            else:
                continue
        session = True
        print("\nAuthentication and login were successful. \n")
        while session:
            print(
                "MENU OPTIONS => \n View items \n View cart \n Add cart item \n Remove from cart \n Checkout \n View order history \n Edit account \n Delete account \n Logout \n")
            command = input(str("Please enter a command from the above list to  perform: "))
            movies, orders, userCart, user, session = parser(command, movies, orders, userCart, user, session)


if __name__ == "__main__":
    main()
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
        #primary key of cart id in db
        cartclass.pk = pk
        cartclass.userID = userID
        #1 or 0 to represent ordered status
        cartclass.ordered = ordered
        cartclass.total = total

@dataclass
#represents an entry in the cart item database table
class cartitemclass:
    def __init__(self, pk, cartID, movieID, title, quantity):
        #primary key of DB entry
        self.pk = pk
        #cart the entry corresponds to
        self.cartID = cartID
        #movie referenced by cart entry
        self.movieID = movieID
        #title of movie
        self.title = title
        #quantity of movies
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
        #SQL Query to get all avalable movies
        result = connection.execute("SELECT rowid, * FROM Movie").fetchall()
        for item in result:
            movie = movieclass(item[0], item[1], item[2], item[3], item[4], item[5], item[6])
            self.inventory.append(movie)        

    def viewInventory(self):
                
        for item in self.inventory:
            print("\n")
            print ("Serial: " + item.serial)
            print("Title: " + item.title)
            print("Price: " + str(item.price))
            print("Rating: " + item.rating)
            print("Genre: " + item.genre)
            print("Quantity: " + str(item.quantity))
            print("\n")

    def updateInventory(self, pk, quantity, remove = False):
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
            #May not be needed, discuss with group
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
        #check for a current non-ordered cart corresponding to user
        tuple = (userID, 0)
        queryStr = '''SELECT rowid, * FROM Cart WHERE userID=? AND ordered=?'''
        result = connection.execute(queryStr, tuple).fetchone()
        if result:                        
            self.cart = cartclass(result[0], result[1], result[2], result[3])
            
        else:
            
            self.newCart(userID)
        self.getItems()

    
    def newCart(self, userID):
        #create a new cart for certain user
        tuple = (userID, 0, 0)
        queryStr = '''INSERT INTO Cart VALUES (?, ?, ?)'''
        connection.execute(queryStr, tuple)
        connection.commit()
        result = connection.execute("SELECT last_insert_rowid();").fetchone()
        
        self.cart = cartclass(result[0], userID, 0, 0)
    
    def getItems(self):
        self.entries: cartitemclass = []
        #Add all entries in Cart Items table to list
        tuple = (self.cart.pk,)
        queryStr = '''SELECT rowid, * FROM CartItem WHERE cartID=?'''
        result = connection.execute(queryStr, tuple).fetchall()
        for item in result:
            self.entries.append(cartitemclass(item[0], item[1], item[2], item[3], item[4]))        
    
    def viewCart(self):
        #display items in current cart
        print("Items in your Cart: ")
        for i in self.entries:
            print ("Entry Num: " + str(i.pk) + " Title: " + i.title + " Quantity: " + str(i.quantity))

    def addToCart(self, movieID, movieTitle, quantity):             
        
        if movieID > 0:
            #SQL statement to add a entry in cart item table
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
        #insert new account in db
        tuple = (fName, lName, username, password, creditCard, shippingAddr, billingAddr)
        queryStr = '''INSERT INTO Account VALUES (?, ?, ?, ?, ?, ?, ?)'''
        try:
            connection.execute(queryStr, tuple)
            connection.commit()
        except:
            pass
        

    def editShippingInfo(self, newAddress):
        self.address = newAddress
        # SQL statement to update address in database

    def editPaymentInfo(self, newPayment):
        self.payment = newPayment

    def editPassword(self, newPassword):
        self.password = newPassword

    def authenticate(usernameEntered, enteredPassword):
        #query for usernames record
        queryStr = '''SELECT rowid, * FROM Account WHERE username=?'''
        result = connection.execute(queryStr, (usernameEntered,)).fetchone()
        
        if result:    
            if result[4] == enteredPassword:
                account = accountclass(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
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
        #Initialize or update the cart/inventory user will be working with
        userCart.assignCart(user.account.id)
        movies.UpdateInventoryList()
        

        #match typed command to action
        if string == "view items":
            movies.viewInventory()
        elif string == "view cart":
            userCart.viewCart()
        elif string == "add cart item":
            
            movieName = input(str("Enter the name of the movie: "))
            quantity = int(input("Enter the number of copies: "))
            
            if userCart.addToCart(movies.checkInventory(movieName, quantity), movieName, quantity):
                print("Item was Successfilly added to cart!")
            else:
                print("Enter a valid title and quantity!")
                
        elif string == "remove from cart":
            cartID = input(str("Enter cart Num you would like to remove: "))
            userCart.removeFromCart(cartID)
        elif string ==  "checkout":
            validCart = True
            total = 0
            for item in userCart.entries:
                if movies.checkInventory(item.title, item.quantity) > 0:
                    continue
                else:
                    validCart = False
            if validCart:
                for item in userCart.entries:
                    #Update number in inventory
                    total += movies.updateInventory(item.movieID, item.quantity, True)
                #change cart entry to ordered
                print(total)
                userCart.checkout(total)
        elif string ==  "add order to history":
            orders.addOrderHistory()
        elif string == "view order history":
            orders.displayOrderHistory(user.account.id)
        elif string == "edit account":
            user.editPassword()
            user.editPaymentInfo()
            user.editShippingInfo()
        elif string ==  "delete account":
            user.deleteAccount()
        elif string ==  "logout":
            session = False
        else:
            print("Error: Command invalid")
        return movies, orders, userCart, user, session
    
def main():   
    
    while 1:
        movies = inventory()
        orders = orderHistory()
        userCart = cart()
        user: account = None


        print("Welcome")
        while 1:
            loginChoice = input(str("login or create account? "))
            if loginChoice == 'login':
                username = input(str("Username: "))            
                password = input(str("Password: "))

                acc: accountclass = account.authenticate(username, password)
                user = account()
                user.account = acc
                if user.account:
                    break
                else:
                    print("Error: Username and password is incorrect")
                    continue
            elif loginChoice == 'create account':
                fName = input(str("Enter your first name: "))
                lName = input(str("Enter your last name "))
                username = input(str("Enter New Username: "))
                password = input(str("Enter Password: "))
                creditCard = input(str("Enter card number: "))
                shippingAddr = input(str("Enter your Shipping Address: "))
                billingAddr = input(str("Enter your Billing Addrress: "))
                user = account()
                user.createAccount(fName, lName, username, password, creditCard, shippingAddr, billingAddr)
                continue
            else:
                continue
        session = True        
        print("Authentication successful: ")
        while session:
            print("Options => view items, view cart, add cart item, remove from cart, checkout, view order history, edit account, delete account, logout")
            command = input(str("Enter one of the commands above: "))
            movies, orders, userCart, user, session = parser(command, movies, orders, userCart, user, session)


if __name__=="__main__":
    
    
    main()
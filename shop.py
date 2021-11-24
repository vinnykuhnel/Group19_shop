import os
import sqlite3
from sqlite3.dbapi2 import Connection, Cursor, paramstyle
from dataclasses import dataclass
from typing import List
from data import InitializeDB

connection = InitializeDB()

@dataclass
class cartclass:
    def __init__(self, pk, userID, ordered):
        #primary key of cart id in db
        cartclass.pk = pk
        cartclass.userID = userID
        #1 or 0 to represent ordered status
        cartclass.ordered = ordered

@dataclass
class cartitemclass:
    def __init__(self, pk, cartID, movieID, quantity):
        #primary key of DB entry
        self.pk = pk
        #cart the entry corresponds to
        self.cartID = cartID
        #movie referenced by cart entry
        self.movieID = movieID
        #quantity of movies

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
        #SQL Query to get all avalable movies
        self.inventory = []
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

    def updateInventory(item, remove = True):
        if remove:
            # SQL statement to decrease item's quantity by quantity parameter
            # Add error checking to make sure the do not decrease past 0 quantity
            return 0
        else:
            # SQL statement to increase item's quantity by quantity parameter
            return 0
    
    def checkInventory(item, quantity):
        # SQL statement to make sure the item has enough inventory
        return 0



class cart:
    def __init__(self):
        self.entries: cartitemclass = []
        self.cart: cartclass = None
    
    def viewCart(self):
        for i in self.itemlist:
            print (i)

    def addToCart(self, item, quantity, inventoryObject):
        # SQL statement to pull item info
        id = 0
        temp = cartclass(id, item, quantity) 
        if any(i.name == temp.name for i in self.itemlist):
            return
            
        if inventoryObject.checkInventory(item, quantity):

            self.itemlist.append(item)
            # SQL statement to update cart in database
        else:
            print("Error")
        

    def removeFromCart(self, item):
        self.itemlist.remove(item)
        # SQL statement to remove item from cart

    def checkout(self, inventoryObject):
        for i in self.itemlist:
            inventoryObject.checkInventory(i)
        self.itemlist.clear()
        inventory.addToOrderHistory()
        


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

    def displayOrderHistory():
        # SQL statement to retrieve all of the orders
        order = []
        for i in order:
            print (i)







def parser(string, movies: inventory, orders: orderHistory, userCart: cart, user: account):
    
        if string == "view items":
            movies.viewInventory()
        elif string == "view cart":
            userCart.viewCart()
        elif string == "add items":
            movies.addItems()
        elif string == "remove from cart":
            userCart.removeFromCart()
        elif string ==  "checkout":
            cart.checkout()
        elif string ==  "add order to history":
            orders.addOrderHistory()
        elif string == "view order history":
            orders.viewOrderHistory()
        elif string == "edit account":
            user.editAccount()
        elif string ==  "delete account":
            user.deleteAccount()
        elif string ==  "logout":
            user.logout()
        else:
            print("Error: Command invalid")
        return movies, orders, userCart, user
    
def main(user):
    movies = inventory()
    orders = orderHistory()
    userCart = cart()
    print("Welcome")
    while 1:
        loginChoice = input(str("login or create account? "))
        if loginChoice == 'login':
            username = input(str("Username: "))            
            password = input(str("Password: "))
            
            acc: accountclass = account.authenticate(username, password)
            user = account()
            user.account = acc
            if user:
                break
            else:
                print("Error: Username and password do not match")
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

    print("Authentication successful: ")
    while 1:
        command = input(str("Enter command:"))
        movies, orders, userCart, user = parser(command, movies, orders, userCart, user)


if __name__=="__main__":
    user: account = None
    
    main(user)
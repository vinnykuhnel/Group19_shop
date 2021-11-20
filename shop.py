import os
import sqlite3
from sqlite3.dbapi2 import Connection, Cursor, paramstyle
from dataclasses import dataclass
from data import InitializeDB

connection = InitializeDB()

@dataclass
class itemclass:
    def __init__(self, id, name, quantity):
        itemclass.id = id
        itemclass.name = name
        itemclass.quantity = quantity

@dataclass
class accountclass:
    def __init__(self, fName, lName, username, password, creditCard, shippingAddr, billingAddr):
        itemclass.fName = fName
        itemclass.lName = lName
        itemclass.username = username
        itemclass.password = password
        itemclass.creditCard = creditCard
        itemclass.shippingAddr = shippingAddr
        itemclass.billingAddr = billingAddr


class inventory:
    def viewInventory(category):
        # SQL statement to retrieve all of the items in the given category
        inventory = []
        for i in inventory:
            print (i)

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
        self.itemlist = []
    
    def viewCart(self):
        for i in self.itemlist:
            print (i)

    def addToCart(self, item, quantity, inventoryObject):
        # SQL statement to pull item info
        id = 0
        temp = itemclass(id, item, quantity) 
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
    def __init__(self, fName, lName, username, password, creditCard, shippingAddr, billingAddr):
        self.account = accountclass(fName, lName, username, password, creditCard, shippingAddr, billingAddr)
        #insert new account in db
        tuple = (fName, lName, username, password, creditCard, shippingAddr, billingAddr)
        queryStr = '''INSERT INTO Account VALUES (?, ?, ?, ?, ?, ?, ?)'''
        connection.execute(queryStr, tuple)
        connection.commit()

    def editShippingInfo(self, newAddress):
        self.address = newAddress
        # SQL statement to update address in database

    def editPaymentInfo(self, newPayment):
        self.payment = newPayment

    def editPassword(self, newPassword):
        self.password = newPassword

    def authenticate(usernameEntered, enteredPassword):
        #query for usernames record
        queryStr = '''SELECT * FROM Account WHERE username=?'''
        result = connection.execute(queryStr, (usernameEntered,)).fetchone()
        
        if result:    
            if result[3] == enteredPassword:
                return accountclass(result[0], result[1], result[2], result[3], result[4], result[5], result[6])
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







#def parser(string):
#    match string:
#            case ("view items"):
#                return viewItems()
#            case ("view cart"):
#                return viewCart()
#            case ("add items"):
#                return addItems()
#            case("remove from cart"):
#                return removeFromCart()
#            case ("checkout"):
#                return checkout()
#            case ("add order to history"):
#                return addOrderHistory()
#            case ("view order history"):
#                return viewOrderHistory()
#            case ("edit account"):
#                return editAccount()
#            case ("delete account"):
#                return deleteAccount()
#            case ("logout"):
#                return logout()
#            case _:
#                print("Error: Command invalid")
#                return -1

    


def main(user):
    
    
    print("Welcome")
    while 1:
        loginChoice = input(str("login or create account? "))
        if loginChoice == 'login':
            username = input(str("Username: "))            
            password = input(str("Password: "))
            user = account.authenticate(username, password)
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
            user = account(fName, lName, username, password, creditCard, shippingAddr, billingAddr)
            continue
        else:
            continue

    print("Authentication successful: ")
#    while 1:
#        command = input(str("Enter command:"))
#        parser(command)


if __name__=="__main__":
    user: accountclass = None
    main(user)
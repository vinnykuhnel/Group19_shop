import os
import sqlite3
from sqlite3.dbapi2 import Cursor, paramstyle
from dataclasses import dataclass
from data import InitializeDB



@dataclass
class itemclass:
    def __init__(self, id, name, quantity):
        itemclass.id = id
        itemclass.name = name
        itemclass.quantity = quantity


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
        


class account:
    def __init__(self, username, address, payment):
        self.username = username
        self.address = address
        self.payment = payment

    def editShippingInfo(self, newAddress):
        self.address = newAddress
        # SQL statement to update address in database

    def editPaymentInfo(self, newPayment):
        self.payment = newPayment



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







def parser(string):
    match string:
            case ("view items"):
                return viewItems()
            case ("view cart"):
                return viewCart()
            case ("add items"):
                return addItems()
            case("remove from cart"):
                return removeFromCart()
            case ("checkout"):
                return checkout()
            case ("add order to history"):
                return addOrderHistory()
            case ("view order history"):
                return viewOrderHistory()
            case ("edit account"):
                return editAccount()
            case ("delete account"):
                return deleteAccount()
            case ("logout"):
                return logout()
            case _:
                print("Error: Command invalid")
                return -1

    


def main():
    cursor = InitializeDB()
    print("Welcome")
    while 1:
        username = input(str("Username: "))
        password = input(str("Password: "))
        if username == password:
            break
        else:
            print("Error: Username and password do not match")
    while 1:
        command = input(str("Enter command:"))
        parser(command)

if __name__=="__main":
    main()
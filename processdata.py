# Caden Weiner
# Data Mining Final Project
# 4/1/2021
import pandas as pd
import csv
import sys
from apyori import apriori
import matplotlib.pyplot as plt
# these are some helper functions I implemented but I don't think that I 
# actually used them they were more for testing 

# These are some functions to make it easier to process the data that we need
def look_up_order(orderdf, order_id):     
    return orderdf[orderdf["order_id"] == order_id]
    
def get_product_name(productdf,product_id): 
    productdf = productdf[productdf["product_id"] == product_id]
    return "".join(productdf["product_name"].values) # turn int id into a string

def print_products(productsdf, orderdf): 
    products = orderdf["product_id"]
    for product in products:
        print(get_product_name(productsdf, product))

def give_users_order_list(ordersdf, user_id): 
    users_orders = ordersdf[ordersdf["user_id"]==user_id] #fiter out order to only contain those matching user id
    return users_orders["order_id"].values

def print_orderlist(order_list): 
    for order in order_list: 
        print(order)

def numberof_orders(order_list): 
    return len(order_list)

def getall_users(ordersdf): 
    return set(ordersdf["user_id"].values) # we want to change it to a set as we only want the unique user ids, as each user can appear in multiple orders
        
def perform_operation_onall_users_orders_file(ordersdf, users, function, file): # also takes in a function that expects the imput of an orders data frame
    ostdout = sys.stdout
    with open(file, 'w') as ourfile: 
        sys.stdout = ourfile    
        #print("user_id,number_orders")
        for user in users: # this is kindof slow, I think it would be better to try and figure out some inbuilt functions to use
            user_orders = ordersdf[ordersdf["user_id"]==user]
            print("{}".format(function(user_orders))) # this will be changed to run apriori in subsequent versions on each individual user's data
        sys.stdout = ostdout
        ourfile.close()

#python3 marketbasketmain.py
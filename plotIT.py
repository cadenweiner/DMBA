import pandas as pd
import csv
import sys
from apyori import apriori
import matplotlib.pyplot as plt



def read_graph_order_size_frequencies(): 
    with open("marketdata/numberofusersbaskets.csv") as user_orders:# running on actual data
        sizes = user_orders.readlines() # now it is a list of baskets
        frequency_dict = {}
        for size in sizes: 
            if frequency_dict.get(size.strip()) != None: 
                frequency_dict[size.strip()] += 1
            else: 
                frequency_dict[size.strip()] = 1
    #print(frequency_dict)
    #plt.plot(frequency_dict.values(), frequency_dict.keys())
    # creates a bar graph
    plt.bar(list(frequency_dict.keys()),list(frequency_dict.values()),color ='maroon', width = .6)
    plt.xlabel("Order Size")
    plt.ylabel("Number of Users With This Size of Order")  
    plt.title("Graph of Order Size Frequencies")
    ax = plt.gca() # this plotting is being a bit weird with the labels, I may just place the labels manually through some type of photoshop tool 
    for label in ax.get_xaxis().get_ticklabels()[::2]:
        label.set_visible(False)
    plt.show()
    return frequency_dict

def createorders(ordersdf, file): # also takes in a function that expects the imput of an orders data frame
    ostdout = sys.stdout
    with open(file, 'w') as ourfile: 
        sys.stdout = ourfile    
        # write users id and the orders associated with it        
        for v in set(ordersdf["order_id"].values): 
            print(v)
        sys.stdout = ostdout
        ourfile.close()

def uniqueusers(ordersdf, file): # also takes in a function that expects the imput of an orders data frame
    ostdout = sys.stdout
    with open(file, 'w') as ourfile: 
        sys.stdout = ourfile    
        # write users id and the orders associated with it
        for v in set(ordersdf["user_id"].values): 
            print(v)
        sys.stdout = ostdout
        ourfile.close()
    return set(ordersdf["user_id"].values)


def run_plots(order_info, order_data, itemfrequencies): 
    #order_id,user_id,eval_set,order_number,order_dow,
    #order_hour_of_day,days_since_prior_order
    read_graph_order_size_frequencies()
    plotbyhour(order_info)
    plotbydateofweek(order_info)
    #plotdayssincepriororder(order_info) # decided not to use that as the info wasn't super helpful


def plotbyhour(order_info): 
    print("Plot by hour")
    translationdict = {'01':1, '02':2,'03':3, '04':4, '05':5, '06':6, '07':7, '08':8, '09':9} # strip the zeros from the front of the data
    order_info['order_hour_of_day'] = order_info.order_hour_of_day.map(lambda x: translationdict.get(x, x)) # using the map function built in to pandas
    #print(order_info)
    frequency_dict = {}
    for hour in order_info['order_hour_of_day']: 
        frequency_dict[hour] = frequency_dict.get(hour, 0) + 1 # if the day is not already in the dict set it to a count of zero initially then increment it to one, otherwise just increment by 1
    print(frequency_dict)
    # creates a bar graph
    plt.bar(list(frequency_dict.keys()),list(frequency_dict.values()),color = 'maroon', width = .4)
    plt.xlabel("Hour Of Day")
    plt.ylabel("Number of Orders at this time")  
    plt.title("Graph of Frequent Order Times")
    plt.show()

def plotbydateofweek(order_info): 
    print("Plot by Date Of week")
    frequency_dict = {}
    for day in order_info['order_dow']:
        frequency_dict[day] = frequency_dict.get(day, 0) + 1 # if the day is not already in the dict set it to a count of zero initially then increment it to one, otherwise just increment by 1

    #print(frequency_dict)
    # creates a bar graph
    plt.bar(list(frequency_dict.keys()),list(frequency_dict.values()),color = 'maroon', width = .4)
    plt.xlabel("Day of week")
    plt.ylabel("Number of Orders on this Day")  
    plt.title("Graph of Frequent Days")
    plt.show()

def plotdayssincepriororder(order_info): 
    print("Plot Time Since Prior Order")
    frequency_dict = {}
    for day in order_info['days_since_prior_order']: 
        frequency_dict[day] = frequency_dict.get(day, 0) + 1 # if the day is not already in the dict set it to a count of zero initially then increment it to one, otherwise just increment by 1
    #print(frequency_dict)
    # creates a bar graph
    plt.bar(list(frequency_dict.keys()),list(frequency_dict.values()),color = 'maroon', width = .4)
    plt.xlabel("Days Since Last order")
    plt.ylabel("Length of this size of Orders")  
    plt.title("Graph of Common Durations Between Orders")
    plt.show()
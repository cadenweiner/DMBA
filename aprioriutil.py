# Caden Weiner
# Data Mining Final Project
# 4/1/2021
import pandas as pd
import sys
from apyori import apriori

#from mlxtend.frequent_patterns import apriori
import random

# this algorithm is not as important for the results, 
# look at apriorimltx for my main apriori function

def generate_baskets_for_humans(orderdf): # we are probably going to want to limit the size of our baskets
    orderbaskets = []
    for order in set(orderdf['order_id']): 
        orderbaskets.append([item for item in orderdf[orderdf['order_id'] == order]['product_name']])# list compression        
    return orderbaskets
    # this was my initial list comprehension, it was "MUCH" slower
    #orderbaskets.append(["".join(set(orderdf.loc[(orderdf['order_id']==order) & (orderdf['product_name']==item)]['product_name'].values)) for item in set(orderdf[orderdf['order_id'] == order]['product_name'])])# list compression
    # faster version, we already verified the item in the order so we can skip the step we perform during list comprehensio
    # this way is much faster for creating our baskets
def generate_baskets(orderdf): 
    orderbaskets = []
    for order in set(orderdf['order_id']): 
        orderbaskets.append([str(item) for item in orderdf[orderdf['order_id'] == order]['product_id']])# list compression        
    return orderbaskets
# I am not currently using this function
def storebaskets(baskets, file): # printing the names to the files iosn't working great so I will just be printing ids. It seems to be an encoding issue, but I can't get it to work the way I need to based off of my searches online
    ostdout = sys.stdout
    with open(file, 'w', encoding="utf-8") as ourfile: # got encodiing to work!!!
        sys.stdout = ourfile    
        # write users id and the orders associated with it
        for basket in baskets: 
            print(",".join(basket))
        sys.stdout = ostdout
        ourfile.close()
# reused from homework 1
def read_stored_baskets(file): # by reading in our already arranged baskets it will be slightly quicker than creating the baskets everytime? 
    # we know all basketsizes are less than or equal 100 based off of our analysis, however the median order size is less than that
    basketlist = [] 
    #with open("confidence-check.txt") as items: # testing confidences
    #with open("browsingdata_50baskets.txt") as items: #testing counting of pairs and triples
    with open(file) as items:# running on actual data
        baskets = items.readlines() # now it is a list of baskets
        for basket in baskets: 
            basketlist.append(basket.split())#creates a list of the baskets filtered by spaces into the individual items for analysis
    return basketlist




# could use numpy, but better off using lists since small basket sizes

def calculateitemfrequencies(productdf, orderdf): # not super fast so I don't think I ended up calling
    frequencies = productdf.copy()# initialy planned to do this to make the data more sparse to run quicker but it was not needed
    tlist = [(len(orderdf[orderdf['product_id']==product]) / len(orderdf.product_id)) for product in productdf['product_id']]
    frequencies['frequencies'] = tlist
    print(frequencies)
    orderdf['frequencies'] = orderdf.product_id.map(lambda x: frequencies[frequencies['product_id']==x].frequencies.values[0]) # data frame has a builtin map function
    orderdf = orderdf[orderdf['frequencies'] >= .001] # we only care about the items that appear in at least 1 % of the baskets
    return frequencies, orderdf

    #  frequencies = product_info.copy()
    # print(product_info)
    # tlist = [] 
    # for product in product_info['product_id']: 
    #     tlist.append(len(order_train_info[order_train_info['product_id']==product]) / len(order_train_info.product_id)) ) 
    # frequencies['frequencies'] = tlist
    # print(frequencies)

def apriori_forall(recordlist,support): 
    # by decreasing lift, the number of rules accepted increases, by decreasing min support num rules increases
    apriori_results = apriori(recordlist, min_support=support, min_confidence=0.1, min_lift=1, max_length=6, verbose = 1) # we need our support to be really small since there are so many item combinations and so many orders
    print(list(apriori_results))
    return apriori_results
    # NOTES on parameter choice
    ######################################################################################
    # we want minsupport to be low enough to get items, but we have too many items with less relevant info on reordering rates. We want items with the top support frequencies
    # there are so many items and so much variety that for the whole data set I think it is probably a good idea to do only .5%
    # min_confidence filters out the confidences that are less than a certain threshold
    # lift metric is shown in the report
    # min support needs to be at least a certain value
    ######################################################################################


def apriori_forone(recordlist): # a user tends to have 10 baskets so we want it to appear in at least 3 so .3 or 30 %. This is because in such a small cart this will give 
    # by decreasing lift, the number of rules accepted increases, by decreasing min support num rules increases
    # print(recordlist)
    # If the threshold is too small it will do it for the whole basket basically and create many baskets that aren't informative since all will pass the support
    # I'm going with a min support of 30%
    # I also decided to increase the confidence to 60% to filter out better results
    # because most people only have 1 - 10 orders give or take, we need a bit higher threshold or else we will recommend items they only purchased once
    
    # may want to transition to the mlxtend tool for apriori
    apriori_results = apriori(recordlist, min_support=0.1, min_confidence=0.5, min_lift=1, max_length=5) # sets of atleast two items # min lift 2, we want items to be more highly related and dependent on each other 
    #print(apriori_results) # generator object
    results = list(apriori_results)
    # print(results[0])
    # print(results[1])
    # print(results[2])
    # print(results[3])
    # print(results[4])
    # print(results[5])
    # will be transitioning to doing this with mlxtend because that seems to be more visually appealling 

    

    # must appear in 1 % of baskets at least//support threshold s, a percentage of the baskets it will appear in
    return results# keep lift as 1 here since smaller basket size just in case to keep more usable results, may need to be increased after testing

def apriori_foruser(userid,userorders,orderdf, productsdf): 
    orderids = userorders[userorders['user_id']==userid]['order_id'].values
    orderbaskets = [] # by using name it makes it easier to notice what patterns mean
    for order in orderids: # for each order we look it up and create baskets over all of a users orders
        orderbaskets.append([item for item in orderdf[orderdf['order_id'] == order]['product_name']])# list compression        
    user_apriori_results = apriori_forone(orderbaskets) # borrows apriori for all and runs it on all of the user's orders 
    
    # print it to file
    return user_apriori_results

def generate_baskets_in_file(orderdf, file): # we are probably going to want to limit the size of our baskets
    ostdout = sys.stdout
    with open(file, 'a', encoding="utf-8") as ourfile: # got encodiing to work!!!
        sys.stdout = ourfile   
        for order in set(orderdf['order_id']): 
            print(",".join([str(item) for item in orderdf[orderdf['order_id'] == order]['product_id']]))# list compression        
        sys.stdout = ostdout
        ourfile.close()



#by storing and reading in the baskets from the file it is wayyyyyyyy faster, 
# like I can run the program in less than a minute instead of hours
def readinbaskets(file): 
    basketlist = [] # reuse from my code in PA 1, modified for commas
    with open(file, encoding="utf-8") as items:# running on actual data
        baskets = items.readlines() # now it is a list of baskets
        for basket in baskets: 
            basketlist.append(basket.split(","))#creates a list of the baskets filtered by spaces into the individual items for analysis
            basketlist[-1][-1] = basketlist[-1][-1].strip()#removes newline
        items.close()
    return basketlist


def generate_namedbaskets_in_file(orderdf, file): # we are probably going to want to limit the size of our baskets
    ostdout = sys.stdout
    with open(file, 'a', encoding="utf-8") as ourfile: # got encodiing to work!!!
        sys.stdout = ourfile   
        for order in set(orderdf['order_id']): 
            print("|".join([item for item in orderdf[orderdf['order_id'] == order]['product_name']]))# list compression        
        
        sys.stdout = ostdout
        ourfile.close()

def readinnamedbaskets(file): 
    basketlist = [] # reuse from my code in PA 1, modified for commas
    with open(file, encoding="utf-8") as items:# running on actual data
        baskets = items.readlines() # now it is a list of baskets
        for basket in baskets: 
            basketlist.append(basket.split("|"))#creates a list of the baskets filtered by spaces into the individual items for analysis
            basketlist[-1][-1] = basketlist[-1][-1].strip()#removes newline
        items.close()
    return basketlist


def randapriorisample10orders(order_info, orderdf, productsdf): 
    for i in range(0, 10):
        # it may pick a user that is in the wrong data set, expecially likely in train so I wont use this function for that 
        userid = random.choice(order_info.user_id.values) # pick a random order id
        num_baskets = len(order_info[order_info['user_id']==userid].values)# gets the number of baskets(orders) for the spricic user
        print("Apriori for {} => User ID = {}, Number of Baskets = {}".format(i, userid, num_baskets))
        apriori_foruser(userid, order_info, orderdf, productsdf)
    

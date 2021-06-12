# Caden Weiner
# Data Mining Final Project
# 4/1/2021
import pandas as pd
import csv
import sys
from apyori import apriori
import matplotlib.pyplot as plt
import time
from apyori import apriori


from readmarketdata import * 
from processdata import * 
from aprioriutil import * # this was the version I started with using the apriori library
from apriorimlxtend import * # this is the version with the mlxtend apriori library which is able to produce much more readable results, and it is the same library that fp comes from 



from plotIT import * 
from  fpgrowthutil import *
import pathlib
# caden

PRIOR = True
TRAIN = False
PLOTDATA = True
TRAINNAMES = "generatedfiles/basketTRAINNAMES.txt"
PRIORNAMES = "generatedfiles/basketPRIORNAMES.txt"

# I will be printing the results of fp to a file

# the result format of the apriori is much harder to deal with. I would like to possibly using the mlxtend version of the algorithm, but it produces the same results and It is hard to convert the whole dataset of baskets


def debug(authorized, *s): 
    if authorized: 
        print(*s)
TESTDEBUG = False
def load_data(): 
    department_info = read_departments() # not used in our analysis, but theoretically might be helpful if we were predicting the departments that would be ordered from rather than the items
    
    aisle_info = read_aisles()
    product_info = read_products()
    order_info = read_orders()
    order_train_info = read_order_products_train()
    order_prior_info = read_order_products_prior()
    
    # printing out the different inputs we made
    debug(TESTDEBUG, numberof_orders(give_users_order_list(order_info, 2)))
    debug(TESTDEBUG, department_info)
    debug(TESTDEBUG, aisle_info)
    debug(TESTDEBUG, product_info)
    debug(TESTDEBUG, order_info)
    debug(TESTDEBUG, order_train_info)
    debug(TESTDEBUG, order_prior_info)
    # testing loopuporder output
    debug(TESTDEBUG, look_up_order(order_train_info, 1))
    debug(TESTDEBUG, look_up_order(order_prior_info, 2))
    # testing print order items
    #print_products(product_info, look_up_order(order_train_info, 1))
    #print_products(product_info, look_up_order(order_prior_info, 2))

    #print_orderlist(give_users_order_list(order_info, 2))
    unique_users = getall_users(order_info)

    return aisle_info, product_info, order_info, order_prior_info, order_train_info

# Judging from the size of the data set, frequent triples will be fairly rare if any
def translation_key(product_info):
    key = {productid:name for productid, name in zip(product_info.product_id, product_info.product_name)} 
    return key

def priortests(order_info, order_prior_info, product_info): 
    print("READ BASKETS PRIOR")
    start = time.time()
    pbaskets = readinnamedbaskets(PRIORNAMES)
    end = time.time()        
    print("Reading baskets prior took : ", end - start)


    #wait = input("Press any key to Start random APRIORI MLXTEND sample ... ")

    print("Running APRIORI MLXTEND on 10 random users")
    start = time.time()
    randapsample10orders(order_info, order_prior_info, product_info,  "results/topresultsforuserap")
    end = time.time()
    print("Calculating APRIORI MLXTEND for 10 random users PRIOR took : ", end - start)

    
    #wait = input("Press any key to Start Full ap ... ")
    print("Running APRIORI MLXTEND on ALL PRIOR") # it is likely best to move the time functions to see how long only fp takes. It took around 1200 seconds last time for both running fp and constructing the df
    # This may take a while, but only because converting the list of items to a dataframe for fp takes a while due to the size
    start = time.time()
    ap_forall(pbaskets, .001,  "results/topresultsforallap.txt") # finding frequent pairs etc is the hardest so it is a bit slow
    end = time.time()
    print("Calculating APRIORI MLXTEND for all PRIOR took : ", end - start)

    




    ################################################################################################
    ################################################################################################

    #wait = input("Press any key to Start random FP sample ... ")

    print("Running FP on 10 random users")
    start = time.time()
    randfpsample10orders(order_info, order_prior_info, product_info, "results/topresultsforuserfp.txt")
    end = time.time()
    print("Calculating FP for 10 random users PRIOR took : ", end - start)

    
    #wait = input("Press any key to Start Full fp ... ")
    print("Running FP on ALL PRIOR") # it is likely best to move the time functions to see how long only fp takes. It took around 1200 seconds last time for both running fp and constructing the df
    # This may take a while, but only because converting the list of items to a dataframe for fp takes a while due to the size
    start = time.time()
    fp_forall(pbaskets, .001,  "results/topresultsforallfp.txt") # finding frequent pairs etc is the hardest so it is a bit slow
    end = time.time()
    print("Calculating FP for all PRIOR took : ", end - start)

    ################################################################################################
    ################################################################################################
    




    ################################################################################################
    ################################################################################################

    # this is from the apyori library that I was originally using

    #wait = input("Press any key to Start random Apriori (apyori library) sample ... ")
    
    # we can run apriori on particular users
    print("Apriori (apyori library) on 10 Random Users")
    start = time.time()
    randapriorisample10orders(order_info, order_prior_info, product_info)# also generates the baskets needed for all the user's orders
    end = time.time()
    print("Calculating APRIORI (apyori library) for 10 random users took : ", end - start)

    
    #wait = input("Press any key to Start Full Apriori (apyori library) ... ")

    # print("PBASKETS",pbaskets) # checking to make sure it lioaded the file properly since no results for apriori, I think the threshold was too high
    print("Running Apriori (apyori library) on ALL PRIOR") # takes about 7-8 minutes or so 
    start = time.time()
    apriori_forall(pbaskets, .001) # finding frequent pairs etc is the hardest so it is a bit slow
    end = time.time()
    print("Calculating APRIORI (apyori library) for all PRIOR took : ", end - start)

    ################################################################################################
    ################################################################################################





def testWeekends_and_Weekdays(order_info, order_prior_info, product_info): 
    weekend_info = order_info[order_info['order_dow'] <= 1]
    weekday_info = order_info[order_info['order_dow'] > 1]
    #weekends traditionally have more people use the market, and thus, more orders
    # now we have a df for weekends and weekdays

    # I would like to run it on the whole dataset, however it would take quite a long time

    #wait = input("Press any key to Start random APRIORI MLXTEND sample ... ")

    print("Running APRIORI MLXTEND on 10 random users Weekend")
    start = time.time()
    randapsample10orders(weekend_info, order_prior_info, product_info,  "dayresults/topresultsforuserapweekend.txt")
    end = time.time()
    print("Calculating APRIORI MLXTEND for 10 random users PRIOR took : ", end - start)

    ################################################################################################
    ################################################################################################

    print("Running FP on 10 random users Weekend")
    start = time.time()
    randfpsample10orders(order_info, order_prior_info, product_info, "dayresults/topresultsforuserfpweekend.txt")
    end = time.time()
    print("Calculating FP for 10 random users PRIOR took : ", end - start)

    ################################################################################################
    ################################################################################################
    # weekdays 
    
    #wait = input("Press any key to Start random APRIORI MLXTEND sample ... ")

    print("Running APRIORI MLXTEND on 10 random users Weekday")
    start = time.time()
    randapsample10orders(order_info, order_prior_info, product_info,  "dayresults/topresultsforuserapweekday.txt")
    end = time.time()
    print("Calculating APRIORI MLXTEND for 10 random users PRIOR took : ", end - start)



    ################################################################################################
    ################################################################################################

    print("Running FP on 10 random users Weekday")
    start = time.time()
    randfpsample10orders(order_info, order_prior_info, product_info, "dayresults/topresultsforuserfpweekday.txt")
    end = time.time()
    print("Calculating FP for 10 random users PRIOR took : ", end - start)


    ################################################################################################
    ################################################################################################
    



# this portion isn't important, it was originally helpful to test on the smaller dataset
# since prior, the large dataset runs well I focus on that instead    
def runtraintests(order_info,order_train_info, product_info): 
    print ("READ BASKETS")
    start = time.time()
        #tbaskets = readinbaskets("generatedfiles/basketTRAIN.txt")
    tbaskets = readinnamedbaskets(TRAINNAMES)
    end = time.time()
    print("Read Baskets takes : ", end - start)

        # print("RUNNING TRAINING")
        # start = time.time()
        # t_basketlist = generate_baskets(order_train_info) # smaller amount of orders # it successfully creates it
        # end = time.time()
        # print("Creating TRAINING BASKETS took : ", end - start)
        #h_t_basketlist = generate_baskets_for_humans(order_train_info)
        # we may want to just use basket ids # fixed encoding for accents
        #storebaskets(t_basketlist, "generatedfiles/BASKETS_T.txt")
        #storebaskets(h_t_basketlist, "generatedfiles/READABLEBASKETSHUMAN_T.txt")
    print("Running Apriori")
    start = time.time()
    apriori_forall(tbaskets, .005)# threshold a bit greater to limit the amount of entries a bit
    end = time.time()
    print("Calculating ALL TRAINING APRIORI took : ", end - start)

        # we can run apriori on particular users
    # not needed for train, its really hard to deal with based off of how they give us 
    # user ids but different orders of the users in both data sets
    # because the prior data set is so much larger 
    # it often just has many blank orders as the orders are in the wrong data set
    # so I will just only do it in prior
    # this method of apriori doesn't rely on the big set of baskets but instead makes new
    # basket sets for each individual user
    # print("Apriori on 10 Rand Users")
    # start = time.time()
    # randapriorisample10orders(order_info, order_train_info, product_info)
    # end = time.time()
    # print("Calculating APRIORI for 10 random users took : ", end - start)



def connect_names(order_train_info,order_prior_info, translationdict): 
    order_prior_info['product_name'] = order_prior_info.product_id.map(lambda x: translationdict.get(x)) # using the map function built in to pandas
    order_train_info['product_name'] = order_train_info.product_id.map(lambda x: translationdict.get(x)) # using the map function built in to pandas
    return order_train_info, order_prior_info

def calculateItemFrequencies(product_info,order_info): 
    return calculateitemfrequencies(product_info, order_info) # returns a df with item frequencies
    
def run_tests(): 
    aisle_info, product_info, order_info, order_prior_info, order_train_info = load_data() # load in our data for testing
    my_translation_key = translation_key(product_info)

    # I will now drop unneccessary columns to try and limit memory usage
    print("Drop Unneccessary Columns")
    order_prior_info = order_prior_info.drop(['add_to_cart_order', 'reordered'], axis = 1)
    order_train_info = order_train_info.drop(['add_to_cart_order', 'reordered'], axis = 1)
    order_info = order_info.drop(['eval_set', 'days_since_prior_order', 'order_number'], axis = 1) # drop all the unneccessary collumns to improve memory usage greatly
    #print(order_prior_info.head())
    #print(order_train_info.head())
    #print(order_info.head())

    # df now contains name info
    order_train_info, order_prior_info = connect_names(order_train_info, order_prior_info, my_translation_key)
    
    # if (True): # ignore this part for now, just my own info
    createorders(order_info, "generatedfiles/orderids.txt") # prints all of the order ids to a file
    userids = uniqueusers(order_info, "generatedfiles/userids.txt") # creates a list of user ids, can be used for testing
    
    # we have two data sets, order_prior_info and order_train_info
    # we will run on both datasets
    # add names to the order information based of the product id
    # we can do both, one or neither
    if (PRIOR): # larger data set, will take much longer to run, so maybe break the data into multiple smaller subsets and run it that way
        basketfilePRIOR = pathlib.Path(PRIORNAMES)
        if basketfilePRIOR.exists ():
            print("basketfilePRIORNAMES exist") # no need to create baskets again
        else:
            print("basketfilePRIORNAMES does not exist, creating baskets") # need to create the file and write the baskets to it
            # It is very slow, the best way is likely to break it up into smaller chunks instead of running all of the data at once
            start = time.time()
            print("shape prior orders ",order_prior_info.shape) # if we filter out the non frequent items first it may also go much faster
            # way faster when I load it in as chunks, probably because it has to search through less data to generate the baskets
            # took 69 minutes or so 
            # for i in range(0,61):# this makes it go much much faster, I will load it into a file so I can just read from the file strait to do apriori quickly
            #     generate_baskets_in_file(order_prior_info[i*500000:(i+1)*500000], "generatedfiles/BASKETSsmallerload.txt")
            # took 52 minutes
            # 62 cases where a data set may be split in two out of 3,200,000 baskets. Looking at a way to check if the basket is split or not. Doing it in 620 cycles is faster but it breaks thbaskets apart more
            for i in range(0,61):# this makes it go much much faster, I will load it into a file so I can just read from the file strait to do apriori quickly
                generate_namedbaskets_in_file(order_prior_info[i*500000:(i+1)*500000], PRIORNAMES)
            end = time.time()
            print("Baskets in file took: ", end - start)

        # regardless of days
        priortests(order_info, order_prior_info, product_info)
        # observing changes in weekday vs weekends, hard to get concrete differences 
        testWeekends_and_Weekdays(order_info, order_prior_info, product_info)



    x = input("Press Any Key to Continue .......") 





    
    if (TRAIN): # smaller dataset, most of our data to train and pinpoint the best settings was done using the training data set as it ran much faster than the prior training set as it is 1 tenth of the size approximately
        #basketfileTRAIN = pathlib.Path("generatedfiles/basketTRAIN.txt")
        basketfileTRAIN = pathlib.Path(TRAINNAMES)
        if basketfileTRAIN.exists ():
            #print ("basketfileTRAIN exist")
            print ("basketfileTRAINNAMES exist")
        else:
            print ("basketfileTRAINNAMES not exist, generate baskets")
            #print ("basketfileTRAIN not exist, generate baskets")
            start = time.time()
            for i in range(0,5):# this makes it go much much faster, I will load it into a file so I can just read from the file strait to do apriori quickly
                generate_namedbaskets_in_file(order_train_info[i*250000:(i+1)*250000], TRAINNAMES)
                generate_baskets_in_file(order_train_info[i*25000:(i+1)*25000], "generatedfiles/basketTRAIN.txt")
           
            end = time.time()
            print("TRAIN Baskets takes : ", end - start)
        
        runtraintests(order_info,order_train_info, product_info)
        
  

    





######################################################################################
######################################################################################
######################################################################################
    print("Create Data Frames with frequencies train")
    print("Order Train info unfiltered",order_train_info.shape)
    start = time.time() # doing it by frequency takes way longer, buuut the other steps become way faster. It might be ideal to store it once, then reload it in many times
    _train_item_frequencies, order_train_info = calculateItemFrequencies(product_info, order_train_info)
    end = time.time()
    print("Frequencies took : ", end - start)
    #print(_train_item_frequencies)
    print(_train_item_frequencies.shape)
    print("Order Train info filtered",order_train_info.shape)


#############################################################################################################
        
    
    print("Create Data Frames with frequencies prior")
    print("Order Prior info unfiltered",order_prior_info.shape)
    start = time.time() # doing it by frequency takes way longer, buuut the other steps become way faster. It might be ideal to store it once, then reload it in many times
    _prior_item_frequencies, order_prior_info = calculateItemFrequencies(product_info, order_prior_info[0:1000000]) # feeding in only a portion so it runs faster # it is still really slow just because it needs to calculate for so many items
    end = time.time()
    print("Frequencies took : ", end - start)
    print(_prior_item_frequencies)
    print(_prior_item_frequencies.shape)
    print("Order prior info filtered",order_prior_info.shape)
        
######################################################################################
######################################################################################
######################################################################################
# _train_item_frequencies = _train_item_frequencies[_train_item_frequencies['frequencies'] >= .01] # we only care about the items that appear in at least 1 % of the baskets
    
######################################################################################
######################################################################################
######################################################################################


    if (PLOTDATA): # global flag, currently false
        run_plots(order_info, order_prior_info, _prior_item_frequencies) # plots the prior info # these plots are basically the same
        #run_plots(order_info, order_train_info, _train_item_frequencies) # plots the train info











#   start = time.time()
  
#   end = time.time()
#   print("Calculating all Similairities took : ", end - start)




# print("RUNNING PRIOR, BASKETS IN FILE")
        # # It is very slow, the best way is likely to break it up into smaller chunks instead of running all of the data at once
        # start = time.time()
        # print(order_prior_info.shape) # if we filter out the non frequent items first it may also go much faster
        # generate_baskets_in_file(order_prior_info, "generatedfiles/BASKETS_frequenciesprior.txt")
        # end = time.time()
        # print("RUNNING PRIOR")
        # start = time.time()# we may want to remove any non frequent items before this as it is taking a long time
        # p_basketlist = generate_baskets(order_prior_info) # smaller amount of orders # it successfully creates it
        # end = time.time()
        # print("CREATING BASKETS for PRIOR took : ", end - start)
        # we may want to just use basket ids # fixed encoding for accents
        #storebaskets(p_basketlist, "generatedfiles/BASKETS.txt")
        # not as helpful because the data is so large, makes the program run much slower
        #h_p_basketlist = generate_baskets_for_humans(order_prior_info)
        #storebaskets(h_p_basketlist, "generatedfiles/READABLEBASKETSHUMAN.txt")
        # print("READ BASKETS PRIOR")
        # start = time.time()
        # pbaskets = readinbaskets("generatedfiles/basketPRIOR.txt")
        # end = time.time()        
        # print("Reading baskets prior took : ", end - start)
        # # print("PBASKETS",pbaskets) # checking to make sure it lioaded the file properly since no results for apriori, I think the threshold was too high
        # print("Running Apriori")
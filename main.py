# Caden Weiner
# Data Mining Final Project
# 4/1/2021
from run_tests import * 

# defined gloabls to indicate how to run the program, for testing
#RUNAPRIORI = False

if __name__ == "__main__": 
    run_tests()
    
    # association_rules = apriori(records, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2)
    # association_results = list(association_rules)

###############################################################################
# In order to deal with the different methods, I think that it might be interesting to 
# try and run the different basket sorting algorithms, compare their run times and results
# theoretically all of the results should be the same. 
###############################################################################
# it might be interesting to generate the top rules for an individual user, and the top rules
# for all the users, ie treating each user independently and using the data as a whole
###############################################################################
# Order_products contains all of the items in each of the orders, we may want to preprocess this information 
###############################################################################
# It might be best to read data into a seperate file that way we do not have to processes it everytime
###############################################################################
# We may also want to remove certain components of the data frame that we aren't using to improve memory 
# usage. this is df.drop(["user_id", "product_id"]) # for example
###############################################################################
# We can also use tools to graph some of the information about the data we
# are using in order for us to better understand trends and ways to improve our approach
###############################################################################
# finding information about the data may be helpful for making inferences. 
# ie predicting what a user/all of the users may buy on friday vs saturday
# this is definitely helpful for online retailers as they can recommend products
# rather than adjusting the entire store
# also hour of the day may be important,more likely to buy coffee in the morning, etc
###############################################################################

#python3 main.py

# previous info. Modified the code to make it much cleaner

    #reading in the order information
    # print("Performing Operation")
    # flag = 2
    # if flag == 1: #manipulate data
    #     perform_operation_onall_users_orders_file(order_info, unique_users, numberof_orders, "numberofusersbaskets.csv")
    # elif flag == 2: #graph
    #     read_graph_order_size_frequencies()
    # createorders(order_info, "orderids.txt")
    # userids = uniqueusers(order_info, "userids.txt")
    # now we use the user ids to run apriori on each of the userids
    # print(order_prior_info.info())
    # print(order_prior_info.shape)
    # we can do head(n) where n is the number of elements and we get the top n
    #print(order_prior_info.head(30))
    # merge the two data frames together and groupby the order id and the max amount of the order size
    # product_order_names = order_prior_info.copy()
    # translationdict = {productid:name for productid, name in zip(product_info.product_id, product_info.product_name)}
    # product_order_names['product_name'] = order_prior_info.product_id.map(lambda x: translationdict[x]) # using the map function built in to pandas
    # order_train_info['product_name'] = order_train_info.product_id.map(lambda x: translationdict[x]) # using the map function built in to pandas
    # print(product_order_names)
    # the longest step, is probably the creation of baskets  
    # if (RUNAPRIORI): 
    #     basketlist = generate_baskets(order_train_info) # smaller amount of orders # it successfully creates it
    #     sbasketlist = generate_baskets_for_humans(order_train_info)
    #     # we may want to just use basket ids    #weird encoding errors due to accents # fixed encoding
    #     storebaskets(basketlist, "BASKETS.txt")
    #     storebaskets(sbasketlist, "READABLEBASKETSHUMAN.txt")
    #     print("Running Apriori")
    #     apriori_forall(basketlist)
    #     # we can run apriori on particular users
    #     print("Apriori on User 1")
    #     apriori_foruser(1,order_info,order_prior_info, product_info)
    #generate_baskets(product_order_names)# this is quite slow, need to try and find a way to speed it up
    #product_order_names[['product_name', 'order_id']] # reduce df to just these two columns

    
    ##########################################
    ##########################################
    ##########################################
    ########################################## computations can be added to another function
    ##########################################
    ##########################################
    ##########################################
    # perhaps we can determine which items are infrequent and filter them out? That way it will speed up apriori

    # to just find the frequent pairs, we could theoretically enumerate all the possible pairs for 
    # a basket and then check if the frequency of both items is greater than our threshold (ie they are both frequent items)
    # perhaps it is a good idea to look into frequent triples asa well, however if it isn't, 
    # it may make sense to try and implement it through the original aproach rather than 
    # using apriori
    # we could also look into the time complexities when we compair the two 
    # should we look into the reordered feature? 
    # I am not really sure how to utilize that in conjunction with apriori
    # I tried to implement it but decided to remove it since it wasn't helpful and was time consuming
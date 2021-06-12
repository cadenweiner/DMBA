import pandas
import sys
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import random
import time

# I was trying with 10 % support but that was much too high considering all the possible items
def ap_forall(recordlist,support, file): 
    # by decreasing lift, the number of rules accepted increases, by decreasing min support num rules increases
    transaction_encoder = TransactionEncoder()
    # this is an encoding method, for 2d arrays 
    # make a way to get a random sample and run it several times
    # this needs to use low memory mode and is much slower compaired to apyori's implementation.
    # encoding the transactions takes the longest amount of time. 
    startbound = 1000000
    endbound = 2500000
    recordlist = recordlist[startbound:endbound] # I have to use less orders because of size limitations, it seems that encoding is a bit weird for the large set so I will use a sampling function. I am taking half the set so all frequent items should be frequent within it
    transaction_encoder_ary = transaction_encoder.fit(recordlist).transform(recordlist, sparse = True) # convert a list of baskets into a dataframe for running apriori mlxtend it now runs without crashing due to memory issues
    #print(te_ary)
    
    recorddf = pandas.DataFrame.sparse.from_spmatrix(transaction_encoder_ary, columns=transaction_encoder.columns_) 
    # print(recorddf.shape) # these were checks when I was making the matrix sparse and trying to debug the code
    # print(recorddf)
    #recorddf = pandas.SparseDataFrame(recorddfNOTSPARSE, default_fill_value=0)
    
    #print(recorddf) 
    
    print("Created the Data Frame Successfully") # this is not the problem 
    start = time.time()
    ap_results = apriori(recorddf, min_support=support, use_colnames=True, max_len = 4, low_memory = True) # we are forced to use low memory since we don't have enough - will be approximately 3-6 times slower than default
    
    print("Generating Rules ")
    # memory issues with this apriori may want to switch to efficient apriori 
    rules = association_rules(ap_results, metric="confidence", min_threshold=.4) # when we run iton all of the data we end up with fairly low confidence
    rules = rules.sort_values(['lift'], ascending=False) # sort by support , confidence already surpases our minimum threshold but we want the ones with the highest confidence
    end = time.time()
    print("Time to Run APRIORI MLX was exactly", end - start)
    printresultsap("\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", file)  # formatting in between new entries
    basketssize = startbound - endbound
    printresultsap("Rules for All Baskets First {} Orders Took {} Seconds | Low Memory Mode | (Order Range ({} -> {}))".format(basketssize,(end-start), startbound, endbound), file)  
    printresultsap("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n", file)  # formatting in between new entries

    printrulesforfullap(rules,file)
    
    
    return rules

def _ap(basketlist, support):
    return apriori(basketlist, min_support=support, use_colnames=True, max_len = 5) # run apriori mlxtend, the max length feature helps prevent the tree from growing out of control when there are way too many frequent patterns ie sizes 10 etc the don't provide super useful information as their confidence scores are low and eat up a ton of time as they don't have montonicity and can't drop items. It generaates the rules much faster now as it can stop itself sooner since I care more about metrics other than just set size. Plus five is already a pretty large basket rule

    
def ap_foruser(userid,userorders,orderdf, productsdf, support): 
    orderids = userorders[userorders['user_id']==userid]['order_id'].values
    orderbaskets = [] # by using name it makes it easier to notice what patterns mean
    for order in orderids: # for each order we look it up and create baskets over all of a users orders
        orderbaskets.append([item for item in orderdf[orderdf['order_id'] == order]['product_name']])# list compression        
    te = TransactionEncoder()
    # this is an encoding method for 2d arrays 
    te_ary = te.fit(orderbaskets).transform(orderbaskets) # convert a list of baskets into a dataframe for running apriori mlxtend
    df = pandas.DataFrame(te_ary, columns=te.columns_)# turn it into a dataframe
    user_ap_results = _ap(df, support) # borrows apriori for all and runs it on all of the user's orders 
    print("Generating Rules")
    if user_ap_results.empty: # if the dataframe is empty return an error code not to print
        return user_ap_results # we couldn't get results 
    rules = association_rules(user_ap_results,metric="confidence", min_threshold=.65) # we know the users set is smaller and more self contained (ie it is more likely for a user to choose similair items so the confidence threshold can be higher) # originally set to 7 but I slowly started to decrease it as not all users could generate rules with such confidence scores (NOTE: This was due to a change I made to the print statement conditions which had led to it printing only if it had exactly two rules, not that the confidence was causing the problem) 
    
    #print(rules)
    # why is sorting by support better? Since we already pass the confidence threshold, we want to take the rules with the highest support as they will be better indicators of user patterns
    # rules = rules.sort_values(['support'], ascending=False) # sort by support , confidence already surpases our minimum threshold but we want the ones with the highest confidence
    #rules = rules.sort_values(['confidence'], ascending=False)
    
    rules = rules.sort_values(['lift'], ascending=False) # lift, accounts for the base popularity of both items, the higher the more correlated two items are
    return rules



def randapsample10orders(order_info, orderdf, productsdf, file): 
    for i in range(0, 10):
        userid = random.choice(order_info.user_id.values) # pick a random order id
        num_baskets = len(order_info[order_info['user_id']==userid].values)# gets the number of baskets(orders) for the spricic user
        if num_baskets <= 5: 
            support = .3 # Need a large support when there are less sets to get relevant info
        elif num_baskets > 50: 
            support = .1 # need smaller support when there are more baskets
        else: 
            support = .2 # support for the range of 6-50 # must apear in more than one basket for size 6 

        print("APRIORI MLXTEND for {} => User ID = {}, Number of Baskets = {}".format(i, userid, num_baskets))
        printresultsap("User ID = {}, Number of Baskets = {}".format(userid, num_baskets), file)
        rules = ap_foruser(userid, order_info, orderdf, productsdf, support) # only take the rules with confidence of 
        
        printtoptwoap(rules, file)

def printresultsap(statement, file): 
    ostdout = sys.stdout
    with open(file, 'a', encoding="utf-8") as ourfile: # got encodiing to work!!!
        sys.stdout = ourfile   
        print(statement)
        sys.stdout = ostdout
        ourfile.close()

# Used Join Statements on the Frozen Set to Improve the Print Output
# I used control F to find and replace the frozen set printed as a string instance to make them more readable as tuples insteas ie frozenset({'', ''}) became ('', '')

def printtoptwoap(rules, file):
    if len(rules['support']) > 1: # there is more than one so we just take top two rules
        printresultsap("Antecedent: (" + str(", ".join(rules['antecedents'].values[0])) + "), Consequent: ("+ str(", ".join(rules['consequents'].values[0])) + ") , Support: " + str(rules['support'].values[0]) + ", Lift: " + str(rules['lift'].values[0]) + ", Confidence: " + str(rules['confidence'].values[0]), file)  
        printresultsap("Antecedent: (" + str(", ".join(rules['antecedents'].values[1])) + "), Consequent: ("+ str(", ".join(rules['consequents'].values[1])) + ") , Support: " + str(rules['support'].values[1]) + ", Lift: " + str(rules['lift'].values[1]) + ", Confidence: " + str(rules['confidence'].values[1]), file)  
    elif len(rules['support']) == 1: # there is exactly one value so we take it
        printresultsap("Antecedent: (" + str(", ".join(rules['antecedents'].values[0])) + "), Consequent: ("+ str(", ".join(rules['consequents'].values[0])) + ") , Support: " + str(rules['support'].values[0]) + ", Lift: " + str(rules['lift'].values[0]) + ", Confidence: " + str(rules['confidence'].values[0]), file)  
    else: 
        printresultsap("No Rules Generated that pass Confidence and Support Thresholds", "results/topresultsforuserap")  

def printrulesforfullap(rules, file): 
    #printresultsap("Rules for All Baskets", "results/topresultsforallap")  
    for i in range(0, len(rules['support'])): 
        printresultsap("Antecedent: (" + str(", ".join(rules['antecedents'].values[i])) + "), Consequent: ("+ str(", ".join(rules['consequents'].values[i])) + ") , Support: " + str(rules['support'].values[i]) + ", Lift: " + str(rules['lift'].values[i]) + ", Confidence: " + str(rules['confidence'].values[i]), file)  




# with ap we need a different function to filter out confidence
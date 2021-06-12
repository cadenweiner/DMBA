import pandas as pd

# Caden: 
# I implemented pandas read_csv to read in all of the data from the different files into
# their own data frames. This allows us to easily deal with the data and we will be 
# able to split the features easily based on the use of searching for specific values
# in the data frame. IE for orders we can search for all of a a specific users orders. 
def read_departments(): 
    dFrame = pd.read_csv("marketdata/departments.csv")
    dFrame = dFrame[['department_id', 'department']]
    return dFrame

def read_aisles(): 
    dFrame = pd.read_csv("marketdata/aisles.csv")
    dFrame = dFrame[['aisle_id','aisle']]
    return dFrame

def read_products(): 
    dFrame = pd.read_csv("marketdata/products.csv")
    dFrame = dFrame[['product_id','product_name','aisle_id','department_id']]
    return dFrame

def read_orders(): 
    dFrame = pd.read_csv("marketdata/orders.csv")
    dFrame = dFrame[['order_id','user_id','eval_set','order_number','order_dow','order_hour_of_day','days_since_prior_order']]
    return dFrame

def read_order_products_prior(): 
    dFrame = pd.read_csv("marketdata/order_products__prior.csv")
    dFrame = dFrame[['order_id','product_id','add_to_cart_order','reordered']]
    return dFrame

def read_order_products_train(): 
    dFrame = pd.read_csv("marketdata/order_products__train.csv")
    dFrame = dFrame[['order_id','product_id','add_to_cart_order','reordered']]
    return dFrame

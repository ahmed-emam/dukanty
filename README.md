Duaknty is an app for online grocery shopping. It will connect you to your nearest local supermarket and act as a liaison between you and the market, assuming the market is signed up with our service.

                                                    Server

Functionality:

Users:
    Database of users registered in our service
    User consist of:
        -   email (used for logging in)
        -   password
        -   phone number
        -   market/customer
    Functionality required:
        -   sign up
        -   login
        -   token authentication
        -   log out

Market/Shop:
    Database of registered markets
    Shop consist of:
        -   Name
        -   Latitude
        -   Longitude
        -   Rating
        -   owner (linked to a user)
    Functionality required, (Server related functionality no api will be provided for commercial use):
        -   add/modify if previously added
        -   remove
        -   getter function

Products:
    Universal list of products.
    product consist of:
        -   Name
        -   Supplier
        -   Category (Bakery, Dairy, Meat, etc)
        -   Image
    Functionality required, (Server related functionality no api will be provided for commercial use):
        -   add
        -   Remove
        -   getter function

Inventory:
    Each market keeps an inventory of products, out of the universal list of products, at his market
    Inventory consist of:
        -   Product
        -   In stock? (T/F)
        -   Price

    Functionality required:
        -   add, Only by the shop owner
        -   remove, Only by the shop owner
        -   getter function


Order:
    An order made by user to specific market, its a list of products
    Order consist of:
        -   list of (Products, price, quantity)
        -   owner (customer)
        -   Market
        -   Status of order (Issued, Accepted, In delivery)
        -   Created at
        -   Modified at
    Functionality required:
        -   create
        -   delete
        -   modify
        -   callback function for modifications, modifications should be propagated depending on status of order
            The callback function will handle:
                -   Checkout,   When the order has been checked-out by the user it should send the order to the market
(Check with the team)
                -   Modification by the user, till when can the user modify his order?
                -   Modification by the market, if any changes to the order has been made the user should be notified
                    by a in-app message
                -   When the market changes the status of the order, Issued --> Accepted or Accepted --> In delivery,
                    the customer should be notified
        - getter function

Basket:
    Pre-saved order
    Basket consist of:
        -   list of Products
    Functionality required:
        -   create
        -   delete
        -   modify
        - getter function
        -   availability check
            When the user wants to purchase a basket, the mobile app should check if the products in that baskets are
            available in the chosen market. If not then the user will be notified




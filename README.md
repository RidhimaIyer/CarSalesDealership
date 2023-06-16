## Car Sales By Dealership 

# Application Details: 

This application keeps tracking record of car inventory and their sales happening in respective dealership. It also calculates sale invoices when user places an order for car purchase. It also allows to create a new employee as well as a new customer.

# Data Models & Respective Functionalities allowed:

Mentioned below are the different data models created(along with primary key and foreign key information) and their respective functionalities defined in their respective view files.

** 1. CarModel - Car model stores all car information in the DB. **

** Structure: **
    car_id(primary key created on the time of creating a new record )
    car_serial_no(unique serial no specific to a car )
    make 
    model
    year 
    color
    price 
    created_at (when record is created)
    modified_at(when record is modified)

** Functionalities allowed: **
    - Create a new car 
    - List all cars 
    - Get Car by car_serial_no 
    - Patch(update) car by car_serial_no 
    - Delete car by car_serial_no 

** 2. CustomerModel: Stores customer information in DB **

** Structure: ** 
    customer_id(primary key created of the time of creation of new record )
    phone
    email_id
    ssn(identification of customer - required to buy car )
    first_name
    last_name
    address
    created_at (when record is created)
    modified_at(when record is modified)

** Functionalities allowed: **
    - Add a new customer 
    - List all customers 
    - Get Customer by customer_id 
    - Patch(update) customer by customer_id 
    - Delete customer by customer_id 


** 3. DealerInventoryModel - Dealer Inventory is the associative mapping between a Dealer and Car. It lists the number of cars present in inventory for that dealer. **
        

** Structure: **
    dealer_inventory_id (primary_key created on time of creation)
    car_count (Number of cars present in inventory for a particular car)
    car_serial_no (Foreign Key- must be present in Car table)
    dealer_id (Foreign Key- must be present in Dealer table)
    created_at (when record is created)
    modified_at(when record is modified)

** Functionalities allowed: **
    - Add a new dealer inventory record 
    - list all dealer inventories 
    - Get inventory information based on dealer_id 
    - Get inventory information based on dealer_id and car_serial_no 
    - Patch(Update) inventory information based on dealer_id and car_serial_no 
    - Delee inventory record based on dealer_id and car_serial_no 

** 4. DealerModel - Stores Dealer information in DB  **

** Structure: **
    - dealer_id(primary key created on time of creation)
    - name (name of dealer)
    - web_url 
    - street_address
    - postal_code 
    - city 
    - state
    - state_tax_id (Foreign Key- must be present in StateTaxModel table)
    - created_at (when record is created)
    - modified_at(when record is modified)

** Functionalities allowed: **
    - Create a new dealer 
    - List all dealers 
    - Get dealer by dealer_id 
    - Get all dealers by state 
    - Patch(Update) dealer by dealer_id 
    - Delete dealer by dealer_id 

** 5. EmployeeModel - Stores Employee information in db **

** Structure: **
    - employee_id(primary key)
    - first_name
    - last_name 
    - dealer_id (Foreign key - must be present in dealers table)
    - created_at (when record is created)
    - modified_at(when record is modified)

** Functionalities allowed: **
    - Create a new employee 
    - List all employees 
    - Get employee by employee_id 
    - Get all employees by dealer_id 
    - Patch(Update) employee by employee_id 
    - Delete employee by employee_id

** 6. SaleLineItemModel - Stores line item information for any sale record. It contains the quantity of items in one sale record. Also calculates the net_price for each sale line item record considering the net_tax and discount_amt **

** Structure: **
    - invoice_line_item_id ( primary key)
    - quantity 
    - car_unit_price 
    - item_tax
    - discount_percentage
    - car_net_price ( (car_unit_price - discount + tax) * quantity)
    - car_serial_no 
    - invoice_id ( Foreign key- must be present in SaleModel)
    - created_at (when record is created)
    - modified_at(when record is modified)

** Functionalities allowed: ** 
    - Create a new sale line item record for a particular invoice 
    - List all sale line items for an invoice 
    - Patch(Update) sale line item by invoice_line_item_id
    - Delete sale line item by invoice_line_item_id

** 7. SaleModel - Stores Sale record **

** Structure ** 
    - invoice_id (primary key)
    - date_of_purchase
    - net_tax (updated once sale line item is added/updated/deleted)
    - net_price (updated once sale line item is added/updated/deleted)
    - dealer_id (foreignkey- must be present in dealers table)
    - customer_id(foreignkey- must be present in customer table)
    - employee_id(foreign key - must be present in employee table)
    - created_at (when record is created)
    - modified_at(when record is modified)

** Functionalites allowed: **
    - Create a new sale record 
    - List all sales by dealer_id based on date_of_purchase range
    - List all sales by dealer_id and customer_id based on date_of_purchase range
    - Patch(Update) sale by invoice_id
    - Delete sale by invoice_id

** 8. StateTaxModel - Stores the Tax information for states  **

** Structure: **
    - state_tax_id(primary key) 
    - state 
    - tax 
    - created_at (when record is created)
    - modified_at(when record is modified)

** Functionalities allowed: ** 
    - Create a new state tax record 
    - List all state taxes 
    - Get state_tax by state_tax_id 
    - Get state_tax by state 
    - Patch(Update) state_Tax by state_tax_id
    - Delete state_Tax by state_tax_id
    

## Technical Approach : 
This application uses Flask as its main web framework. Flask is chosen since it is highly flexible and gives full autonomy to structure the application based on our requirement. Also, flask provides the functionality of Blueprints(used here) which allows to organize code and seperate funcionalities allowing to decouple our application into smaller re-usable components. For API documentation Swagger(openapi 3.0.0) is used. "Connexion" is used to setup swagger to allow for writing swagger api before implementing operations. 

## Database:
This application uses Sqlite for testing. The database models are created at the time of app creation. Attached with this repo is a "dataabase.db" file which contains one record for each model to help with functionality testing. 

## API Documentation: 
Swagger OpenAPi 3.0.0
Swagger Local URL(available after starting app) : http://127.0.0.1:5000/ui/

## Package Requirements:
pipenv 
flask-sqlalchemy = "*"
flask-migrate = "*"
connexion = {extras = ["swagger-ui"], version = "*"}
flask = "==2.2.5"

##Usage:

1. Setup Virtual Environment: This will create a new virtual environment and download all required packages

pipenv install 

2. Start the application 

pipenv run python wsgi.py 

3. Open swagger url for further processing: http://127.0.0.1:5000/ui/
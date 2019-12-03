BEGIN TRANSACTION;
 
CREATE TABLE if not exists products (
product_line VARCHAR,
product_code VARCHAR PRIMARY KEY,
product_name VARCHAR,
product_scale VARCHAR,
product_vendor VARCHAR,
product_description VARCHAR,
quantity_in_stock INT,
buy_price float,
msrp varchar,
html_description varchar
);

CREATE TABLE if not exists employees (
office_code VARCHAR,
employee_number INTEGER PRIMARY KEY,
last_name VARCHAR,
first_name VARCHAR,
reports_to INTEGER,
job_title VARCHAR,
city varchar,
state varchar, 
country varchar,
office_location varchar
);

CREATE TABLE if not exists orders (
customer_number INTEGER,
order_number INTEGER,
product_code varchar,
quantity_ordered INTEGER,
price_each float,
order_line_number INTEGER,
order_date TIMESTAMP,
required_date TIMESTAMP,
shipped_date TIMESTAMP,
status VARCHAR,
product_comment varchar,
customer_name VARCHAR,
contact_last_name VARCHAR,
contact_first_name VARCHAR,
city varchar,
state varchar, 
country varchar,
sales_rep_employee_number INTEGER,
credit_limit varchar,
customer_location varchar
);

END TRANSACTION;
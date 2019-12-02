BEGIN TRANSACTION;

create schema if not exists classic_models;

SET search_path TO classic_models;

CREATE TABLE if not exists classic_models.product_lines (
product_line VARCHAR PRIMARY KEY,
text_description VARCHAR,
html_description VARCHAR,
image VARCHAR
);

CREATE TABLE if not exists classic_models.products (
product_code VARCHAR PRIMARY KEY,
product_name VARCHAR,
product_line VARCHAR REFERENCES product_lines (product_line),
product_scale VARCHAR,
product_vendor VARCHAR,
quantity_in_stock INT,
buy_price MONEY,
msrp MONEY
);

CREATE TABLE if not exists classic_models.offices (
office_code VARCHAR PRIMARY KEY,
city VARCHAR,
country VARCHAR
);

CREATE TABLE if not exists classic_models.employees (
employee_number INTEGER PRIMARY KEY,
last_name VARCHAR,
first_name VARCHAR,
email VARCHAR,
office_code VARCHAR REFERENCES offices (office_code),
reports_to INTEGER REFERENCES employees (employee_number),
job_title VARCHAR
);

CREATE TABLE if not exists classic_models.customers (
customer_number INTEGER PRIMARY KEY,
customer_name VARCHAR,
contact_first_name VARCHAR,
contact_last_name VARCHAR,
city VARCHAR,
state VARCHAR,
postal_code VARCHAR,
country VARCHAR,
sales_rep_employee_number INTEGER REFERENCES employees (employee_number),
credit_limit MONEY
);

CREATE TABLE if not exists classic_models.orders (
order_number INTEGER PRIMARY KEY,
order_date TIMESTAMP,
required_date TIMESTAMP,
shipped_date TIMESTAMP,
status VARCHAR,
customer_number INTEGER REFERENCES customers (customer_number)
);

CREATE TABLE if not exists classic_models.order_details (
order_line_number INTEGER,
order_number INTEGER REFERENCES orders (order_number),
product_code VARCHAR REFERENCES products (product_code),
quantity_ordered INTEGER,
price_each MONEY,
PRIMARY KEY (order_line_number, order_number)
);

END TRANSACTION;
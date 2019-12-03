import pandas as pd
import dataset
import os

def check_nan(d):
    return None if pd.isna(d) else d

def cast_keys(d, keys):
    for k in keys:
        d[k] = check_nan(d[k])
    return d

def load_table(db, dat, table, keys, nones = []):
    recs = dat.drop_duplicates(keys).to_dict(orient='record')
    recs = [cast_keys(d, nones) for d in recs]
    table = db[table]
    table.insert_many(recs, ensure=False)

if __name__ == '__main__':
    db = dataset.connect('postgres://mydb:mydb@localhost:5439/mydb')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cwd = os.getcwd()
    print(dir_path)
    products = pd.read_csv(cwd+'/postgres/pg_data/products.csv').rename(columns= {'_m_s_r_p': 'msrp'})
    orders = pd.read_csv(cwd+'/postgres/pg_data/orders.csv')
    employees = pd.read_csv(cwd+'/postgres/pg_data/employees.csv')

    tables = [
        (products, 'product_lines', 'product_line'),
        (products, 'products', 'product_code'),
        (employees, 'offices', 'office_code'),
        (employees, 'employees', 'employee_number', ['reports_to']),
        (orders, 'customers', 'customer_number'),
        (orders, 'orders', 'order_number', ['order_date', 'required_date', 'shipped_date']),
        (orders, 'order_details', ['order_number', 'order_line_number'])
    ]

    for t in tables:
        load_table(db, *t)
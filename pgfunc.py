import psycopg2

try:
    conn = psycopg2.connect("dbname= duka user=postgres password=leo.steve")
    cur = conn.cursor()
except Exception as e:
    print(e)


def fetch_data(tbln):
    try:
       q = "SELECT * FROM " + tbln + ";"
       cur.execute(q)
       records = cur.fetchall()
       return records
    except Exception as e :
        return e

def revenue_per_day():
    q = "SELECT TO_CHAR(s.time, 'DD-MM-YYYY') AS sale_month, SUM(s.quantity * p.selling_price) AS revenue FROM sales s JOIN products p ON s.pid = p.id GROUP BY TO_CHAR(s.time, 'DD-MM-YYYY');;"
    cur.execute(q)
    results = cur.fetchall()
    return results

def revenue_per_month():
    q = "SELECT TO_CHAR(s.time, 'MM-YYYY') AS sale_month, SUM(s.quantity * p.selling_price) AS revenue FROM sales s JOIN products p ON s.pid = p.id GROUP BY TO_CHAR(s.time, 'MM-YYYY');"
    cur.execute(q)
    results = cur.fetchall()
    return results



def insert_sales(v):
    vs = str(v)
    q = "insert into sales(pid,quantity,time) "\
        "values" + vs
    cur.execute(q)
    conn.commit()
    return q



def update_products(vs):
    print(vs)
    id = vs[0]
    name = vs[1]
    buying_price = vs[2]
    selling_price = vs[3]
    q = "UPDATE products SET name = %s,buying_price = %s,selling_price = %s WHERE id = %s"
    cur.execute(q, (name,buying_price,selling_price,id))
    conn.commit()
    return q


def add_custom_info(contact):
    vs = str(contact)
    q = "insert into custom_info (name, email, phone, message) VALUES (%s, %s, %s, %s);"
    "values" + vs
    cur.execute(q , contact)
    conn.commit()
    return "Request submitted successfully."
    


def insert_products(v):
    vs = str(v)
    q = "insert into products(name,buying_price,selling_price) "\
        "values" + vs
    cur.execute(q)
    conn.commit()
    return q
    


def sales_per_month():
    q = "select * from sale_per_month"
    cur.execute(q)
    results = cur.fetchall()
    return results


def sales_per_product():
    q = "select * from sale_per_product"
    cur.execute(q)
    results = cur.fetchall()
    return results


def remaining_stock():
    q = " SELECT * from remaining_stock"
    cur.execute(q)
    results = cur.fetchall()
    return results

def stockremaining(product_id=None):
    q = """  SELECT 
            
            COALESCE(s.stock_quantity, 0) - COALESCE(sa.sales_quantity, 0) AS closing_stock
            FROM
                (SELECT pid, SUM(quantity) AS stock_quantity FROM stock GROUP BY pid) AS s
            LEFT JOIN
                (SELECT pid, SUM(quantity) AS sales_quantity FROM sales GROUP BY pid) AS sa
            ON s.pid = sa.pid
            WHERE s.pid = %s
            GROUP BY s.stock_quantity,sa.sales_quantity;"""
    
    cur.execute(q,(product_id,))
    results = cur.fetchall()
    if results:
        return results[0]
    else:
        return None



def insert_stock(v):
    vs = str(v)
    q = "insert into stock(pid,quantity,time) "\
        "values" + vs
    cur.execute(q)
    conn.commit()
    return q


def add_users(full_name, email, password, confirm_password,time):
    if not all([full_name, email, password, confirm_password]):
        return "Error: Please provide all required information."

    if password != confirm_password:
        return "Error: Passwords do not match."

    q = "INSERT INTO users  (full_name, email, password, confirm_password,time) " \
        "VALUES (%s, %s, %s, %s,%s);"
    cur.execute(q, (full_name, email, password, confirm_password,time))
    conn.commit()
    return "User added successfully."






def loginn():
    q = "SELECT email, password FROM users;"
    cur.execute(q)
    results = cur.fetchall()
    return results 


def get_pid():
    q = "SELECT id FROM products;"
    cur.execute(q)
    results = cur.fetchall()
    return results
      
    



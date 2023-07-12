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
    q = "insert into products(name,buying_price,selling_price,quantity) "\
        "values" + vs
    cur.execute(q)
    conn.commit()
    return q
    


def sales_per_day():
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



def loginn(email,password):
    q = "SELECT email, password FROM users WHERE email = %s AND password = %s;"
    cur.execute(q, (email, password))
    results = cur.fetchall()
    return results 


def stockremaining():
   rem="SELECT p.id,p.name,sd.quantity - COALESCE(sum(sa.quantity), 0::bigint) AS remaining_stock FROM products p JOIN stock sd ON p.id = sd.pid LEFT JOIN sales sa ON p.id = sa.pid GROUP BY p.id, sd.quantity; "
   cur.execute(rem)
   rm=cur.fetchall()
   return(rm)


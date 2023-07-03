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

def add_users(v):
    vs = str(v)
    q = "insert into users(full_name,email, password, confirm_password, time) "\
        "values" + vs
    cur.execute(q)
    conn.commit()
    return q


def add_user(v):
    vs = str(v)
    q = "insert into users(full_name,email,password,comfirm_password,time)"\
         "values" + vs
    cur.execute(q)
    conn.commit()
    return q

def loginn(email,password):
    q = "SELECT email, password FROM users;"
    cur.execute(q)
    results = cur.fetchall()
    return results 
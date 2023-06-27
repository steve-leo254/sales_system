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
    q = "SELECT substring(TO_CHAR(time,'MM-YYYY'),1,7) as m, SUM(quantity) as total_sales FROM sales GROUP BY m ORDER BY m;"
    cur.execute(q)
    results = cur.fetchall()
    return results

def sales_per_product():
    q = " SELECT p.name, COUNT(s.*) AS total_sales FROM products p JOIN sales s ON p.id = s.pid GROUP BY p.name"
    cur.execute(q)
    results = cur.fetchall()
    return results
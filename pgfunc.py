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
    q = "insert into sales(pid,quantity,tine) "\
        "values" + vs
    cur.execute(q)
    conn.commit()
    return q

def insert_products(v):
    vs = str(v)
    q = "insert into products(name,buying_price,selling_price,stock_quantity) "\
        "values" + vs
    cur.execute(q)
    conn.commit()
    return q
    



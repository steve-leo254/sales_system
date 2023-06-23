import psycopg2

try:
    conn = psycopg2.connect("dbname=duka user=postgres password=leo.steve")
    cur = conn.cursor()
except Exception as e:
    print(e)
# conn = psycopg2.connect(
#     host="localhost",
#     database="samosa_march",
#     user="postgres",
#     password="leo.steve"



def fetch_data(tbln):
    try:
        q="SELECT * FROM " + tbln + ";"
        cur.execute(q)
        records=cur.fetchall()
        return records
    except Exception as e:
        return e
    
   
def insert_product(vs):
    try:
        q = "INSERT INTO products(name, buying_price, selling_price, quantity) VALUES (%s, %s, %s, %s)"
        cur.execute(q, vs)
        conn.commit()
        return "Product successfully added"
    except Exception as e:
        return str(e)


def insert_addproduct(v):
    try:
        q = "INSERT INTO addproducts(name, buying_price, selling_price, quantity) VALUES (%s, %s, %s, %s)"
        cur.execute(q, v)
        conn.commit()
        return "Product successfully added"
    except Exception as e:
        return str(e)


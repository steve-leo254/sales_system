from flask import Flask, render_template, request, redirect,url_for, flash ,session
from pgfunc import fetch_data, insert_products,insert_stock,remaining_stock,stockremaining,revenue_per_day,revenue_per_month
from pgfunc import fetch_data, insert_sales,sales_per_month,sales_per_product,add_users,add_custom_info,update_products,loginn,get_pid
import pygal

import psycopg2

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

import barcode
from PIL import Image
from barcode import generate
from barcode import Code128
from barcode.writer import ImageWriter
from functools import wraps

from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash, check_password_hash


# engine = create_engine("mysql+pymysql://username:leo.steve@host:port/duka")
conn = psycopg2.connect("dbname=duka user=postgres password=leo.steve")
cur = conn.cursor()
from passlib.hash import sha256_crypt
# db = scoped_session(sessionmaker(bind=engine))

from datetime import datetime, timedelta
from functools import wraps




app = Flask(__name__)
app.secret_key="leo.steve"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///duka.db' 



def login_required(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not session.get('logged_in') and not session.get('registered'):
            return redirect('/login') 
        return view_func(*args, **kwargs)
    return decorated_view




@app.route('/')
def landing():
    return render_template("landing.html")



@app.route('/index')
def home():
    return render_template("index.html")



@app.route("/register") 
def register():
   return render_template('register.html')


@app.route('/login')
def loginpage():
    return render_template('index.html')


@app.route('/signup', methods=["POST", "GET"])
def user_added():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Validation checks before registration
        if len(full_name) < 1:
            flash('Full name must be greater than 1 character.', category='error')
            return redirect("/register")
        elif len(email) < 10:
            flash('Email must be greater than 10 characters.', category='error')
            return redirect("/register")
        elif password != confirm_password:
            flash('Passwords don\'t match. Please try again', category='error')
            return redirect("/register")
        elif len(password) < 6:
            flash('Password must be at least 6 characters.', category='error')
            return redirect("/register")

        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(password)

        # To check if the email already exists in the database
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
            result = cur.fetchone()
            if result[0] > 0:
                flash('Email already exists! Please use another email!', category='error')
                return redirect("/register")
            else:
                # Adding the new user to the database, after all checks are passed.
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO users (full_name, email, password, confirm_password, time) VALUES (%s, %s, %s, %s, now())",
                        (full_name, email, hashed_password, confirm_password))
                conn.commit()
                flash('Account created successfully!', category='success')

    session['registered'] = True
    return render_template("login.html")



@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        users = loginn()
        if users:
            for user in users:
                db_email = user[0]
                db_password_hash = user[1]

                if db_email == email and check_password_hash(db_password_hash, password):
                    flash('Authentication has been successfully verified!', category='success')
                    session['logged_in'] = True
                    return redirect("/")
            else:
                flash('Incorrect email or password, please try again.', category='error')
                return redirect("/login")

    return render_template("index.html")


# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html'),404



@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out. Would you like to gain access? Kindly log in.', category='error')
    return redirect('/login')

        


@app.route('/products')
@login_required
def products():
    prods = fetch_data("products")
    return render_template('products.html', prods=prods)


@app.route('/addproducts', methods=["POST", "GET"])
def addproducts():
    if request.method == "POST":
        name = request.form["name"]
        buying_price = request.form["buying_price"]
        selling_price = request.form["selling_price"]
        products = (name, buying_price, selling_price)
        insert_products(products)
        return redirect("/products")


@app.route('/editproduct', methods=["POST", "GET"])
def edit_products():
   if request.method=="POST":
      id = request.form['id']
      name = request.form["name"]
      buying_price= request.form["buying_price"]
      selling_price=request.form["selling_price"]
      print(name)
      print(buying_price)
      print(selling_price)
      v=(id,name,buying_price,selling_price)
      update_products(v)
      return redirect("/products")
   

   

@app.route('/sales')
@login_required
def sales():
    sales = fetch_data("sales")
    prods = fetch_data("products")
    return render_template('sales.html', sales=sales, prods=prods)


@app.route('/addsales', methods=["POST", "GET"])
def addsale():
    if request.method == "POST":
        pid = request.form["pid"]
        quantity = request.form["quantity"]
        sales = ( pid, quantity,'now()')
        insert_sales(sales)
        return redirect("/sales")

    
@app.route('/dashboard')
@login_required
def dashboard():
    bar_chart = pygal.Bar()
    sp = sales_per_product()
    name = []
    sale = []
    for i in sp:
     name.append(i[0])
     sale.append(i[1])
    bar_chart.title = "Sales per Product"
    bar_chart.x_labels = name
    bar_chart.add('Sale', sale)
    bar_chart_data = bar_chart.render_data_uri()

    # Sales per month (Line Chart)
    line_chart = pygal.Line()
    daily_sales = sales_per_month()
    dates = []
    sales = []
    for i in daily_sales:
        dates.append(i[0])
        sales.append(i[1])
    line_chart.title = "Sales per Month"
    line_chart.x_labels = dates
    line_chart.add('Sales', sales)
    line_chart = line_chart.render_data_uri()


    # remaianing_stocks
    bar_chart = pygal.Bar()
    bar_chart.title = 'remaining stock'
    remain_stock = remaining_stock()
    
    name1 = []
    stock = []
    for i in remain_stock:
       name1.append(i[1])
       stock.append(i[2])
    bar_chart.x_labels = name1
    bar_chart.add('stock', stock)
    bar_chart=bar_chart.render_data_uri()
    # print(remaining_stock)

     #Graph to show revenue per day
    daily_revenue = revenue_per_day()
    dates = []
    sales_revenue_per_day = [] 
    for i in daily_revenue:
     dates.append(i[0])
    sales_revenue_per_day.append(i[1]) 
    line_chart1 = pygal.Line()
    line_chart1.title = "Revenue per Day"
    line_chart1.x_labels = dates
    line_chart1.add("Revenue(KSh)", sales_revenue_per_day)
    line_chart1 = line_chart1.render_data_uri()
    
    #Graph to show revenue per month
    monthly_revenue = revenue_per_month()
    dates = []
    sales_revenue_per_month = [] 
    for i in monthly_revenue:
     dates.append(i[0])
    sales_revenue_per_month.append(i[1]) 
    line_chart2 = pygal.Line()
    line_chart2.title = "Sales Revenue per Month"
    line_chart2.x_labels = dates
    line_chart2.add("Revenue(KSh)", sales_revenue_per_month)
    line_chart2 = line_chart2.render_data_uri()
    

    return render_template("dashboard.html", bar_chart_data=bar_chart_data, line_chart=line_chart, bar_chart=bar_chart, line_chart1=line_chart1, line_chart2=line_chart2)


@app.context_processor
def inject_stockremaining():
    def remaining_stock(product_id=None):
     stock = stockremaining(product_id)
     return stock[0] if stock is not None else int('0')

    return {'remaining_stock':remaining_stock}


@app.context_processor
def inject_datetime():
    now = datetime.now()
    return {'current_date': now.strftime('%d-%m-%Y'), 'current_time': now.strftime('%I:%M:%S %p')}



@app.route('/stock')
def stock():
    stock = fetch_data("stock")
    prods= fetch_data("products")
    return render_template('stock.html', stock=stock, prods=prods)


@app.route('/addstock', methods=["POST"])
def addstock():
   if request.method=="POST":
      pid= request.form["pid"]
      quantity=request.form["quantity"]
      stock=(pid,quantity,'now()')
      insert_stock(stock)
      return redirect("/stock")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/addcontact', methods=["POST", "GET"])
def add_contact(): 
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    message = request.form["message"]
    contact = (name, email, phone, message)
    add_custom_info(contact)
    return render_template("contact.html")




@app.context_processor
def generate_barcode():
    id_list = get_pid()
    barcode_paths = []
    for pid_tuple in id_list:
        pid = pid_tuple[0]
        code = Code128(str(pid), writer=ImageWriter())
        barcode_path = f"static/barcodes/{pid}.png"
        code.save(barcode_path)
        barcode_paths.append(barcode_path)
    return {'generate_barcode': generate_barcode}







if __name__ == "__main__":
    app.run(debug=True)
 
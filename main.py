from flask import Flask, render_template, request, redirect,url_for, flash
from pgfunc import fetch_data, insert_products,insert_stock,remaining_stock,stockremaining
from pgfunc import fetch_data, insert_sales,sales_per_day,sales_per_product,add_users,add_custom_info,update_products,loginn
import pygal
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker,session

from datetime import datetime, timedelta
from functools import wraps
conn = psycopg2.connect("dbname=duka user=postgres password=leo.steve")
cur = conn.cursor()
from werkzeug.security import generate_password_hash, check_password_hash




app = Flask(__name__)
app.secret_key="leo.steve"


@app.route('/')
def landing():
    return render_template("landing.html")




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
    return render_template("index.html")


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




@app.route('/signup', methods=["POST", "GET"])
def addusers():
   error1 = None
   if request.method=="POST":
      full_name = request.form["full_name"]
      email = request.form["email"]
      password = request.form["password"]
      confirm_password = request.form["confirm_password"]
      if password != confirm_password:
         error1 = "Passwords do not match! Please enter again."
      else:
         add_users(full_name, email, password, confirm_password,'now()')

   return render_template("register.html", error1=error1)


@app.route("/register") 
def register():
   return render_template('register.html')



@app.route('/login')
def login_page():
    return render_template('index.html')




@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out. Would you like to gain access? Kindly log in.', category='error')
    return redirect('/login')




@app.route('/index')
def home():
    if "email" in session:
        email = session["email"]
        # Do something with the user's email
        return render_template("index.html", email=email)
    else:
        flash("You are not logged in!")
        return render_template("index.html")
        


@app.route('/products')
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

    # Sales per Day (Line Chart)
    line_chart = pygal.Line()
    daily_sales = sales_per_day()
    dates = []
    sales = []
    for i in daily_sales:
        dates.append(i[0])
        sales.append(i[1])
    line_chart.title = "Sales per Month"
    line_chart.x_labels = dates
    line_chart.add('Sales', sales)
    line_chart_data = line_chart.render_data_uri()


    # remaianing_stocks
    bar_chart1 = pygal.Bar()
    bar_chart1.title = 'remaining stock'
    remain_stock = remaining_stock()
    
    name1 = []
    stock = []
    for i in remain_stock:
       name1.append(i[1])
       stock.append(i[2])
    bar_chart1.x_labels = name1
    bar_chart1.add('stock', stock)
    bar_chart1=bar_chart1.render_data_uri()
    # print(remaining_stock)

    return render_template("dashboard.html", bar_chart_data=bar_chart_data, line_chart_data=line_chart_data, bar_chart1=bar_chart1)


@app.context_processor
def inject_stockremaining():
    def remaining_stock(product_id=None):
     stock = stockremaining(product_id)
     return stock[0] if stock is not None else int('0')

    return {'remaining_stock':remaining_stock}




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




if __name__ == "__main__":
    app.run(debug=True)
 
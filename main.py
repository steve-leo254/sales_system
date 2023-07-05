from flask import Flask, render_template, request, redirect,url_for
from pgfunc import fetch_data, insert_products
from pgfunc import fetch_data, insert_sales, insert_products,sales_per_day,sales_per_product,add_users,loginn,add_custom_info
import pygal






app = Flask(__name__)
# app.secret_key="Mombasa.Kamundi"


@app.route('/')
def landing():
    return render_template("landing.html")


@app.route('/index')
def home():
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
        quantity = request.form["quantity"]
        products = (name, buying_price, selling_price,quantity)
        insert_products(products)
        return redirect("/products")
    

@app.route('/sales')
def sales():
    sales = fetch_data("sales")
    return render_template('sales.html', sales=sales)


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

    return render_template("dashboard.html", bar_chart_data=bar_chart_data, line_chart_data=line_chart_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error2 = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = loginn(email,password)
        if user:
          for i in user:
                db_email = i[0]
                db_password = i[1]
          if db_password== password and db_email== email:
             return redirect("/index")
          else:
             error2 = "Invalid password or email. Please try again Pal."
            #  return render_template("login.html", error2)
        else:
            error2 = "Account not found. Please register first."
    return render_template("login.html", error2=error2)   

@app.route('/register')
def register():
    return render_template('register.html')



@app.route('/signup', methods=["POST", "GET"])
def addusers():
   error1 = None
   if request.method=="POST":
      full_name= request.form["full_name"]
      email=request.form["email"]
      password=request.form["password"]
      confirm_password=request.form["confirm_password"]
      if password != confirm_password:
         error1 = "password do not match! please enter again."

   users=(full_name,email,password,confirm_password,'now()')
   add_users(users)
   return render_template("register.html", error1=error1)



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
 
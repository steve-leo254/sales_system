from flask import Flask, render_template, request, redirect,url_for
from pgfunc import fetch_data, insert_products,insert_stock ,remaining_stock,stockremaining
from pgfunc import fetch_data, insert_sales,sales_per_day,sales_per_product,add_users,loginn,add_custom_info,update_products
import pygal






app = Flask(__name__)
# app.secret_key="Mombasa.Kamundi"


@app.route('/')
def landing():
    return render_template("landing.html")

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
      full_name = request.form["full_name"]
      email = request.form["email"]
      password = request.form["password"]
      confirm_password = request.form["confirm_password"]
      if password != confirm_password:
         error1 = "Passwords do not match! Please enter again."
      else:
         add_users(full_name, email, password, confirm_password,'now()')

   return render_template("register.html", error1=error1)


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
 
from flask import Flask, render_template, request, redirect
from pgfunc import fetch_data, insert_products
from pgfunc import fetch_data, insert_sales, insert_products,sales_per_day,sales_per_product
import pygal


app = Flask(__name__)

@app.route("/")
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
    line_chart.title = "Sales per Day"
    line_chart.x_labels = dates
    line_chart.add('Sales', sales)
    line_chart_data = line_chart.render_data_uri()

    return render_template("dashboard.html", bar_chart_data=bar_chart_data, line_chart_data=line_chart_data)




if __name__ == "__main__":
    app.run(debug=True)

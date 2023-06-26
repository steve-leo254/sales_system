from flask import Flask, render_template, request, redirect
from pgfunc import fetch_data, insert_products
from pgfunc import fetch_data, insert_sales, insert_products
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
    
@app.route('/sales_amount')
def sales_amount():
    # Sales per Product (Bar Chart)
    bar_chart = pygal.Bar()
    bar_chart.title = 'Sales per Product'
    product_names = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    sales_data = [250, 500, 350, 200, 400]
    bar_chart.x_labels = product_names
    bar_chart.add('Sales', sales_data)
    bar_chart_data = bar_chart.render_data_uri()

    # Sales per Day (Line Chart)
    line_chart = pygal.Line()
    line_chart.title = 'Sales per Day'
    # Query your table to get the data for x-axis (created_at) and y-axis (sales) for each day
    # Assuming you have the data as two separate lists: dates and sales_per_day
    dates = ['2023-06-01', '2023-06-02', '2023-06-03', '2023-06-04', '2023-06-05']
    sales_per_day = [100, 150, 200, 180, 250]
    line_chart.x_labels = dates
    line_chart.add('Sales', sales_per_day)
    line_chart_data = line_chart.render_data_uri()

    return render_template("sales_amount.html", bar_chart_data=bar_chart_data, line_chart_data=line_chart_data)




if __name__ == "__main__":
    app.run(debug=True)

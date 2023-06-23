from flask import Flask, render_template, request, redirect
from pgfunc import fetch_data, insert_products
from pgfunc import fetch_data, insert_sales, insert_products


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
        id = request.form["id"]
        pid = request.form["pid"]
        quantity = request.form["quantity"]
        time = request.form["time"]
        sales = (id, pid, quantity, time)
        insert_sales(sales)
        return redirect("/sales")
    

if __name__ == "__main__":
    app.run(debug=True)

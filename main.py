from flask import Flask ,render_template,request,redirect
from main2 import insert_product,fetch_data


#create an object called app
#__name__ is used to tell flask where to access html files
#all htmls files are put inside templates folder
#all css/js/images are put inside static folder
app = Flask(__name__)

#A route is an extension of urlwhich loads you an html page
#techcamp.co.ke/



@app.route("/")
def home():
    return render_template("index.html")




@app.route('/products')
def products():
    prods = fetch_data("products")
    return render_template('products.html', prods=prods)

@app.route('/addproducts', methods=["POST","GET"])
def addproducts():
    if request.method == "POST":
        name = request.form["name"]
        buying_price = request.form["buying_price"]
        selling_price = request.form["selling_price"]
        quantity = request.form["quantity"]
        print(name)
        print(buying_price)
        print(selling_price)
        print(quantity)
        products = (name, buying_price, selling_price, quantity)
        insert_product(products)
        return redirect("/products")


if __name__ == "__main__":
    app.run(debug=True)


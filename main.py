from flask import Flask ,render_template
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
def products ():
    prods =fetch_data("products")
    return render_template('products.html', prods=prods)

@app.route('/sales')
def sales():
    sales = fetch_data("sales")
    return render_template('sales.html', sales=sales)

app.run()

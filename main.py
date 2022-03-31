
from enum import auto
from inspect import EndOfBlock
from ntpath import join
from re import S
from tkinter.font import names
from turtle import end_fill
from flask import Flask, render_template, redirect, request
import psycopg2
from datetime import date, datetime
#create an object
app = Flask(__name__)

conn = psycopg2.connect(user= "postgres",password="JMKag0th0@2oo!",port="5432",database="myduka")
cur = conn.cursor()

#create home route
@app.route("/", methods=['GET', 'POST'])
def home_page():
    username = 'Techcamp Kenya'
    return render_template('index.html', name = username)


@app.route("/inventory", methods=['GET', 'POST'])
def inventory():    
    if request.method=="POST":  
        productname=request.form["pname"]
        buyingprice= request.form["bprice"]
        sellingprice= request.form["sprice"]
        quantity= request.form["quantity"]
        
        
        cur.execute(" insert into products (name,buying_price,selling_price,stock_quantity) values(%s,%s,%s,%s)" , (productname,buyingprice,sellingprice,quantity))    
        conn.commit()
        return redirect("/inventory")
    
    else:
        cur.execute("select * from products")
        data = cur.fetchall()
        for i in data:
            end_fill
        return render_template("inventory.html", dt=data)
    

@app.route("/make_sale", methods = ["GET", "POST"])
def make_sale():
    pid = request.form['productid']
    quantity = request.form["purch"]
    created_at ="NOW(())"
    
    cur.execute(" insert into sales (pid,quantity,created_at)  values(%s,%s,%s)" , (pid,quantity,created_at))
    conn.commit()
    return redirect("/inventory")

@app.route("/sales/<int:prid>")
def sales(prid):
    cur.execute("select * from sales where pid = %s ", [prid])
    sales = cur.fetchall()
    return render_template('sales.html', s = sales)

@app.route("/sales")
def salestotal():
    cur.execute("select * from sales")
    sales = cur.fetchall()
    return render_template('sales.html', s = sales)



@app.route('/dashboard')
def dashboard():    
    cur.execute("select count(id) from products")
    total_sales = cur.fetchone()
    cur.execute("select count(id) from sales")    
    total_products = cur.fetchone()    
    print(total_products)
    cur.execute('select sum((products.selling_price - products.buying_price) * sales.quantity) as profit, products.name from sales join products on products.id=sales.pid GROUP BY products.name')
    graph = cur.fetchall()
    product_name=[]
    profit=[]
    for i in graph:
        product_name.append(i[1])
        profit.append(i[0])
    return render_template('dashboard.html',total_products = total_products[0], total_sales = total_sales[0], product_name = product_name,profit=profit)



if __name__ == "__main__":
    app.run(debug=True)
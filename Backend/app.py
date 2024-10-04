from flask import Flask,render_template,redirect,url_for,request,flash,render_template_string
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Stock import Stock
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'AodShabuMookrata'

stock = Stock()

Menu = [] 

@app.route('/')
def home():
    return redirect(url_for('booktable'))

@app.route('/admin/booktable')
def booktable():
    return render_template("bookTable.html")

@app.route('/admin/stock')
def _stock():
    stock_items = stock.inOrder()
    return render_template('stock.html', stock_items=stock_items)

@app.route('/admin/stock/addstock')
def addStock():
    return render_template("addStock.html")

@app.route('/admin/stock/addstock',methods=['GET','POST'])
def AddMenu():
    try:
        id = int(request.form['id'])
        name = request.form['name']
        number = int(request.form['num'])

        img_file = request.files['img']
        if img_file:
            filename = secure_filename(img_file.filename)

            # ตรวจสอบว่ามีโฟลเดอร์ static/images แล้วหรือไม่
            img_directory = os.path.join('static', 'images')
            if not os.path.exists(img_directory):
                os.makedirs(img_directory)

            img_path = os.path.join(img_directory, filename)
            img_file.save(img_path)

        # เพิ่มข้อมูลใหม่เข้า stock
        inserted = stock.insert(id, name, number, filename)
        if inserted:
            flash("Stock item added successfully!", "success")
            return redirect(url_for('_stock'))
        else:
            flash("ID already exists!", "error")
            return redirect(url_for('addStock'))

    except ValueError:
        flash("Invalid input. Please enter valid numbers.", "error")
        return redirect(url_for('addStock'))
        
@app.route('/admin/queue')
def queue():
    return render_template("queue.html")

@app.route('/table1')
def table1():
    stock_items = stock.inOrder()
    return render_template("table4.html",stock_items=stock_items)


@app.route('/table2')
def table2():
    stock_items = stock.inOrder()
    return render_template("table4.html",stock_items=stock_items)


@app.route('/table3')
def table3():
    stock_items = stock.inOrder()
    return render_template("table4.html",stock_items=stock_items)


@app.route('/table4')
def table4():
    stock_items = stock.inOrder()
    return render_template("table4.html",stock_items=stock_items)

@app.route('/table5')
def table5():
    stock_items = stock.inOrder()
    return render_template("table4.html",stock_items=stock_items)



if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0')
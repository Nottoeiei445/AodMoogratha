from flask import Flask,render_template,redirect,url_for
app = Flask(__name__)

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/')
def home():
    return redirect(url_for('admin'))

@app.route('/admin/booktable')
def booktable():
    return render_template("bookTable.html")

@app.route('/admin/stock')
def stock():
    return render_template("stock.html")

@app.route('/admin/stock/addstock')
def addStock():
    return render_template("addStock.html")

@app.route('/admin/queue')
def queue():
    return render_template("queue.html")

@app.route('/table1')
def table1():
    return render_template("table1.html")

@app.route('/table2')
def table2():
    return render_template("table2.html")

@app.route('/table3')
def table3():
    return render_template("table3.html")

@app.route('/table4')
def table4():
    return render_template("table4.html")

@app.route('/table5')
def table5():
    return render_template("table5.html")


if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0' ) #,host = '0.0.0.0'
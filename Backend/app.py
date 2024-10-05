from flask import Flask,render_template,redirect,url_for,request,flash,render_template_string
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Backend import Backend
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'AodShabuMookrata'

backend = Backend(5)

Menu = [] 

@app.route('/')
def home():
    return redirect(url_for('booktable'))

@app.route('/admin/booktable')
def booktable():
    return render_template("bookTable.html")

@app.route('/admin/stock')
def _stock():
    stock_items = backend.inOrderStock() 
    return render_template('stock.html', stock_items=stock_items) #ส่งไปที่หน้า stock.html

@app.route('/admin/stock/searchstock',methods=['GET'])
def searchStock():
    try: 
        id = int(request.args.get('id'))

        searchstock = backend.searchStock(id)
        if searchstock:
            stock_items = [searchstock]  # หากพบสินค้า ให้ส่งสินค้าเดียวนั้นกลับไปแสดงผล
            flash("Found here!", "success")
            return render_template('stock.html', stock_items=stock_items)  # ส่งผลการค้นหากลับไปที่หน้า stock.html
        elif id=="":
            return render_template('stock.html', stock_items=stock_items)
        
        else:
            flash("ID is not exist", "error")
            return redirect(url_for('_stock'))  # ถ้าไม่พบสินค้าจะกลับไปที่หน้า stock ทั้งหมด
    except ValueError:
        flash("Invalid input. Please enter valid numbers.", "error")
        return redirect(url_for('_stock'))


@app.route('/admin/stock/addstock') 
def addStock(): #METHOD แสดงหน้า addstock.html
    return render_template("addStock.html")

@app.route('/admin/stock/addstock/insertstock',methods=['GET','POST']) 
def AddMenu(): #method รับค่า
    try:
        id = int(request.form['id']) #รับ id
        name = request.form['name'] #รับ name
        number = int(request.form['num']) #รับ num

        img_file = request.files['img'] #รับ img
        if img_file:
            filename = secure_filename(img_file.filename)
            # ไม่บันทึกไฟล์ลงในเครื่อง แค่เก็บชื่อไฟล์ในฐานข้อมูล

        # เพิ่มเมนูใหม่เข้า stock พร้อมชื่อไฟล์รูปภาพ (ถ้ามี)  
        inserted = backend.insertStock(id, name, number, filename)# เพิ่มเมนูใหม่เข้า stock

        if inserted:
            flash("Stock item added successfully!", "success")
            return redirect(url_for('_stock'))
        else:
            flash("ID already exists!", "error")
            return redirect(url_for('addStock'))

    except ValueError:
        flash("Invalid input. Please enter valid numbers.", "error")
        return redirect(url_for('addStock'))
    
@app.route('/admin/stock/updateqty',methods=['PUT'])
def updateQTY():
    try:
        id = int(request.form['id'])
        number = int(request.form['num'])

        updateQTY = backend.updateQTY(id,number)
        if  updateQTY:
            flash("Update Successfully","success")
            return redirect(url_for("_stock"))
        else:
            flash("ID is not exist","error")
            return redirect(url_for('updateqty'))
    except ValueError:
        flash("Invalid input. Please enter valid numbers.", "error")
        return redirect(url_for('updateqty'))

@app.route('/admin/stock/updateimg',methods=['PUT'])
def updateIMG():
    try:
        id = int(request.form['id']) #รับ id
        img_file = request.files['img'] #รับ img
        if img_file: #เซฟไฟล์รูปภาพ
            filename = secure_filename(img_file.filename)

            # ตรวจสอบว่ามีโฟลเดอร์ static/images แล้วหรือไม่
            img_directory = os.path.join('static', 'images')
            if img_file:
                filename = secure_filename(img_file.filename)
            # ไม่บันทึกไฟล์ลงในเครื่อง แค่เก็บชื่อไฟล์ในฐานข้อมูล

        
        updateIMG = backend.updateIMG(id,filename)

        if updateIMG:
            flash("Update Image Succesfully!", "success")
            return redirect(url_for('_stock'))
        else:
            flash("ID is not exists!", "error")
            return redirect(url_for('updateimg'))

    except ValueError:
        flash("Invalid input. Please enter valid numbers.", "error")
        return redirect(url_for('updateimg'))
    
@app.route('/admin/stock/delete', methods=['DELETE'])
def delete_stock():
    try:
        id = int(request.form['id'])  # รับ ID ของสินค้าที่ต้องการลบ
        
        # เรียก backend เพื่อลบ stock item ที่มี id ตรงกับที่ส่งมา
        delete_status = backend.deleteStock(id)

        if delete_status:
            flash("Stock item deleted successfully!", "success")
        else:
            flash("ID does not exist!", "error")
        
        return redirect(url_for('_stock'))

    except ValueError:
        flash("Invalid input. Please enter a valid ID.", "error")
        return redirect(url_for('_stock'))


    
@app.route('/admin/queue')
def queue():
    return render_template("queue.html")

@app.route('/admin/queue/enqueue', methods=['GET', 'POST'])
def enqueue():
    stock_items = backend.inOrderStock()  # ดึงข้อมูลสินค้าทั้งหมดจาก stock
    for item in stock_items:
        id = item['ID']  # กำหนดค่า id จากสินค้าในลูป
        qty = request.form.get(f'num_{id}', default=0, type=int)  # ดึงค่าจำนวนที่สั่งจากฟอร์ม

        # ตรวจสอบว่าจำนวนที่สั่งมากกว่า 0 ก่อนที่จะ enqueue
        if qty > 0:
            enqueue_ = backend.enqueue(1, id, qty)  # สั่งซื้อสินค้าลงคิว (table id ถูกกำหนดเป็น 1 สำหรับการทดสอบ)

            # ตรวจสอบผลลัพธ์จากการ enqueue
            if enqueue_ == "Enqueue Success!!":
                flash(f"Stock item ID {id} added to queue successfully!", "success")
                return render_template("queue.html",enqueue=enqueue_)
            else:
                flash(enqueue, "error")


@app.route('/table1')
def _table1():
    stock_items = backend.inOrderStock()
    return render_template("table1.html",stock_items=stock_items)


@app.route('/table2')
def table2():
    stock_items = backend.inOrderStock()
    return render_template("table2.html",stock_items=stock_items)


@app.route('/table3')
def table3():
    stock_items = backend.inOrderStock()
    return render_template("table3.html",stock_items=stock_items)


@app.route('/table4')
def table4():
    stock_items = backend.inOrderStock()
    return render_template("table4.html",stock_items=stock_items)

@app.route('/table5')
def table5():
    stock_items = backend.inOrderStock()
    return render_template("table5.html",stock_items=stock_items)



if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0')
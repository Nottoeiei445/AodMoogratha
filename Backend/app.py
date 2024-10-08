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
    displaytable = backend.displayTable()
    return render_template("bookTable.html",display = displaytable)

@app.route('/admin/booktable',methods = ['GET','POST'])
def _booktable():
    try:
        customer = int(request.form['customer'])
        table = int(request.form['table'])

        bookTable = backend.book_table(table,customer)

        display = backend.displayTable()
   
        if bookTable:
            return  render_template("bookTable.html",display=display)
    except ValueError:
        flash("Invalid input. Please enter valid numbers.", "error")
        return redirect(url_for('booktable'))

@app.route('/admin/booktable/cleartable',methods= ['POST'])
def clear_table():
    try:
        table_clear = int(request.form['table_clr'])  # รับหมายเลขโต๊ะจากฟอร์ม
        clear_status = backend.clear_table(table_clear)  # เรียก backend เพื่อเคลียร์โต๊ะ

        if clear_status:
            flash(f"Table {table_clear} has been cleared successfully.", "success")
        else:
            flash(f"Table {table_clear} is already available or does not exist.", "error")

        return redirect(url_for('booktable'))  # กลับไปยังหน้ารายการโต๊ะ
    except ValueError:
        flash("Invalid input. Please enter a valid table number.", "error")
        return redirect(url_for('booktable'))
@app.route('/admin/booktable/searchtable',methods=['POST'])
def searchtable():
    try:
        table = int(request.form['table'])
        search = backend.searchTable(table)
        if search:
            display = [search]
            flash(f"Here is Table {table} ")
            return render_template('booktable.html', display = display)
        else:
            flash(f"No have table {table} ")
    except:
        return redirect(url_for('booktable'))
        
@app.route('/admin/boktable/filtertable',methods=['GET','POST'])
def filtertable():
    try:
        filter_ = request.form.get('filter')
        if filter_ == 'All':
            displayfilter = backend.displayTable()
        elif filter_ == 'Booked':
            displayfilter = backend.displayBook()
        elif filter_ =='UnBooked':
            displayfilter = backend.displayUnBook()
        return render_template('booktable.html',display = displayfilter)
    except:
        return redirect(url_for('booktable'))

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
        
        return render_template()

    except ValueError:
        flash("Invalid input. Please enter a valid ID.", "error")
        return redirect(url_for('_stock'))
    
@app.route('/admin/queue')
def queue():
    queue_items = backend.displayQueue()  
    return render_template('queue.html', enqueue_=queue_items)

@app.route('/admin/queue/enqueue', methods=['GET', 'POST'])
def enqueue():
    stock_items = backend.inOrderStock()  # ดึงข้อมูลสินค้าทั้งหมดจาก stock
    queue_items = backend.displayQueue()  # ดึงรายการคิวเริ่มต้น
    
    for item in stock_items:
        id = item['ID']  # กำหนดค่า id จากสินค้าในลูป
        qty = request.form.get(f'num_{id}', default=0, type=int)  # ดึงค่าจำนวนที่สั่งจากฟอร์ม
        table = request.form.get('table')
        table = int(table)
        
        # ตรวจสอบว่า qty ต้องมากกว่า 0 และสินค้ามีจำนวนเพียงพอ
        if qty > 0:
            # ตรวจสอบก่อนว่าสินค้าในสต็อกมีเพียงพอหรือไม่
            stock_item = backend.searchStock(id)
            queue_items = backend.displayQueue()

            # เข้าถึง attributes ของ stock_item โดยตรง แทนการใช้ subscript []
            if stock_item and stock_item.QTY >= qty:
                enqueue_ = backend.enqueue(table, id, qty)  # สั่งซื้อสินค้าลงคิว (table id ถูกกำหนดเป็น 1 สำหรับการทดสอบ)
                if enqueue_ == "Enqueue Success!!":  # ถ้าสำเร็จ
                    flash(f"Successfully added {qty} of item ID: {id} to queue.", "success")
                else:
                    flash(f"Failed to enqueue item ID: {id}. Reason: {enqueue_}", "error")
            else:
                flash(f"Insufficient stock for item ID: {id}", "error")
                
    return redirect(url_for('displayQueue'))

@app.route('/admin/queue/dequeue', methods=['POST'])
def dequeue():
    item = backend.dequeue()  # เรียกใช้ฟังก์ชัน dequeue
   

    # ตรวจสอบว่า item ไม่ใช่ None ก่อนที่จะเข้าถึงแอตทริบิวต์
    if item is not None:
        # ในที่นี้ item เป็น queueNum ซึ่งเป็นตัวเลข ไม่ใช่ object ของ Node
        flash(f"Dequeued item from queue number: {item}", "success")
    else:
        flash("Queue is empty, nothing to dequeue.", "error")

    # หลังจาก dequeue แล้วให้ redirect กลับไปที่หน้า queue โดยไม่ให้เกิดการเพิ่มข้อมูลใหม่
    return redirect(url_for('queue'))

@app.route('/displayqueue')
def displayQueue():
    queue_items = backend.displayQueue()  # อัปเดตคิวจาก backend
    return render_template("displayqueue.html", enqueue_=queue_items)

@app.route('/table1')
def table1():
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
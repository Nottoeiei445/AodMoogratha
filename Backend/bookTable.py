# Backend/booktable.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.lib.pagesizes import mm
import datetime
import os


class Node:
    def __init__(self, tableNum, customerNum, status):
        # โต๊ะที่ :
        self.tableNum = tableNum
        # จำนวนลูกค้า : 
        self.customerNum = customerNum
        # สถานะการจอง :
        self.status = status
        self.prev = None
        self.next = None

class BookTable:
    # Constructor
    def __init__(self, maxTable):
        self.first = None
        self.maxTable = maxTable
        for i in range(maxTable):
            self.insert()

    # ยัดโต๊ะเข้าไป
    def insert(self):
        if self.first is None:
            new_node = Node(1, 0, False)
            self.first = new_node
            return
        
        last = self.first
        i = 2
        while last.next:
            last = last.next
            i += 1
        new_node = Node(i, 0, False)
        last.next = new_node
        new_node.prev = last

    # จองโต๊ะ
    def book_table(self, table, customer):
        ptr = self.first
        if table > self.maxTable or table < 1:
            return f"Table {table} does not exist."
        if ptr is None:
            return "No tables available."
        
        while ptr and ptr.tableNum != table:
            ptr = ptr.next
        
        if ptr and not ptr.status:
            ptr.status = True
            ptr.customerNum = customer
            return f"Table {table} successfully booked for {customer} customer(s)."
        elif ptr and ptr.status:
            return f"Table {table} is already booked!"
        else:
            return "Table not found."

    # ล้างโต๊ะ
    def clear_table(self, table):
        ptr = self.first
        if table > self.maxTable or table < 1:
            return f"Table {table} does not exist."
        if ptr is None:
            return "No tables available."
        
        while ptr and ptr.tableNum != table:
            ptr = ptr.next
        
        if ptr and ptr.status:
            price = ptr.customerNum * 599
            # เรียกใช้ฟังก์ชัน generate_receipt เพื่อสร้างใบเสร็จ
            receipt = self.generate_receipt(ptr.tableNum, ptr.customerNum, price)
            ptr.customerNum = 0
            ptr.status = False
            return f"Table {table} cleared. Total price: {price} THB.\n{receipt}"
        elif ptr and not ptr.status:
            return f"Table {table} is not booked yet!"
        else:
            return "Table not found."
        

    def generate_receipt(self, tableNum, customerNum, totalPrice):
        # ตั้งชื่อไฟล์ใบเสร็จ
        receipt_name = f"receipt_table_{tableNum}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # กำหนดขนาดกระดาษเป็น 58x80 มม.
        receipt_width, receipt_height = (58 * mm, 80 * mm)

        # สร้าง canvas สำหรับ PDF ด้วยขนาด 58x80 มม.
        c = canvas.Canvas(receipt_name, pagesize=(receipt_width, receipt_height))
        
        # หาตำแหน่งโฟลเดอร์ฟอนต์แบบ relative
        font_folder = os.path.join(os.path.dirname(__file__), 'Font')

        # ระบุ path ฟอนต์
        regular_font_path = os.path.join(font_folder, 'Sarabun-Regular.ttf')
        bold_font_path = os.path.join(font_folder, 'Sarabun-Bold.ttf')

        # ลงทะเบียนฟอนต์ภาษาไทย
        pdfmetrics.registerFont(TTFont('THSarabunNew', regular_font_path))
        pdfmetrics.registerFont(TTFont('THSarabunNew-Bold', bold_font_path))
        
        # ตั้งค่าฟอนต์ภาษาไทยและขนาด
        c.setFont("THSarabunNew-Bold", 12)
        
        # เริ่มจัดการวางข้อความในตำแหน่งที่เหมาะสมสำหรับใบเสร็จ
        c.drawString(10, receipt_height - 20, f"โต๊ะ: {tableNum}")
        
        # ข้อมูลร้าน
        c.setFont("THSarabunNew", 10)
        c.drawString(10, receipt_height - 35, "อ๊อดชาบูหมูกระทะ")
        c.drawString(10, receipt_height - 50, "(ประตู 0 ม.นเรศวร)")
        c.drawString(10, receipt_height - 65, "ซอย : ไม่ทราบ")
        c.drawString(10, receipt_height - 80, "โทร: 0916182945")
        
        # วาดเส้นคั่น
        c.line(5, receipt_height - 90, 53 * mm, receipt_height - 90)
        
        # ข้อความใบแจ้งหนี้
        c.setFont("THSarabunNew-Bold", 12)
        c.drawString(10, receipt_height - 105, "ใบแจ้งหนี้")
        
        # ข้อมูลโต๊ะ
        c.setFont("THSarabunNew", 10)
        c.drawString(10, receipt_height - 120, f"โต๊ะ: {tableNum}")
        c.drawString(10, receipt_height - 135, f"วันที่: {datetime.datetime.now().strftime('%d/%m/%Y')}")
        c.drawString(35 * mm, receipt_height - 135, f"เวลา: {datetime.datetime.now().strftime('%H:%M:%S')}")
        
        # รายละเอียดการสั่ง
        c.drawString(10, receipt_height - 150, f"{customerNum} บุฟเฟ่ต์ 599")
        c.drawString(35 * mm, receipt_height - 150, f"{totalPrice} บาท")
        
        # วาดเส้นคั่น
        c.line(5, receipt_height - 160, 53 * mm, receipt_height - 160)
        
        # รวมยอด
        c.setFont("THSarabunNew-Bold", 10)
        c.drawString(10, receipt_height - 175, "รวม:")
        c.drawString(35 * mm, receipt_height - 175, f"{totalPrice} บาท")
        
        # ยอดสุทธิ
        c.drawString(10, receipt_height - 190, "ยอดสุทธิ:")
        c.drawString(35 * mm, receipt_height - 190, f"{totalPrice} บาท")
        
        # วาดเส้นคั่น
        c.line(5, receipt_height - 200, 53 * mm, receipt_height - 200)
        
        # ข้อความขอบคุณ
        c.setFont("THSarabunNew", 8)
        c.drawString(10, receipt_height - 215, "ขอบคุณที่ใช้บริการ")
        
        # บันทึก PDF
        c.showPage()
        c.save()
        
        return f"Receipt generated: {receipt_name}"

    def searchTable(self,table):
        ptr = self.first
        if ptr is None:
            return None
        while table is not ptr.tableNum:
            ptr = ptr.next
        return ptr
        

    # แสดงรายการทั้งหมด
    def display(self):
        tables = []
        current = self.first
        while current:
            tables.append({
                'tableNum': current.tableNum,
                'customerNum': current.customerNum,
                'status': current.status
            })
            current = current.next
        return tables
    
    # แสดงเฉพาะโต๊ะที่จองแล้ว
    def displayBooked(self):
        tables = []
        current = self.first
        while current:
            if current.status is True:
                tables.append({
                    'tableNum': current.tableNum,
                    'customerNum': current.customerNum,
                    'status': current.status
                })
            current = current.next
        return tables
    
    # แสดงเฉพาะโต๊ะที่ยังไม่จอง
    def displayUnBooked(self):
        tables = []
        current = self.first
        while current:
            if current.status is False:
                tables.append({
                    'tableNum': current.tableNum,
                    'customerNum': current.customerNum,
                    'status': current.status
                })
            current = current.next
        return tables

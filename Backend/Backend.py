from bookTable import BookTable
from Stock import Stock
from QueueList import QueueList

class Backend:
    def __init__(self,maxTable):
        self.table = BookTable(maxTable)
        self.stock = Stock()
        self.queue = QueueList()
    
    #Table 
    def displayTable(self):
        return self.table.display()
    
    def book_table(self,table,customer):
        return self.table.book_table(table,customer)

    def clear_table(self,table):
        return self.table.clear_table(table)
    
    def searchTable(self,table):
        return self.table.searchTable(table)
    
    def displayTable(self):
        return self.table.display()
    
    def displayBook(self):
        return self.table.displayBooked()
    
    def displayUnBook(self):
        return self.table.displayUnBooked()
    
    #Stock
    def insertStock(self, ID, Name, QTY, IMG):
        searchNode = self.stock.search(ID)
        if searchNode is None:
            self.stock.insert(ID,Name,QTY,IMG)
            return "Add Success!!"
        else:
            return "ID is already exist"
        
    def searchStock(self, ID):
        return self.stock.search(ID)
    
    def inOrderStock(self):
        return self.stock.inOrder()
    
    def updateQTY(self, ID, QTY):
        searchNode = self.stock.search(ID)
        if searchNode is None:
            return "ID is not exist"
        else:
            return self.stock.updateQTY(ID,QTY)
        
    def deleteStock(self, ID):
        searchNode = self.stock.search(ID)
        if searchNode is None:
            return "ID is not exist."
        else:
            return self.stock.delete(ID)
    
    
    #Queue
    def enqueue(self,table,ID,qty):
        searchTable = self.table.searchTable(table)
        if searchTable is None:
            return "We don't have that table"
        elif searchTable.status == False:
            return "This table is not booked yet" 
        #ถ้าไม่ว่าง Return ข้อความ
        else:
            searchStock = self.stock.search(ID)
            if searchStock is None:
                return "We dont have that ID's menu"
            else:
                if searchStock.QTY < qty:
                    return "We don't have enough"
                else:
                    self.queue.enqueue(table,ID,qty)
                    searchStock.QTY -= qty
                    return "Enqueue Success!!"

    def dequeue(self):
        return self.queue.dequeue()
      

    def displayQueue(self):
        return self.queue.display()


if __name__ == "__main__":
    # Initialize Backend with max table of 5
    be = Backend(5)

    # --- Table Booking Tests ---
    print("=== Table Booking Tests ===")
    
    # Book tables
    print("Booking table 1 for customer 101")
    print(be.book_table(1, 101))  # Should book successfully
    print("Booking table 2 for customer 102")
    print(be.book_table(2, 102))  # Should book successfully
    print("Booking table 1 for customer 103")
    print(be.book_table(1, 103))  # Should fail (already booked)
    
    # Display all tables
    print("\nAll Tables:")
    for item in be.displayTable():
        print(f"Table {item['tableNum']} | Customer {item['customerNum']} | Status {item['status']}")
    
    # Display booked tables
    print("\nBooked Tables:")
    for item in be.displayBook():
        print(f"Table {item['tableNum']} | Customer {item['customerNum']} | Status {item['status']}")

    # Clear table 1
    print("\nClearing table 1")
    print(be.clear_table(2))

    # Display unbooked tables
    print("\nUnbooked Tables:")
    for item in be.displayUnBook():
        print(f"Table {item['tableNum']} | Customer {item['customerNum']} | Status {item['status']}")

    # Search table
    print("\nSearching table 1")
    search_result = be.searchTable(1)
    if search_result is not None:
        print(f"Table {search_result.tableNum} | Status {search_result.status}")

    # --- Stock Management Tests ---
    print("\n=== Stock Management Tests ===")
    
    # Insert stock items
    print("Inserting stock item ID 1")
    print(be.insertStock(1, "Item 1", 10, "image1.png"))  # Success
    print("Inserting stock item ID 2")
    print(be.insertStock(2, "Item 2", 5, "image2.png"))   # Success
    print("Inserting duplicate stock item ID 1")
    print(be.insertStock(1, "Item Duplicate", 20, "image3.png"))  # ID exists, should fail

    # Display stock in order
    print("\nStock in order:")
    for item in be.inOrderStock():
        print(f"ID: {item['ID']} | Name: {item['Name']} | QTY: {item['QTY']} | IMG: {item['IMG']}")

    # Update quantity of stock item ID 1
    print("\nUpdating stock quantity for ID 1 to 50")
    print(be.updateQTY(1, 50))

    # Attempt to update quantity of non-existing stock item ID 999
    print("\nUpdating stock quantity for ID 999 to 50")
    print(be.updateQTY(999, 50))

    # Display updated stock
    print("\nStock after update:")
    for item in be.inOrderStock():
        print(f"ID: {item['ID']} | Name: {item['Name']} | QTY: {item['QTY']} | IMG: {item['IMG']}")

    # Delete stock item ID 2
    print("\nDeleting stock item ID 2")
    print(be.deleteStock(2))

    # Attempt to delete non-existing stock item ID 999
    print("\nDeleting stock item ID 999")
    print(be.deleteStock(999))

    # Display stock after deletion
    print("\nStock after deletion:")
    for item in be.inOrderStock():
        print(f"ID: {item['ID']} | Name: {item['Name']} | QTY: {item['QTY']} | IMG: {item['IMG']}")

    # --- Queue Management Tests ---
    print("\n=== Queue Management Tests ===")
    
    # Enqueue order for table 1, menu item 1 with quantity 2
    print("Enqueue order for table 1, menu item 1, quantity 2")
    print(be.enqueue(1, 1, 2))  # Success
    
    # Enqueue order for table 1, menu item 2 with quantity 1
    print("Enqueue order for table 1, menu item 2, quantity 1")
    print(be.enqueue(1, 2, 1))  # Success

    # Display queue
    print("\nQueue:")
    for item in be.displayQueue():
        print(f"Table: {item['table']} | Menu: {item['ID']} | QTY: {item['qty']}")
    
    # Dequeue order
    print("\nDequeue an order")
    print(be.dequeue())  # Should return the first order in the queue
    
    # Display updated queue
    print("\nQueue after dequeue:")
    for item in be.displayQueue():
        print(f"Table: {item['table']} | Menu: {item['ID']} | QTY: {item['qty']}")

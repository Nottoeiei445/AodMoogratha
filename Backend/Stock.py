# stock.py

class Node:
    def __init__(self, ID, Name, QTY, IMG):
        self.ID = ID
        self.Name = Name
        self.QTY = QTY
        self.IMG = IMG
        self.left = None
        self.right = None        

class Stock:

    def __init__(self):
        self.root = None

    def _insert(self, ptr, ID, Name, QTY, IMG):
        if ptr is None:
            return Node(ID, Name, QTY, IMG), True
        if ID < ptr.ID:
            ptr.left, inserted = self._insert(ptr.left, ID, Name, QTY, IMG)
            return ptr, inserted
        elif ID > ptr.ID:
            ptr.right, inserted = self._insert(ptr.right, ID, Name, QTY, IMG)
            return ptr, inserted
        else:
            # ID already exists
            return ptr, False

    def insert(self, ID, Name, QTY, IMG):
        self.root, inserted = self._insert(self.root, ID, Name, QTY, IMG)
        return inserted

    def __search(self, ptr, ID):
        if ptr is None:
            return None  # Return None if the node is not found
        if ID < ptr.ID:
            return self.__search(ptr.left, ID)
        elif ID > ptr.ID:
            return self.__search(ptr.right, ID)
        return ptr  # Node found

    def search(self, ID):
        return self.__search(self.root, ID)

    def _inOrder(self, ptr, result):
        if ptr is None:
            return
        self._inOrder(ptr.left, result)
        result.append({'ID': ptr.ID, 'Name': ptr.Name, 'QTY': ptr.QTY, 'IMG': ptr.IMG})
        self._inOrder(ptr.right, result)

    def inOrder(self):
        result = []
        self._inOrder(self.root, result)
        return result

    def updateQTY(self, ID, QTY):
        updateNode = self.search(ID)
        if updateNode is not None:
            updateNode.QTY = QTY
            return True
        else:
            return False

    def updateIMG(self, ID, IMG):
        updateNode = self.search(ID)
        if updateNode is not None:
            updateNode.IMG = IMG
            return True
        else:
            return False

    def _delete(self, ptr, ID):
        if ptr is None:
            return ptr, False
        if ID < ptr.ID:
            ptr.left, deleted = self._delete(ptr.left, ID)
            return ptr, deleted
        elif ID > ptr.ID:
            ptr.right, deleted = self._delete(ptr.right, ID)
            return ptr, deleted
        else:
            # Node with only one child or no child
            if ptr.left is None and ptr.right is None:
                del(ptr)
                return None, True
            elif ptr.left is None:
                tmp = ptr.right
                del(ptr)
                return tmp, True
            elif ptr.right is None:
                tmp = ptr.left
                del(ptr)
                return tmp, True
            else:
                # Node with two children: Get the inorder predecessor (max in the left subtree)
                maxNode = self.findMax(ptr.left)
                ptr.ID = maxNode.ID
                ptr.Name = maxNode.Name
                ptr.QTY = maxNode.QTY
                ptr.IMG = maxNode.IMG
                ptr.left, deleted = self._delete(ptr.left, maxNode.ID)
                return ptr, deleted

    def findMax(self, ptr):
        while ptr.right is not None:
            ptr = ptr.right
        return ptr

    def delete(self, ID):
        self.root, deleted = self._delete(self.root, ID)
        return deleted

if __name__ == "__main__":
    stk = Stock()
    
    # เพิ่มข้อมูลเริ่มต้น
    initial_data = [
        {'ID': 5, 'Name': "Item A", 'QTY': 5, 'IMG': "Image1.png"},
        {'ID': 4, 'Name': "Item B", 'QTY': 4, 'IMG': "Image2.png"},
        {'ID': 2, 'Name': "Item C", 'QTY': 3, 'IMG': "Image3.png"},
        {'ID': 3, 'Name': "Item D", 'QTY': 6, 'IMG': "Image4.png"},
    ]
    
    print("Adding initial items:")
    for item in initial_data:
        inserted = stk.insert(item['ID'], item['Name'], item['QTY'], item['IMG'])
        if inserted:
            print(f"Inserted: {item}")
        else:
            print(f"Failed to insert (ID already exists): {item}")
    
    print("\nInitial in-order traversal:")
    for item in stk.inOrder():
        print(f"{item['ID']} : {item['Name']} : {item['QTY']} : {item['IMG']}")
    
    print("==============================")
    
    # อัปเดต QTY ของ ID 3
    print("Updating QTY of ID 3 to 999.")
    updated = stk.updateQTY(3, 999)
    if updated:
        print("Update successful.")
    else:
        print("Update failed. ID 3 not found.")
    
    print("\nIn-order traversal after updating QTY of ID 3:")
    for item in stk.inOrder():
        print(f"{item['ID']} : {item['Name']} : {item['QTY']} : {item['IMG']}")
    
    print("==============================")
    
    # ลบ ID 3 และ 2
    print("Deleting ID 3.")
    deleted = stk.delete(3)
    if deleted:
        print("Deletion of ID 3 successful.")
    else:
        print("Deletion failed. ID 3 not found.")
    
    print("Deleting ID 2.")
    deleted = stk.delete(2)
    if deleted:
        print("Deletion of ID 2 successful.")
    else:
        print("Deletion failed. ID 2 not found.")
    
    print("\nIn-order traversal after deleting IDs 3 and 2:")
    for item in stk.inOrder():
        print(f"{item['ID']} : {item['Name']} : {item['QTY']} : {item['IMG']}")
    
    print("==============================")
    
    # อัปเดต IMG ของ ID 4
    print("Updating IMG of ID 4 to 'Image000.png'.")
    updated = stk.updateIMG(4, "Image000.png")
    if updated:
        print("Update successful.")
    else:
        print("Update failed. ID 4 not found.")
    
    print("\nFinal in-order traversal:")
    for item in stk.inOrder():
        print(f"{item['ID']} : {item['Name']} : {item['QTY']} : {item['IMG']}")

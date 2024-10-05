class Node:
    def __init__(self,queueNum,table,ID,QTY):
        self.queueNum = queueNum
        self.table = table
        self.ID = ID
        self.QTY = QTY
        self.next = None

class QueueList:
    def __init__(self):
        self.first = None

    def enqueue(self,table,ID,QTY):
        if self.first is None:
            newNode = Node(1,table,ID,QTY)
            self.first = newNode
        else:
            i = 2
            last = self.first
            while last.next is not None:
                last = last.next
                i = i+1
            newNode = Node(i,table,ID,QTY)
            last.next = newNode

    def dequeue(self):
        queueNum = self.first.queueNum
        tmp = self.first
        self.first = self.first.next
        del(tmp)
        return queueNum

    def display(self):
        result = []
        current = self.first
        if current is None:
            return "No queue"
        while current:
            result.append({
                'queueNum': current.queueNum,
                'table': current.table,
                'ID': current.ID,
                'qty' : current.QTY
            })
            current = current.next

        return result



    

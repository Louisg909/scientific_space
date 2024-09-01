




class HeapNode:
    def __init__(self, value, item):
        self.value = value
        self.item = item
        self.large = None
        self.small = None

    def add_node(self, node):
        if node > self:
            node.large = self
            node.small = 

    def __gt__(self, other):
        return self.value > other.value



class MaxHeap:
    def __init__(self, root):
        self.root = root

    def add_node(self, node):
        if self.root > 
        






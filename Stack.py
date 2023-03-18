from queue import LifoQueue

class Stack(object):
   
    def __init__(self):
        self.stack = LifoQueue()
       
        
    def push(self, item):
        self.stack.put(item)
        
    
    def pop(self):
        return self.stack.get()
    
    
    def top(self):
        top = self.pop()
        self.stack.put(top)
        
        return top
    
    
    def snoc(self):
        if self.get_size() == 1:
            return (self.pop(), None)
        
        return (self.pop(), self.top())
    
    
    def get_size(self):
        return self.stack.qsize()
    
    
    def is_empty(self):
        return self.stack.empty()
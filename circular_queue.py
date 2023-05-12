class CircularQueue():
    def __init__(self, size):
        self.size = size
        self.queue = [-1 for i in range(size)] 
        self.front = self.rear = -1
        self._current_index = 0

    def __repr__(self):
        text = "["
        for i in self:
            index = (self.size - i + self.rear)%self.size 
            text += str(self.queue[index])
            if not i == 9:
                text += " "
        text += "]"
        return text
    
    def __iter__(self):
        self._start = False
        self._current_index = self.rear
        return self
    
    def __next__(self):
        if self.rear == self._current_index and self._start:
            raise StopIteration
        if self.front == -1 or self.rear == -1 or self.queue[self._current_index] == -1:
            raise StopIteration
        if not self._current_index == -1 or not self._current_index == self.rear:
            self._start = True
            dis = self.queue[self._current_index]
            self._current_index = self._current_index - 1
            if self._current_index < 0:
                self._current_index = self.size - 1
            return dis
    
    def enqueue(self, data):  
        # condition if queue is full
        if ((self.rear + 1) % self.size == self.front): 
            self.dequeue()
            # next position of rear
            self.rear = (self.rear + 1) % self.size 
            self.queue[self.rear] = data
        # condition for empty queue
        elif (self.front == -1): 
            self.front = 0
            self.rear = 0
            self.queue[self.rear] = data
        else:
            # next position of rear
            self.rear = (self.rear + 1) % self.size 
            self.queue[self.rear] = data

    def dequeue(self):
        if (self.front == -1): # condition for empty queue
            # print ("Queue is Empty\n")
            pass
              
        # condition for only one element
        elif (self.front == self.rear): 
            temp = self.queue[self.front]
            self.queue[self.front] = -1
            self.front = -1
            self.rear = -1
            return temp
        else:
            temp = self.queue[self.front]
            self.queue[self.front] = -1
            self.front = (self.front + 1) % self.size
            return temp
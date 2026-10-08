class MinStack:

    def __init__(self):
        self.stack = []
        self.min_s = []

    def push(self, val):
        self.stack.append(val)

        if not self.min_s:
            self.min_s.append(val)
        else:
            if val < self.min_s[-1]:
                self.min_s.append(val)
            else:
                self.min_s.append(self.min_s[-1])

    def pop(self):
        self.stack.pop()
        self.min_s.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_s[-1]
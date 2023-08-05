class Number:
  def __init__(self, value):
      self.num=float(value)
  def add(self, otherval):
      self.num+=otherval
  def subtract(self, otherval):
      self.num-=otherval
  def mul(self, otherval):
      self.num*=otherval

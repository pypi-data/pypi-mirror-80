import math
import numpy, scipy
import matplotlib.pyplot as plt


def TR(n):
	'''function to gve you triangular number n'''
	tr=n*(n-1)
	return tr
def tn(n, t1, d):
	tn=t1+d*(n-1)
	return tn

#define some constants
pi=3.14159265358979323846264338327950
e=2.7182818284590452353602874713527

def sqrtofn(n):
	sqrty=math.sqrt(n)
	return sqrty

def square(n):
	'''return the square of n'''
	n=n**2
	return n

def pow(x, y):
	n=x**y
	return n

	'''return c from a and b, for pythagorean theorem'''
	c2=pow(a, 2)+pow(b, 2)
	c=sqrtofn(c2)
	return c
def dectofrac(dec):
    frac=str(dec)+'/1'
    return frac
def factorial(x):
	numlist=[]
	for y in range(x):
		numlist.append(y)
	z=1
	for y in numlist:
		z*=y
	return z

def Fibonacci(n):
    if n<=0:
        print("Incorrect input")
    # First Fibonacci number is 0
    elif n==1:
        return 0
    # Second Fibonacci number is 1
    elif n==2:
        return 1
    else:
        return Fibonacci(n-1)+Fibonacci(n-2)

class RightTriangle:
    def __init__(self, angleone, hypotenuse, leg1, leg2):
        '''leg1=opposite, leg2=adjacent, hypotenuse=hypotenuse'''
        self.angle1=angleone
        self.s1=hypotenuse
        self.s2=leg1
        self.s3=leg2
        self.angle3=90
    def draw(self):
        import turtle
        turtle.rt(90)
        turtle.fd(self.s2)
        turtle.lt(90)
        turtle.fd(self.s3)
        turtle.lt(self.angle1)
        turtle.fd(self.s1)
    def sin(self):
        return self.s2/self.hypotenuse
    def cos(self):
        return self.s3/hypotenuse
    def tan(self):
        return self.s2/self.s3
    def changedimensions(self, newhypotenuse, newleg1, newleg2):
        self.s1=newhypotenuse
        self.s2=newleg1
        self.s3=newleg2
    def changeangles(self, newangle1):
        self.angle1=newangle1

def absval(x):
    if x<0:
        return -x
    elif x>=0:
        return x
    else:
        print("enter a valid number")
        return "enter a valid number"

def graph_equation(formula, x_range):
    x = numpy.array(x_range)
    y = eval(formula)
    plt.plot(x, y)
    plt.show()

def absgraph(x):
    graph_equation(abs(x))

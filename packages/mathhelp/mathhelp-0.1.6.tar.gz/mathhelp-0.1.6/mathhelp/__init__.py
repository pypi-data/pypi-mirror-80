import math
import numpy, scipy
import matplotlib.pyplot as plt

def TR(n):
	'''function to gve you triangular number n'''
	tr=n*(n-1)
	return tr
def tn(n, t1, d):
	'''gives you term n in an arithmatic sequence'''
	tn=t1+d*(n-1)
	return tn

#define some constants
pi=3.14159265358979323846264338327950
e=2.7182818284590452353602874713527

def sqrtofn(n):
	'''give square root of n'''
	sqrty=math.sqrt(n)
	return sqrty

def square(n):
	'''return the square of n'''
	n=n**2
	return n

def pow(x, y):
	'''return x raised to the power y'''
	n=x**y
	return n

def pythagorean(a, b):
	'''return c from a and b, for pythagorean theorem'''
	c2=pow(a, 2)+pow(b, 2)
	c=sqrtofn(c2)
	return c


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

def sin(angle):
	return math.sin(angle)
def cosine(angle):
	return math.cos(angle)
def tan(angle):
	return math.tan(angle)

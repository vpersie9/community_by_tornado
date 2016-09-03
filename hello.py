#-*-coding:utf-8-*-
__author__="vpersie9"

import functools

def funciton(x,y):
	return x**y


func=functools.partial(function,2,3)

print func()

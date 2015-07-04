import numpy as np
import csv
from ED import *
from ED_2D import *

def mag(n):
	l = [bin(x)[2:].rjust(n, '0') for x in range(2**n)]
	b = np.array([np.array(map(int, i)) for i in l])
	lst = [round(x* 0.1,2) for x in range(0,21)]
	b_list = []
	for i in b:
		b_list.append(list(i))
	magnetization = []
	for i in b_list:
		magnetization.append(abs(i.count(1) - i.count(0)))

	c = []
	for j in lst: 
		#print j, '+++++++++++++'
		e = ED(n,j)[1]
		a = 0
		#print ED(n,j)[1], '***********************'
		for i in range(len(magnetization)):
			a += e[i][0]*e[i][0]*magnetization[i]
		#	print i, magnetization[i], e[i][0],e[i][0]*e[i][0], e[i][0]*e[i][0]*magnetization[i], '####'
		c.append([a,j])
	return c

def mag_2D(n,m):
	l = [bin(x)[2:].rjust(n, '0') for x in range(2**(n*m))]
	b = np.array([np.array(map(int, i)) for i in l])
	lst = [round(x* 0.1,2) for x in range(0,21)]
	b_list = []
	for i in b:
		b_list.append(list(i))
	magnetization = []
	for i in b_list:
		magnetization.append(abs(i.count(1) - i.count(0)))

	c = []
	for j in lst: 
		#print j, '+++++++++++++'
		e = ED_2D(n,m,j)[1]
		a = 0
		#print ED(n,j)[1], '***********************'
		for i in range(len(magnetization)):
			a += e[i][0]*e[i][0]*magnetization[i]
		#	print i, magnetization[i], e[i][0],e[i][0]*e[i][0], e[i][0]*e[i][0]*magnetization[i], '####'
		c.append([a,j])
	return c
def oneD(n):
	a = mag(n)
	b = mag(n-1)
	c = []
	for i in range(len(a)):
		c.append([(a[i][0]-b[i][0])*n,a[i][0],a[i][1]])
	return c

def twoD(n,m):
	a = mag_2D(n,m)
	b = mag_2D(n,m-1)
	c = mag_2D(n-1,m)
	d = mag_2D(n-1,m-1)
	e = []
	#for i in range(len(a)):
	#	print a[i][0],'-', b[i][0],'-', c[i][0],'+', d[i][0],'=', a[i][0] -b[i][0] -c[i][0] +d[i][0],'h =', a[i][1]
	for i in range(len(a)):
		e.append([(a[i][0]-b[i][0]-c[i][0]+d[i][0])*(n*m),a[i][1]])
	return e

if __name__ == "__main__":
	mag(2)
	oneD(2)
	twoD(2,2)
	mag_2d(2,2)
'''
for i in mag(3):
	print i
for i in twoD(2,2):
	print i
'''
print mag_2D(2,2)
#print twoD(3,3)
#with open("mag_nlce_ed_12.csv", "wb") as f:
 #   writer = csv.writer(f)
  #  writer.writerows()

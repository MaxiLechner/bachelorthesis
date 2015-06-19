import numpy as np
import csv
from ED import *

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

def asd(n):
	a = mag(n)
	b = mag(n-1)
	c = []
	for i in range(len(a)):
		c.append([(a[i][0]-b[i][0])*n,a[i][0],a[i][1]])
	return c
if __name__ == "__main__":
	mag(2)
	asd(2)
#c = []
#print (mag(5)-mag(4))*5
#for i in asd(6):
#	print i

#with open("mag_nlce_ed.csv", "wb") as f:
 #   writer = csv.writer(f)
  #  writer.writerows(asd(10))

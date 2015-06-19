import numpy as np
import csv
from ED import *
n = 14
l = [bin(x)[2:].rjust(n, '0') for x in range(2**n)]
b = np.array([np.array(map(int, i)) for i in l])
lst = [round(x* 0.1,2) for x in range(0,20)]
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

with open("mag.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(c)
#print ED(3,0)[1]
#print ED(3,20)[1]

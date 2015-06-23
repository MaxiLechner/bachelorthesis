import numpy as np
from ED import *

def densitymatrix(n,m,h):
	#n,m number of sites in seperated regions
	a = ED(n,h)[1]
	b = ED(m,h)[1]
	Mc = np.outer(a,b)
	if n<=m:
		return np.dot(Mc,Mc.conj().T)
	else:
		return np.dot(Mc.conj().T,Mc)

print densitymatrix(2,2,1)

def renyientropy(alpha,n,m,h):
	eigenvalues = np.linalg.eigvalsh(densitymatrix(n,m,h))
	if alpha==1:
		von_Neumann = 0
		for i in eigenvalues:
			von_Neumann += i * np.log(i)
		return von_Neumann
	else:
		trace = 0
		for i in eigenvalues:
			trace += i
		print eigenvalues
		print trace, np.log(trace),'####'
		return (1/(1-alpha) * np.log(trace))
print renyientropy(1.5,2,2,1)

def sum_line_x(alpha,n,m,h):
	a = []
	for i in range((n-1)):
		a.append(i+1)
	b = list(reversed(a))
	s = 0
	for i in range(len(a)):
		s += renyientropy(alpha,a[i]*m,b[i]*m,h)
	return s

def sum_line_y(alpha,n,m,h):
	a = []
	for i in range((m-1)):
		a.append(i+1)
	b = list(reversed(a))
	s = 0
	for i in range(len(a)):
		s += renyientropy(alpha,n*a[i],n*b[i],h)
	return s

def cornerentropy(alpha,n,m,h):
	a = []
	b = []
	for i in range((m-1)):
		a.append(i+1)
	for i in range((n-1)):
		b.append(i+1)
	
	c = []
	for i in b:
		for j in a:
			c.append([i*j,n*m-i*j])
			print i*j,i,j
	d = []
	for i in reversed(c):
		d.append(list(reversed(i)))

	s = 0
	for i in range(len(c)):
		s += (renyientropy(alpha,c[i][0],c[i][1],h) + renyientropy(alpha,d[i][0],d[i][1],h))
	return 1/2 * (s-(m-1)*sum_line_x(alpha,n,m,h) - (n-1)*sum_line_y(alpha,n,m,h))



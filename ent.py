import numpy as np
from ED import *

def densitymatrix(x_a,y_a,x_b,y_b,h):
	#x_a: size of system a in x direction
	#y_a: size of system a in y direction
	#...
	phi = ED((x_a*y_a)+(x_b*y_b),h)[1]
	Mc = np.resize(phi,(2**(x_a*y_a),2**(x_b*y_b)))
	'''
	s = (2**m,2**(N-m))
	p = np.zeros(s)
	
	for i in range(len(phi)):
		for j in range(2**m):
			for k in range(2**(N-m)):
				p[j,k] = phi[i]
				print phi[i], j, k, '####', p[j,k]
	'''
	if (x_a*y_a)>=(x_b*y_b):
		return np.dot(Mc.conj().T,Mc)
	else:
		return np.dot(Mc,Mc.conj().T)

	#return np.dot(np.resize(phi,(2**m,2**(N-m))).T,np.resize(phi,(2**m,2**(N-m)))), np.dot(np.resize(phi,(2**m,2**(N-m))),np.resize(phi,(2**m,2**(N-m))).T)
#print densitymatrix(3,2,3,1,3.0)
#print densitymatrix(1,1,1,1,2)

def densitymatrix_sitebased(n,m,h):
	#x_a: size of system a in x direction
	#y_a: size of system a in y direction
	#...
	phi = ED(n+m,h)[1]
	Mc = np.resize(phi,(2**n,2**m))
	if n >= m:
		return np.dot(Mc.conj().T,Mc)
	else:
		return np.dot(Mc,Mc.conj().T)
#print densitymatrix_sitebased(1,1,2)

def renyientropy(alpha,x_a,y_a,x_b,y_b,h):
	eigenvalues = np.linalg.eigvalsh(densitymatrix(x_a,y_a,x_b,y_b,h))
	#print eigenvalues
	if alpha==1:
		von_Neumann = 0
		for i in eigenvalues:
			von_Neumann += i * np.log(i)
		return von_Neumann
	else:
		trace = 0
		for i in eigenvalues:
			trace += i
		#print trace, np.log(trace),'####'
		return (1/(1-alpha) * np.log2(trace))

#print renyientropy(1,1,1,1,1,2)

def renyientropy_sitebased(alpha,n,m,h):
	eigenvalues = np.linalg.eigvalsh(densitymatrix_sitebased(n,m,h))
	#print eigenvalues
	if alpha==1:
		von_Neumann = 0
		for i in eigenvalues:
			von_Neumann += i * np.log(i)
		return von_Neumann
	else:
		trace = 0
		for i in eigenvalues:
			trace += i
		#print trace, np.log(trace),'####'
		return (1/(1-alpha) * np.log(trace))
#print renyientropy(1.5,3,2,3,1,2.0)
#print renyientropy_sitebased(1.1,1,1,2)
def sum_line_x(alpha,n,m,h):
	a = []
	for i in range((n-1)):
		a.append(i+1)
	b = list(reversed(a))
	s = 0
	for i in range(len(a)):
		s += renyientropy(alpha,a[i],m,b[i],m,h)
	return (m-1)*s
#print sum_line_x(1,3,3,1.0)

def sum_line_y(alpha,n,m,h):
	a = []
	for i in range((m-1)):
		a.append(i+1)
	b = list(reversed(a))
	s = 0
	for i in range(len(a)):
		s += renyientropy(alpha,n,a[i],n,b[i],h)
	return (n-1)*s
#print sum_line_y(1,3,3,1.0)
def cornerentropy(alpha,n,m,h):
	a = []
	b = []
	for i in range((m-1)):
		a.append(i+1)
	for i in range((n-1)):
		b.append(i+1)
    #print a
	#print b
	c = []
	for i in b:
		for j in a:
			c.append([i*j,n*m-i*j])
	#		print i*j,n*m-i*j
	#print c
	d = []
	for i in reversed(c):
		d.append(list(reversed(i)))
	#print d
	s1 = 0
	s2 = 0
	for i in range(len(c)):
		s1 += renyientropy_sitebased(alpha,c[i][0],c[i][1],h)
		s2 += renyientropy_sitebased(alpha,d[i][0],d[i][1],h)
	return (s1 + s2)

n=3
m=3
h=2
a=1
#print cornerentropy(a,n,m,h) 
print sum_line_x(a,n,m,h) 
print sum_line_y(a,n,m,h)

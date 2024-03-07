"""
given Testcases from: https://bwinf.de/bundeswettbewerb/41/2/
"""

with open("kaese1.txt") as k1:
	tc1 = k1.read().splitlines()
with open("kaese2.txt") as k2:
	tc2 = k2.read().splitlines()
with open("kaese3.txt") as k3:
	tc3 = k3.read().splitlines()
with open("kaese4.txt") as k4:
	tc4 = k4.read().splitlines()
with open("kaese5.txt") as k5:
	tc5 = k5.read().splitlines()
with open("kaese6.txt") as k6:
	tc6 = k6.read().splitlines()
with open("kaese7.txt") as k7:
	tc7 = k7.read().splitlines()

def generateCheeseSliceList(arr):
	l = []
	for n in arr[1:]:
		cs = []
		p = ''
		for a in n:
			if a != ' ':
				p += a
			else:
				cs.append(int(p))
				p = ''
		cs.append(int(p))
		l.append(cs)
	return l

def generateCheeseSliceDict(arr):
	d = {}
	for n in arr[1:]:
		cs = []
		p = ''
		for a in n:
			if a != ' ':
				p += a
			else:
				cs.append(int(p))
				p = ''
		cs.append(int(p))
		if cs[0] > cs[1]:
			(cs[0], cs[1]) = (cs[1], cs[0])
		prod = cs[0]*cs[1]
		if d.get(prod) == None:
			d[prod] = [cs[1]]
		else:
			d[prod].append(cs[0])
	return d

def convertListToDict(arr):
	d = {}
	for n in arr:
		if n[0] > n[1]:
			(n[0], n[1]) = (n[1], n[0])
		prod = n[0]*n[1]
		if d.get(prod) == None:
			d[prod] = [n[1]]
		else:
			d[prod].append(n[1])
	return d


import random
def sliceCheeseCuboid(cuboid):
	slices = []
	while not (cuboid[0] == 1 or cuboid[1] == 1 or cuboid[2] == 1):
		random_rotation = random.randint(0,2)
		if random_rotation == 0:
			slices.append([cuboid[1], cuboid[2]])
			cuboid[0] -= 1
		elif random_rotation == 1:
			slices.append([cuboid[0], cuboid[2]])
			cuboid[1] -= 1
		else:
			slices.append([cuboid[0], cuboid[1]])
			cuboid[2] -= 1
	if cuboid[0] == 1:
		slices.append([cuboid[1], cuboid[2]])
	elif cuboid[1] == 1:
		slices.append([cuboid[0], cuboid[2]])
	else:
		slices.append([cuboid[0], cuboid[1]])
	return slices

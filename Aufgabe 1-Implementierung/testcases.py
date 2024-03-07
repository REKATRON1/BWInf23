"""
given Testcases from: https://bwinf.de/bundeswettbewerb/41/2/
"""

import matplotlib.pyplot as plt

with open("wenigerkrumm1.txt") as w:
	str_map1 = w.read().splitlines()
with open("wenigerkrumm2.txt") as w:
	str_map2 = w.read().splitlines()
with open("wenigerkrumm3.txt") as w:
	str_map3 = w.read().splitlines()
with open("wenigerkrumm4.txt") as w:
	str_map4 = w.read().splitlines()
with open("wenigerkrumm5.txt") as w:
	str_map5 = w.read().splitlines()
with open("wenigerkrumm6.txt") as w:
	str_map6 = w.read().splitlines()
with open("wenigerkrumm7.txt") as w:
	str_map7 = w.read().splitlines()

def convert_txtMap(arr):
	points = []
	for line in arr:
		new_point = []
		x = ''
		for letter in line:
			if letter != ' ':
				x += letter
			else:
				new_point.append(float(x))
				x = ''
		new_point.append(float(x))
		points.append(new_point)
	"""
	plt.scatter([p[0] for p in points], [p[1] for p in points])
	plt.plot([p[0] for p in points], [p[1] for p in points])
	plt.show()
	"""
	return points

import random
import nnfs

nnfs.init()

def generate_randomMap(num_points):
	points = []
	for n in range(num_points):
		points.append([random.random()*1000-500, random.random()*1000-500])
	return points

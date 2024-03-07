import testcases as tc
import numpy as np
import time

def isolate_edges(slices, filt={}):
	edges = {}
	for face_area, face_edges in slices.items():
		for e in list(map(lambda x,y:x*y, slices.get(face_area), filt.get(face_area))):
			if e > 0:
				if edges.get(e) == None:
					edges[e] = [int(face_area/e)]
				else:
					edges[e].append(int(face_area/e))
	return edges

def edges_to_list(edges):
	face_list = []
	for edge1, edges2 in edges.items():
		for edge2 in edges2:
			face_list.append([edge1, edge2])
	return face_list

def remove_usedANDduplicates(face_list, used):
	new_face_list = []
	for face in face_list:
		append = True
		remove = ()
		for u in used:
			if face[0] == u[0] and face[1] == u[1]:
				append = False
				remove = u
				break
		if append:
			a = True
			for f in new_face_list:
				if face[0] == f[0] and face[1] == f[1]:
					a = False
			if a:
				new_face_list.append(face)
		else:
			used.remove(remove)
	return new_face_list

def separate(face_list):
	new_list = []
	for face in face_list:
		new_list.append(face[0])
		new_list.append(face[1])
	return new_list

def one_equals(arrA, arrB):
	if len(arrA) != len(arrB):
		return False
	for n in range(len(arrA)):
		if arrA[n] == arrB[n]:
			return True
	return False

def generate_primefactors(a):
	p = 2
	prime_factors = []
	while p*p <= a:
		if a % p:
			p += 1
		else:
			a //= p
			prime_factors.append(p)
	if a > 1:
		prime_factors.append(a)
	return prime_factors

def prod_combinations(arr):
	combinations = prod_combinations_intern(arr, 0)
	return list(dict.fromkeys(combinations))

def prod_combinations_intern(arr, i):
	if i < len(arr):
		comb = []
		rec_comb = prod_combinations_intern(arr, i+1)
		comb.extend(rec_comb)
		for n in rec_comb:
			comb.append(n*arr[i])
		return comb
	return [1]

def not_match_index(arrA, arrB):
	arrC = arrB.copy()
	for i in range(len(arrA)):
		if len(arrC) == 0:
			return i
		if arrA[i] in arrC:
			arrC.remove(arrA[i])
		else:
			return i
	return 0

def copy_dict(d0):
	new_dict = {}
	for key in d0:
		new_dict[key] = d0[key].copy()
	return new_dict

def biggest_face(face_list):
	biggest = 0
	for face in face_list:
		if prod(face) > biggest:
			biggest = prod(face)
	return biggest

def sum(arr):
	s = 0
	for n in arr:
		s += n
	return s

def prod(arr):
	p = 1
	for n in arr:
		p *= n
	return p

def does_contain(slices, filt, face):
	if face[0] < face[1]:
		(face[0], face[1]) = (face[1], face[0])
	if slices.get(prod(face)) != None and face[0] in list(map(lambda x,y:x*y, slices.get(prod(face)), filt[prod(face)])):
		return True
	return False
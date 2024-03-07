import numpy as np

def calculate_distance(point_A, point_B):
	return np.sqrt((point_A[0]-point_B[0])**2+(point_A[1]-point_B[1])**2)

def calculate_angle(point_A, point_over, point_C):
	if point_A != point_over and point_A != point_C and point_over != point_C:
		ba = np.array(point_A) - np.array(point_over)
		bc = np.array(point_C) - np.array(point_over)
		cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
		if cos_angle < -1:
			cos_angle = -0.9999
		elif cos_angle > 1:
			cos_angle = 0.9999
		angle = np.arccos(cos_angle)
		if np.isnan(angle) or np.isnan(np.degrees(angle)):
			print(point_A,point_over,point_C)
			print('cos', cos_angle)
			print('ang', angle)
			print('deg', np.degrees(angle))
		if angle == 0:
			angle = 0.0001
		return np.degrees(angle)
	return 0

def get_max_distance(matrix):
	n = 0
	for a in matrix:
		for b in a:
			if b > n:
				n = b
	return n

def count_acute_angles(path, angles=None):
	num_acute_angle = 0
	if angles != None:
		for n in range(2, len(path)):
			if angles[path[n-2]][path[n-1]][path[n]] < 90:
				num_acute_angle += 1
		return num_acute_angle
	for n in range(2, len(path)):
		if calculate_angle(path[n-2], path[n-1], path[n]) < 90:
			num_acute_angle += 1
	return num_acute_angle

def count_distances(path, distances=None):
	total_distance = 0
	if distances != None:
		for n in range(1, len(path)):
			total_distance += distances[path[n-1]][path[n]]
		return total_distance
	for n in range(1, len(path)):
		total_distance += calculate_distance(path[n-1], path[n])
	return total_distance

def sum(l):
	s = 0.0
	for i in l:
		s += i
	return s

def get_max_weight(weights):
	m = 0
	for row in weights:
		for n in row:
			if n > m:
				m = n
	return m

def lighter(color, percent):
    '''assumes color is rgb between (0, 0, 0) and (255, 255, 255)'''
    color = np.array(color)
    white = np.array([1.0, 1.0, 1.0])
    vector = white-color
    return color + vector * percent

def lerp(a, b, percent):
	return a-percent*(a-b)
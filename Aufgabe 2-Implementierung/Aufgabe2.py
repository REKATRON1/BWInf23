import testcases as tc
import numpy as np
import sidefunc as sf

def recreate_cheese_cuboid(slices):
	"""
	recreate_cheese_cuboid baut aus einer Liste an Scheiben (slices), welche durch das gerade Zerschneiden 
	eines Käsequaders in gleichmäßige 1 LE-Dicke Scheiben entstehen, 
	den Käsequader wieder zusammen und gibt die Sequenz des Zusammenfügens, falls eine existiert, aus.
	"""
	#Schritt 1: Bestimmung der potentiellen Größen des Käsequaders
	#Schritt 1.1: Berechnung des Volumens des Käsequaders aus der Summe der Volumina der Scheiben
	total_volume = 0
	for key in slices:
		total_volume += key*len(slices[key])

	#Schritt 1.2: Bestimmung der Teiler des Volumens
	primes_of_volume = sf.generate_primefactors(total_volume)
	combinations_volume = sf.prod_combinations(primes_of_volume)

	#Schritt 1.3: Überprüfung der Teiler auf Übereinstimmung mit Maßen der Scheiben
	possible_cubes = []
	for combination in combinations_volume:
		if slices.get(combination) != None:
			new_available_faces = []
			for edge in slices.get(combination):
				if edge in combinations_volume:
					new_available_faces.append(edge)
			new_available_faces = list(dict.fromkeys(new_available_faces))
			for n in new_available_faces:
				possible_cubes.append(([n, int(combination/n)], (n, int(combination/n), int(np.ceil(total_volume/combination)))))

	#Phase 2: Testen der Zusammensetzbarkeit für jede ermittelten Größe
	for first_face, cube_size in possible_cubes:
		#Phase 2.1: Initiierung des Filters und der Lösungssequenz
		slices_filter = {}
		slices_filter[sf.prod(first_face)] = [1 for x in range(len(slices[sf.prod(first_face)]))]
		slices_filter[sf.prod(first_face)][slices[sf.prod(first_face)].index(first_face[0])] = 0
		solution = [first_face]
		current_size = [cube_size[0], cube_size[1], cube_size[2]-1]
		added_face = True
		#Phase 2.2: Wiederholendes Einfügen von Scheiben in das 'Größengitter', bis keine Scheibe mehr eingefügt werden kann
		while True:
			#Phase 2.2.1: Durchsuche die Scheiben auf eine Passende (Beachtung des Filters)
			potential_faces = []
			for face_size in [(current_size[0], current_size[1]),(current_size[0], current_size[2]),(current_size[1],current_size[2])]:
				if slices.get(sf.prod(face_size)) != None:
					if slices_filter.get(sf.prod(face_size)) == None:
						slices_filter[sf.prod(face_size)] = [1 for x in range(len(slices.get(sf.prod(face_size))))]
					if sf.sum(map(lambda x,y:x*y, slices.get(sf.prod(face_size)), slices_filter.get(sf.prod(face_size)))) > 0: #Punkweise Multiplikation der Scheiben mit dem Filter
						for n in face_size:
							if n in map(lambda x,y:x*y, slices.get(sf.prod(face_size)), slices_filter.get(sf.prod(face_size))) and n in current_size:
								potential_faces.append((n, int(sf.prod(face_size)/n)))
			#Phase 2.2.2: Falls es mehrere Mögliche Scheiben zum einfügen gibt, wähle die Größte
			face = []
			if len(potential_faces) == 0:
				#Phase 2.2.2.1: Falls keine Scheibe eingefügt werden kann, breche den Wiederaufbau ab
				break
			elif len(potential_faces) > 1:
				for pface in potential_faces:
					if sf.prod(face) < sf.prod(pface):
						face = list(pface)
			else:
				face = list(potential_faces[0])
			#Phase 2.2.3: Füge die Scheibe ein
			solution.append(face)
			slices_filter.get(sf.prod(face))[list(map(lambda x,y:x*y,slices.get(sf.prod(face)),slices_filter.get(sf.prod(face)))).index(face[0])] = 0
			current_size[sf.not_match_index(current_size, face)] -= 1
		#Phase 2.3: Überprüfung, ob das Käse-Größengitter ausgefüllt ist und, falls ja, mögliche Lösung inversiert zurückgeben
		if sf.one_equals(current_size, [0,0,0]):
			return solution[::-1]

#kaese1 = tc.generateCheeseSliceDict(tc.tc1)
#kaese2 = tc.generateCheeseSliceDict(tc.tc2)
#kaese3 = tc.generateCheeseSliceDict(tc.tc3)
#kaese4 = tc.generateCheeseSliceDict(tc.tc4)
kaese5 = tc.generateCheeseSliceDict(tc.tc5)
#kaese6 = tc.generateCheeseSliceDict(tc.tc6)
#kaese7 = tc.generateCheeseSliceDict(tc.tc7)
sol = recreate_cheese_cuboid(kaese5)
print(sol)

#Zusätzliche Testungen durch das erstellen zufälliger Käsewürfel:

def recreate_x1000(cuboid):
	for i in range(1000):
		s = tc.sliceCheeseCuboid(cuboid.copy())
		sol = recreate_cheese_cuboid(tc.convertListToDict(s))
		if sol == None:
			print('Error',s)
			print(sol, cuboid)
			return False
		return True

import random
def create_random_cuboid():
	return [random.randint(1,15000),random.randint(1,15000),random.randint(1,15000)]

#recreate_x1000(create_random_cuboid())
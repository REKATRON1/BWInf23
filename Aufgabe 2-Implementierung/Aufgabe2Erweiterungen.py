import testcases as tc
import numpy as np
import sidefunc as sf

#Aufgabe 2: Erweiterung
def cubeit(slices, filt={}, p_adds=5, remaining_cubes=2):
	possible_solutions = []
	#1. Initiierung des Filters
	for key, value in slices.items():
		if filt.get(key) == None:
			filt[key] = [1 for x in range(len(value))]
	#2. Generieren der möglichen Größen des 'größten' Käsequaders
	sizes = generate_sizes(slices, filt)

	#3. Durchprobieren aller Größen
	for first_faces, cube_size in sizes:
		slices_filter = sf.copy_dict(filt)
		for sl in first_faces:
			slices_filter[sf.prod(sl)][list(map(lambda x,y:x*y, slices.get(sf.prod(sl)), slices_filter[sf.prod(sl)])).index(sl[0])] = 0
		sol = recreate_cheese_cuboid([[first_faces[-1]], cube_size], slices, slices_filter, p_adds, remaining_cubes)
		if sol != None:
			s = [first_faces[:-1]]
			s[0].extend(sol[0][0])
			if len(sol[0]) > 1:
				s.extend(sol[0][1:])
			possible_solutions.append([s, sol[1], sol[2]])
	#4. Filtern der Lösungen und Invertieren der Lösungssequenz
	if len(possible_solutions) == 0:
		return None
	best_sol = possible_solutions[0]
	if len(possible_solutions) > 1:
		for sol in possible_solutions[1:]:
			#Die beste Lösung ist die, die so wenig Scheiben wie möglich einfügen muss und so viele Scheiben wie möglich nutzt.
			if len(sol[1]) + len(sol[2]) < len(best_sol[1]) + len(best_sol[2]):
				best_sol = sol
	invert_sol = [best_sol[0][0][::-1]]
	if len(best_sol[0]) > 1:
		for s in best_sol[0][1:]:
			invert_sol.append(s)
	return [invert_sol, best_sol[1], best_sol[2]]

def generate_sizes(slices, filt):
	"""
	generate_sizes nimmt ein Wörterbuch mit Käsescheiben, welche aus dem Zerschneiden eines oder meherer Käsequader entstanden sind,
	als Input und gibt mögliche Größen für den größten (ausgehend von der Scheibe mit der längsten Kante) Käsequader zurück,
	sowie die dazugehörigen 'Randscheiben' des Käsequaders.
	"""
	#1. Konvertiere das Scheiben-Wörterbuch (slices) in ein Kanten-Wörterbuch, wobei statt dem Produkt der Kanten die jeweils längere Kante der Schlüssel ist
	#und alle Kanten, die mit dieser längeren Kante in Kombination in einer der Scheiben auftreten, die Werte sind.
	edges = sf.isolate_edges(slices, filt)
	#2. Suche nach der längsten Kante
	largest_face, num_duplicates = [0, 0], 0
	for edge, value in edges.items():
		if edge > largest_face[0]:
			largest_face[0] = edge
			largest_face[1] = 0
			num_duplicates = 0
			for v in value:
				#2.1 Füge nur die längsten 'Kombinationskanten' (Kanten, die mit der längsten Kante vorkommen) als mögliche Startscheibe hinzu.
				if v > largest_face[1]:
					largest_face[1] = v
					num_duplicates = 1
				#2.2 Falls die 'größte' Scheibe mehrfach vorkommt, zähle wie oft.
				elif v == largest_face[1]:
					num_duplicates += 1
	#3. Generiere aus den größten gefundenen Scheiben mögliche Größen für den 'größten' Käsequader
	possible_cubes = []
	#3.1 Nutze nicht notwendigerweise alle größten Scheiben, da jene möglicherweise von unterschiedlichen Quadern kommen
	for d in range(1, num_duplicates+1):
		all_slices_list = sf.edges_to_list(edges) #konvertiert Kanten-Wörterbuch wieder zu einer Liste an Scheiben
		#all_slices_list sieht z.B. so aus: [[4, 2], [4, 2], [4, 2], [4, 3], [6, 4], [6, 4], [6, 4], [6, 6], [6, 6], [6, 3], [3, 3], [3, 3]]
		cut_slices_list = sf.remove_usedANDduplicates(all_slices_list, [largest_face for x in range(d)]) #Entfernt Redundante Scheiben und die benutzten größten Scheiben aus der Scheibenliste
		#cut_slices_list sieht z.B. so aus: [[4, 2], [4, 3], [6, 4], [6, 6], [6, 3], [3, 3]] (es wurde nur 1x [6, 6] genutzt)
		split_edges_list = sf.separate(cut_slices_list) #teilt die Scheiben in einzelne Kanten auf:
		#split_edges_list sieht z.B. so aus: [4, 2, 4, 3, 6, 4, 6, 6, 6, 3, 3, 3]
		possibility = []
		for e in range(len(split_edges_list)):
			if split_edges_list[e] == largest_face[1]:
				#Die Kante mit dem Index e in split_edges_list gehört zur Scheibe mit dem Index ⌊e/2⌋ in cut_slices_list
				possibility.append(int(np.floor(e/2)))
		for p in possibility:
			used_slices = [largest_face for x in range(d)]
			used_slices.append(cut_slices_list[p])
			#3.2 Füge die, sich ergebende, Größe den möglichen Größen hinzu, wobei die Verwendeten Randscheiben abzuziehen sind
			potential_remaining_size = [largest_face[0]-1, largest_face[1], cut_slices_list[p][sf.not_match_index(cut_slices_list[p], largest_face)]]
			possible_cubes.append([used_slices, potential_remaining_size])
	return possible_cubes

def recreate_cheese_cuboid(sizes, slices, filt, remaining_adds=0, remaining_cubes=0):
	"""
	recreate_cheese_cuboid generiert rekursiv die optimale Sequenz zum Zusammenfügen einer Liste an Scheiben zu mehreren Käsequadern.
	sizes: Liste an möglichen Größen für den 'größten' Quader mit zugehörigen 'Randscheiben'
	slices: assoziative List/Wörterbuch mit den Scheiben (key=Produkt der Kanten, value=Liste der Kanten der Scheiben dessen Kanten das Produkt des zugehörigen keys ergeben)
	filt: Filter für die slices (sodass slices nicht kopiert werden muss)
	remaining_adds: Integer der zur Begrenzung der Rekursionstiefe dient, indem er die Menge der Hinzufügbaren Scheiben begrenzt
	remaining_cubes: Integer der zur Begrenzung der Rekursionstiefe dient, indem er die Menge der gesuchten, vermischen Quader begrenzt
	"""
	possible_solutions = []
	#1. Rekursionsanker: Falls das Größengitter gefüllt ist:
	if sf.one_equals(sizes[1], [0,0,0]):
		#1.1 Bestimme ob es übriggebliebene Scheiben gibt.
		remaining = []
		for key, value in slices.items():
			for v in list(map(lambda x,y:x*y, slices.get(key), filt.get(key))):
				if v != 0:
					remaining.append([v, int(key/v)])
		#1.2 Falls ja, versuche aus ihnen ebenfalls einen Quader zusammenzubauen
		if len(remaining) > 0 and remaining_cubes>0:
			s1 = [sizes[0]]
			s2 = cubeit(slices, filt, remaining_adds, remaining_cubes-1)
			#1.2.1 Falls das möglich ist, füge die Lösungen zusammen
			if s2 == None:
				return [s1, [], remaining]
			s1.extend(s2[0])
			return [s1, s2[1], s2[2]]
		return [[sizes[0]], [], remaining]
	#2. Bestimme, in das Größengitter einfügbaren, Scheiben
	solution = sizes[0]
	for dim in range(3):
		p_face = sizes[1].copy()
		p_face.pop(dim)
		p_new_size = sizes[1].copy()
		p_new_size[dim] -= 1
		#2.1 Überprüfe ob es die Scheibe in der Scheibenliste gibt
		if sf.does_contain(slices, filt, p_face):
			#2.1.1 falls ja, führe für sie den Algorithmus mit dem aktualisierten Größengitter rekursiv aus
			new_slices_filter = sf.copy_dict(filt)
			new_slices_filter[sf.prod(p_face)][list(map(lambda x,y:x*y, slices.get(sf.prod(p_face)), filt[sf.prod(p_face)])).index(p_face[0])] = 0
			new_solution = recreate_cheese_cuboid([[p_face], p_new_size], slices, new_slices_filter, remaining_adds, remaining_cubes)
			#2.1.2 Falls es für die eingefügte Scheibe eine Lösung gibt, füge der Lösung die eingefügte Scheibe hinzu und speichere die Lösung als mögliche Gesamtlösung
			if new_solution != None:
				p_solution = solution.copy()
				p_solution.extend(new_solution[0][0])
				total_sol = [p_solution]
				if len(new_solution[0]) > 1:
					total_sol.extend(new_solution[0][1:])
				possible_solutions.append([total_sol, new_solution[1], new_solution[2]])
		#2.2 Falls es die Scheibe nicht gibt und noch nicht bereits einige Scheiben hinzugefügt wurden,
		elif remaining_adds > 0:
			#2.2.1 'tue so' als ob es die Scheibe gäbe und führe den Algorithmus trotzdem rekursiv mit dem aktualisierten Größengitter aus
			new_slices_filter = sf.copy_dict(filt)
			new_solution = recreate_cheese_cuboid([[p_face], p_new_size], slices, new_slices_filter, remaining_adds-1, remaining_cubes)
			#2.2.2 Falls es für die eingefügte Scheibe eine Lösung gibt, füge der Lösung und der Sammlung hinzugefügter Scheiben 
			#die eingefügte Scheibe hinzu und speichere die Lösung als mögliche Gesamtlösung
			if new_solution != None:
				p_solution = solution.copy()
				p_solution.extend(new_solution[0][0])
				p_added = new_solution[1]
				p_added.append(p_face)
				total_sol = [p_solution]
				if len(new_solution[0]) > 1:
					total_sol.extend(new_solution[0][1:])
				possible_solutions.append([total_sol, p_added, new_solution[2]])
	#3. Filtere die Lösungen nach der besten und gebe diese an die nächsthöhere Schicht/den Benutzer zurück:
	if len(possible_solutions) == 0:
		return None
	best_sol = possible_solutions[0]
	if len(possible_solutions) > 1:
		for sol in possible_solutions[1:]:
			#Die beste Lösung ist die, die so wenig Scheiben wie möglich einfügen muss und so viele Scheiben wie möglich nutzt.
			if len(sol[1]) + len(sol[2]) < len(best_sol[1]) + len(best_sol[2]):
				best_sol = sol
	return best_sol

import random
def scramble(l):
	for i in range(100):
		a = random.randint(0, len(l)-1)
		b = random.randint(0, len(l)-1)
		(l[a], l[b]) = (l[b], l[a])


def printit(sol):
	for cube in range(1, len(sol[0])+1):
		print('Würfel', str(cube) + ':', sol[0][cube-1])
	if len(sol[1]) > 0:
		print('\nHinzugefügte Scheiben:', sol[1])
	if len(sol[2]) > 0:
		print('\nÜbriggebliebene Scheiben:', sol[2])

#mische Würfel zusammen
scheibenliste = tc.generateCheeseSliceList(tc.tc1)
scheibenliste.extend(tc.generateCheeseSliceList(tc.tc2))

scramble(scheibenliste)
#entferne Scheiben
removed = [scheibenliste.pop(-1)]
for i in range(3):
	removed.append(scheibenliste.pop(-1))

print('Eingabe:', scheibenliste)
print('Entfernte Scheiben:', removed)

scheiben_dictionary = tc.convertListToDict(scheibenliste)

sol = cubeit(scheiben_dictionary)
printit(sol)

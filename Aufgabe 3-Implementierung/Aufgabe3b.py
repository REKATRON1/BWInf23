def hash_func(stapel):
	"""
	hash_func ordnet jedem gekürzten Stapel einen eindeutigen Index zu.
	"""
	hash_number = 0
	for index in range(len(stapel)):
		hash_number += (stapel[index]-1)*(len(stapel))**index
	return hash_number

#Ausgangsfunktions der Aufgabe 3
def pWUEFunc(stapel, index):
	"""
	pWUEFunc gibt den, beim Anwenden der PWUE-Funktion am Index index, entstehenden Stapel zurück.
	"""
	stapel_front = stapel[0:index][::-1]
	stapel_end = stapel[index+1:]
	stapel_front.extend(stapel_end)
	return stapel_front

def generate_stapelcombinations(size):
	"""
	generate_stapelcombinations gibt alle Permutationen des Stapels S=[1,2,...,size] zurück.
	(Wrapper-Funktion für generate_stapelcombinations_intern)
	"""
	return generate_stapelcombinations_intern([], [x+1 for x in list(range(size))])

def generate_stapelcombinations_intern(stapel, remaining_numbers):
	"""
	generate_stapelcombinations_intern generiert rekursiv alle Permutationen des Stapels S=[1,2,...,size]
	und gibt sie zurück.
	"""
	if len(remaining_numbers) > 0:
		return_stapel = []
		for number in remaining_numbers:
			new_stapel = stapel.copy()
			new_stapel.append(number)
			new_rem = remaining_numbers.copy()
			new_rem.remove(number)
			return_stapel.extend(generate_stapelcombinations_intern(new_stapel, new_rem))
		return return_stapel
	return [stapel]

def reduce_stapel(stapel):
	"""
	reduce_stapel 'kürzt' den stapel (vgl. Kapitel 2.2.3)
	"""
	new_stapel = list(map({j: i for i, j in enumerate(sorted(set(stapel)))}.get, stapel))
	return [x+1 for x in new_stapel]

def generiere_PWUEZahl_von_n(size):
	"""
	generiere_PWUEZahl_von_n generiert die PWUE-Zahl von size durch die Nutzung der Längen der Lösungssequenzen
	der vorherigen Schicht (size-1).
	"""
	all_stapel = generate_stapelcombinations(size)
	#1. Rekursives Generieren aller vorherigen Schichten bis n=1.
	if size == 1:
		return {0: 0}, 0, [1]
	previous_layer = generiere_PWUEZahl_von_n(size-1)[0]
	new_layer = {}
	#2a. Der einzig sortierte Stapel ist der Stapel des Formats S=[1,2,...,size], welcher von generate_stapelcombinations
	#als erster generiert wird:
	new_layer[hash_func(all_stapel[0])] = 0
	#2b. Für alle anderen Stapel...
	best_stapel = None
	for stapel in all_stapel[1:]:
		best_PWUEZahl = size
		#3a. generiere alle Stapel, die sich durch das einmalige Anwenden der PWUE-Funktion auf den Stapel ergeben
		for i in range(len(stapel)):
			#3b. und 'kürze' sie.
			new_stapel = reduce_stapel(pWUEFunc(stapel.copy(), i))
			#4a. Schlage die Länge der Lösungssequenz für die neuen Stapel in der vorherigen Schicht nach und
			#bestimme dir kürzeste eines jeden Stapels.
			if previous_layer[hash_func(new_stapel)]+1 < best_PWUEZahl:
				best_PWUEZahl = previous_layer[hash_func(new_stapel)]+1
		#Speicherung der PWUE-Zahl & des korrespondierenden Stapels
		if best_stapel == None or best_stapel[0] < best_PWUEZahl:
			best_stapel = [best_PWUEZahl, stapel]
		#4b. Speichere die kürzeste Länge einer Lösungssequenz (+1) für den Stapel im new_layer.
		new_layer[hash_func(stapel)] = best_PWUEZahl
	#Rückgabe des new_layer, der PWUE-Zahl und des 'unsortiertesten' Stapels.
	return new_layer, best_stapel[0], best_stapel[1]

def printit(i):
	current_layer, maxPWUEZ, p_stapel = generiere_PWUEZahl_von_n(i)
	print('Für n=' + str(i), 'ist die PWUE-Zahl:', str(maxPWUEZ) + ',', 'exemplarischer Stapel:', p_stapel)

printit(8)

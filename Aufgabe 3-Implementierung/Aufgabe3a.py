def pWUEFunc(liste, index):
	"""
	pWUEFunc ist die Implementierung des, in Aufgabe 3 beschriebenen, Pfannkuchen-Wende-Und-Ess-Algorithmus
	"""
	arr_front = liste[0:index][::-1]
	arr_end = liste[index+1:]
	arr_front.extend(arr_end)
	return arr_front

#Aufgabe 3a)
def generate_Loesungssequenz(liste):
	"""
	generate_Loesungssequenz generiert die Lösungssequenz für eine Liste an Pfannkuchen in Form von Indices,
	an welchen die PWUE-Funktion in der entsprechenden Reihenfolge angewendet wird.
	(Wrapper-Funktion für die rekursive, interne Funktion)
	"""
	alpha = [len(liste)] #Intiierung des Abbruchfaktors alpha als maximal
	pWUESequence = generate_Loesungssequenz_intern(liste, [], alpha) #Aufruf der Rekursiven Funktion
	return len(pWUESequence), pWUESequence #Rückgabe der Lösung der internen Funktion

def generate_Loesungssequenz_intern(liste, actions, alpha):
	"""
	generate_Loesungssequenz_intern probiert rekursiv alle möglichkeiten die PWUE-Funkion auf die, ihm übergebene, 
	Liste an Pfannkuchen anzuwenden und dadurch zu sortieren.
	"""
	#1. Überprüfe ob die Liste bereits sortiert ist und falls ja, gebe die durchgeführten actions zurück (Rekursionsanker)
	if len(liste) > 1 and not is_sorted(liste):
		#2. Generiere alle möglichen Listen durch Anwenden der PWUE-Funktion auf alle Indices der erhaltenen Liste
		shortest_action = None
		for n in range(0, len(liste)):
			#Optimierung 1: Breche das Suchen ab, falls bereits mehr actions durchgeführt wurden, als die bisher beste Lösungssequenz
			#benötigt hat, da die momentanige Sequenz nicht besser sein kann.
			if len(actions)+1 < alpha[0]:
				new_actions = actions.copy()
				new_actions.append(n)
				#3. Rufe mit der neuen Liste und der aktualisierten Lösungssequenz wieder sich selber auf (Rekursionsschritt)
				new_shortest_action_recursive = generate_Loesungssequenz_intern(pWUEFunc(liste, n), new_actions, alpha)
				if new_shortest_action_recursive == None:
					continue
				#4. Bestimme die kürzeste Lösungssequenz und...
				if shortest_action == None or len(shortest_action) > len(new_shortest_action_recursive):
					shortest_action = new_shortest_action_recursive
					#Optimierung 2: Falls die neue Lösungssequenz kürzer ist als die bisher kürzeste, aktualisiere die kürzeste.
					if len(shortest_action) < alpha[0]:
						alpha[0] = len(shortest_action)
		#4. ...gebe sie zurück.
		return shortest_action
	else:
		return actions

def is_sorted(liste):
	prev = liste[0]
	for n in range(1, len(liste)):
		if liste[n] < prev:
			return False
		else:
			prev = liste[n]
	return True


tc0 = [5,3,2,4,5,1]
tc1 = [7,6,3,1,7,4,2,5]
tc2 = [8,8,1,7,5,3,6,4,2]
tc3 = [11,5,10,1,11,4,8,2,9,7,3,6]
tc4 = [13,7,4,11,5,10,6,1,13,12,9,3,8,2]
tc5 = [14,4,13,10,8,2,3,7,9,14,1,12,6,5,11]
tc6 = [15,14,8,4,12,13,2,1,15,7,11,3,9,5,10,6]
tc7 = [16,8,5,10,15,3,7,13,6,2,4,12,9,1,14,16,11]
a, loesungssequenz = generate_Loesungssequenz(tc5)
print('Lösungssequenz:', loesungssequenz, 'Länge:', a)
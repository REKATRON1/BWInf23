import testcases as tc
import sidefunc as sf
import numpy as np
from numpy.random import choice as np_choice
import random

class DrohnenKolonie():
	"""
	Die Klasse DrohnenKolonie dient dem Generieren von einer möglichst optimalen Route durch eine Sammlung von Punkten via. ant-colony-optimization

	Variable Einstellungen:
	generieren_von_routen_einflussfaktoren(Winkel, Distanz, Gewichte, zusätzliche Polarisierung): Gewichtung verschiedener Faktoren bei dem Wählen des nächsten Punktes beim Generieren einer Route
	gewichtung_bewertung: Polarization bei der Bewertung der Routen
	menge_der_gespeicherten_routen: Menge der gespeicherten Top-Routen der vorherigen Generation (werden in nächste Generation als Vergleich übernommen) -> verhindert Verschlechterung
	verblassgeschwindigkeit_gewichte: Faktor 
	"""
	def __init__(self, punkte, generieren_von_routen_einflussfaktoren=[5, 2, 3, 3], gewichtung_bewertung=2, menge_der_gespeicherten_routen=3, verblassgeschwindigkeit_gewichte=0.85):
		"""
		Initialisierung und Instanziierung der Einstellung dieses Algorithmus
		"""
		self.punkte = punkte
		#Optimierung durch präventive Berechnung aller Winkel und Distanzen die sich in den Punkten ergeben können und Speicherung in einer Matrix
		self.distanzen_matrix = [[sf.calculate_distance(p1, p2) for p2 in punkte] for p1 in punkte]
		self.winkel_matrix = [[[sf.calculate_angle(p1, p2, p3) for p3 in punkte] for p2 in punkte] for p1 in punkte]

		#Initialisierung der konstanten Einstellungen
		self.verblassgeschwindigkeit_gewichte = verblassgeschwindigkeit_gewichte

		self.einflussfaktor_winkel = generieren_von_routen_einflussfaktoren[0]
		self.einflussfaktor_distanz = generieren_von_routen_einflussfaktoren[1]
		self.einflussfaktor_gewichte = generieren_von_routen_einflussfaktoren[2]
		self.zusaetzliche_polarisierung = generieren_von_routen_einflussfaktoren[3]

		self.polarization_inder_bewertung_von_routen = gewichtung_bewertung
		self.menge_der_gespeicherten_besten_routen = menge_der_gespeicherten_routen


	def generiere_route(self, anzahl_generationen=150, routen_pro_generation=25):
		"""
		generiere_route generiert mithilfe eines evolutionär-inspierierten Algorithmus eine möglichst kurze Route durch eine Menge an Punkten
		mit möglichst keinen spitzen Winkeln, wobei Generationen mit jeweils n Routen generiert werden, die jeweils je nach Performance Gewichte
		anpassen/justieren, welche den nachfolgenden Generationen als Wegweiser dienen.
		"""
		#Instanziierung der Gewichte.
		self.strecken_gewichtungen = np.ones((len(punkte), len(punkte)))
		beste_route = None
		vorherige_beste_routen = None
		for generation in range(anzahl_generationen):
			#Generieren aller Routen einer Generation.
			routen_einer_generation = self.generiere_routen_einer_generation(routen_pro_generation, vorherige_beste_routen)
			#Anpassen der Gewichte je nach Performance der Route in der Generation.
			self.anpassen_der_gewichte(routen_einer_generation)
			#Ermittlung der besten Routen der neuen Generation.
			vorherige_beste_routen = sorted(routen_einer_generation, key=lambda x: x[1])[:self.menge_der_gespeicherten_besten_routen]
			beste_route_aktuelle_generation = min(routen_einer_generation, key=lambda x: x[1])
			#Eventuelle Aktualisierung der insgesamt besten Route (falls beste Route der Generation besser ist als die insgesamt beste bisher gefundene Route).
			if beste_route == None:
				beste_route = beste_route_aktuelle_generation
			elif beste_route_aktuelle_generation[1] < beste_route[1]:
				beste_route = beste_route_aktuelle_generation
			#Verblassen der Gewichte, sodass der Einfluss der älteren Justierungen geringer für das Generieren neuer Routen ist, als die Justierungen neuerer Generationen.
			self.verblassen_der_gewichte()
		#Schließlich wird die beste gefundene Route zurückgegeben.
		return beste_route[2], sf.count_distances(beste_route[0], self.distanzen_matrix), [self.punkte[p] for p in beste_route[0]]

	def generiere_routen_einer_generation(self, routen_pro_generation, vorherige_beste_routen):
		"""
		generiere_routen_einer_generation generiert routen_pro_generation viele Routen unter Beachtung der entsprechenden Gewichte
		"""
		routen_einer_generation = []
		for nte_route in range(routen_pro_generation):
			#Für jede Route wird ein zufälliger Startpunkt gewählt von welchem aus die Route generiert und dann gespeichert wird.
			zufaelliger_startpunkt = random.randint(0, len(self.punkte)-1)
			route = self.generiere_einzelne_route_mit_startpunkt(zufaelliger_startpunkt)
			routen_einer_generation.append((route, self.generiere_punktzahl_der_route(route), sf.count_acute_angles(route, self.winkel_matrix)))
		#Anschließend werden die vorherigen besten Routen der Generation, als Vergleich, hinzugefügt.
		if vorherige_beste_routen != None:
			for route in vorherige_beste_routen:
				routen_einer_generation.append((route[0], route[1], route[2]))
		return routen_einer_generation

	def generiere_einzelne_route_mit_startpunkt(self, startpunkt):
		"""
		generiere_einzelne_route_mit_startpunkt generiert eine Route vom Startpunkt startpunkt unter Beachtung der entsprechenden Gewichte
		"""
		#Initialisierung der variablen zur speicherung der neuen Route und der bereits besuchten Punkte
		route = [startpunkt]
		bereits_besucht = set()
		bereits_besucht.add(startpunkt)
		vorheriger_punkt = startpunkt
		for n in range(len(self.punkte)-1):
			#Solange nicht alle Punkte in der Route erreicht wurden: Füge weiteren Punkt der Route hinzu...
			if len(route) > 1:
				naechster_punkt = self.waehle_naechsten_punkt(self.strecken_gewichtungen[vorheriger_punkt], bereits_besucht, route[-1], route[-2])
			else:
				#Falls die Route noch weniger als zwei Punkt enthält, können keine Winkel berechnet werden.
				naechster_punkt = self.waehle_naechsten_punkt(self.strecken_gewichtungen[vorheriger_punkt], bereits_besucht, route[-1])
			#Füge den neuen Punkt der Route hinzu und entferne ihn als zukünftige Option
			route.append(naechster_punkt)
			bereits_besucht.add(naechster_punkt)
			vorheriger_punkt = naechster_punkt
		#Gebe die fertige Route zurück
		return route

	def waehle_naechsten_punkt(self, strecken_gewichtungen, bereits_besucht, vorheriger_punkt1, vorheriger_punkt2=None):
		"""
		waehle_naechsten_punkt wählt aus den möglichen (noch nicht erreichten) Punkten einen zufälligen aus
		unter Beachtung der entsprechenden Gewichte, Winkel und Distanzen.
		"""
		#Übernehme die gespeicherten Gewichte für die Strecken vom derzeitigen Punkt
		gewichtungen_fuer_moegliche_naechste_punkte = np.copy(strecken_gewichtungen)
		#Entfernen der bereits benutzten Optionen
		gewichtungen_fuer_moegliche_naechste_punkte[list(bereits_besucht)] = -0.1
		#Jeder Option eine Wahrscheinlichkeit geben und strecken_gewichtungen anpassen
		gewichtungen_fuer_moegliche_naechste_punkte += 1.1
		gewichtungen_fuer_moegliche_naechste_punkte = gewichtungen_fuer_moegliche_naechste_punkte ** self.einflussfaktor_gewichte
		gewichtungen_fuer_moegliche_naechste_punkte -= 1
		gewichtungen_fuer_moegliche_naechste_punkte /= max(gewichtungen_fuer_moegliche_naechste_punkte)
		#Wahrscheiblichkeiten anpassen durch Winkel & Distanzen
		for moeglicher_naechster_punkt_index in range(len(gewichtungen_fuer_moegliche_naechste_punkte)):
			if gewichtungen_fuer_moegliche_naechste_punkte[moeglicher_naechster_punkt_index] > 0: #nur < 0, wenn bereits in Route enthalten
				if vorheriger_punkt2 != None:
					gewichtungen_fuer_moegliche_naechste_punkte[moeglicher_naechster_punkt_index] *= (self.winkel_matrix[vorheriger_punkt2][vorheriger_punkt1][moeglicher_naechster_punkt_index]/360.0) ** self.einflussfaktor_winkel * (1.0/self.distanzen_matrix[vorheriger_punkt1][moeglicher_naechster_punkt_index]) ** self.einflussfaktor_distanz
				else:
					#Falls die Route noch weniger als zwei Punkt enthält, können keine Winkel berechnet werden.
					gewichtungen_fuer_moegliche_naechste_punkte[moeglicher_naechster_punkt_index] *= (1.0/self.distanzen_matrix[vorheriger_punkt1][moeglicher_naechster_punkt_index]) ** self.einflussfaktor_distanz
		angepasste_gewichtungen = gewichtungen_fuer_moegliche_naechste_punkte ** self.zusaetzliche_polarisierung
		#Wahrscheinlichkeiten normalisieren (Summe aller Wahrscheinlichkeiten = 1)
		normalisierte_angepasste_gewichtungen = angepasste_gewichtungen / sf.sum(angepasste_gewichtungen)
		#Fehlerbehebung
		if np.isnan(normalisierte_angepasste_gewichtungen).any():
			normalisierte_angepasste_gewichtungen = np.ones(len(normalisierte_angepasste_gewichtungen))/len(normalisierte_angepasste_gewichtungen)
		#Zufällige Wahl des nächsten Punktes unter Beachtung der berechneten Gewichtungen
		naechster_punkt = np_choice(range(len(self.punkte)), 1, p=normalisierte_angepasste_gewichtungen)[0]
		#Rückgabe des gewählten Punktes
		return naechster_punkt

	def generiere_punktzahl_der_route(self, route):
		"""
		generiere_punktzahl_der_route berechnet die Punktzahl einer Route aus der Menge ihrer spitzen Winkel und ihrer Länge,
		wobei eine Route mit weniger spitzen Winkeln immer besser ist als eine kürzere Route.
		"""
		return (sf.count_acute_angles(route, self.winkel_matrix) + 1) * sf.count_distances(route, self.distanzen_matrix)

	def anpassen_der_gewichte(self, generation):
		"""
		anpassen_der_gewichte justiert die Gewichte entsprechend der verhältnismäßigen Performance der Routen einer Generation.
		"""
		#Sortieren der Routen der Generation entsprechend deren Punktzahl
		sortierte_routen = sorted(generation, key=lambda x: x[1])
		for routen_index in range(len(sortierte_routen)-1, -1, -1):
			#Berechnung der verhältnismäßigen Performance einer Route (im Vergleich zu besten Route)
			verhaeltnismaeszige_performance_faktor = (sortierte_routen[0][1]/sortierte_routen[routen_index][1]) ** self.polarization_inder_bewertung_von_routen
			if routen_index == 0 and sortierte_routen[1][2] > sortierte_routen[0][2]:
				#Falls eine Route mit Abstand die beste war: Vergebe Bonus-Punkte
				verhaeltnismaeszige_performance_faktor *= 2.5
			if verhaeltnismaeszige_performance_faktor < 1e-4:
				#Falls eine Route zu schlecht war: ziehe sie nicht in die Bewertung mit ein
				continue
			#Justiere die entsprechenden Gewichte der Route gemäß ihrer Performance
			for index_punkt_in_route in range(1, len(sortierte_routen[routen_index][0])):
				#Ignoriere dabei Strecken die für einen spitzen Winkel sorgten (zusätzliche 'Bestrafung' spitzer Winkel).
				if index_punkt_in_route < 2 or self.winkel_matrix[sortierte_routen[routen_index][0][index_punkt_in_route-2]][sortierte_routen[routen_index][0][index_punkt_in_route-1]][sortierte_routen[routen_index][0][index_punkt_in_route]] >= 90:
					self.strecken_gewichtungen[sortierte_routen[routen_index][0][index_punkt_in_route-1]][sortierte_routen[routen_index][0][index_punkt_in_route]] += verhaeltnismaeszige_performance_faktor
		#Normalisieren aller Gewichte
		for i in range(len(self.strecken_gewichtungen)):
			self.strecken_gewichtungen[i] /= sf.sum(self.strecken_gewichtungen[i])

	def verblassen_der_gewichte(self):
		"""
		verblassen_der_gewichte multipliziert alle Gewichte mit einem Faktor (<1), sodass 'ältere' Justierungen mit den Generationen einen geringeren Einfluss haben.
		"""
		for gewichte_eines_punktes in self.strecken_gewichtungen:
			gewichte_eines_punktes *= self.verblassgeschwindigkeit_gewichte


punkte = tc.convert_txtMap(tc.str_map1)
colony1 = DrohnenKolonie(punkte)
result = colony1.generiere_route(25, 25) #Dauer: ca. 20s
print('Anzahl spitzer Winkel:', result[0])
print('Länge der Route:', str(result[1])+'km')
print('Route:', result[2])
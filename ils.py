from read_excel import *
from random import *
import numpy as np
"""
Notation utilisée par la suite
L_ce  #liste customer/end office
L_ed  #liste end-office/digital hub
L_dd  #liste digital hub/digital hub le numéro en position k indique à quel hub est relié le hub k
"""

def est_plein_end_office(k,L_ce):
	utilisateurs = 0
	for i in range(len(L_ce)):
		if L_ce[i] == k:
			utilisateurs += 1
	if utilisateurs >= Uj[k-1]:
		return True
	return False

def est_plein_digital_hub(k,L_ed,L_ce):
	utilisateurs = 0
	for j in range(len(L_ed)):
		if L_ed[j] == k:
			for i in range(len(L_ce)):
				if L_ce[i] == j+1:
					utilisateurs += 1
	if utilisateurs >= Vk[k-1]:
		return True
	return False

def est_utilise_digital_hub(k,L_dd):
	return k in L_dd

def liste_hub_utilises(Ldd):
	Ldd_cycle = []
	for k in range(1,len(Ldd)+1):
		if est_utilise_digital_hub(k,Ldd):
			Ldd_cycle.append(k)
	return Ldd_cycle

def end_office_aleatoire(L_ce):
	k = 0
	trouve = False
	while not trouve:
		k = randint(1,M)
		if not est_plein_end_office(k,L_ce):
			trouve = True
	return k

def digital_hub_aleatoire(L_ce,L_ed):
	k = 0
	trouve = False
	while not trouve:
		k = randint(1,N)
		if not est_plein_digital_hub(k,L_ed,L_ce):
			trouve = True
	return k

def init_random():
	Lce=[0 for k in range(C)]
	Led = [0 for k in range(M)]
	Ldd = [0 for k in range(N)]

	clients = sample(range(1,C), int(alpha*C+1))
	for c in clients:
		end_off = end_office_aleatoire(Lce)
		Lce[c] = end_off

	for i in range(M):
		digital_hub = digital_hub_aleatoire(Lce,Led)
		Led[i] = digital_hub

	digital_hubs_obliges = []
	for i in range(len(Led)):
		if Led[i] not in digital_hubs_obliges:
			digital_hubs_obliges.append(Led[i])

	if len(digital_hubs_obliges) < 3:
		for i in range(3-len(digital_hubs_obliges)):
			digital_hubs_obliges.append(digital_hub_aleatoire(Lce,Led))

	for i in range(len(digital_hubs_obliges)-1):
		Ldd[digital_hubs_obliges[i]-1] = digital_hubs_obliges[i+1]
	Ldd[digital_hubs_obliges[-1]-1] = digital_hubs_obliges[0]
	
	return Lce,Led,Ldd


def verif(L_ce,L_ed,L_dd): #verifies it is a solution
	#Verification de alpha
	customers_pas_servis = 0
	for i in range(len(L_ce)):
		if L_ce[i] == 0:
			customers_pas_servis += 1
	if 1-(customers_pas_servis/len(L_ce)) < alpha:
		return False

	#Verification des capacites
	for i in range(1,len(L_ed)+1): #Les capacites des end office
		utilisateurs = 0
		for j in range(len(L_ce)):
			if L_ce[j] == i:
				utilisateurs += 1
		if utilisateurs > Uj[i-1]:
			return False

	for i in range(1,len(L_dd)+1): #Les capacites des digital hubs
		utilisateurs = 0
		for j in range(1,len(L_ed)+1):
			if L_ed[j-1] == i:
				for k in range(len(L_ce)):
					if L_ce[k] == j:
						utilisateurs += 1

		if utilisateurs > 0 and L_dd[i-1] == 0:
			return False
		if utilisateurs > Vk[i-1]:
			return False

	#Verifie si plus de 3 digital hubs sont selectionnes
	selectionnes = []
	for i in range(len(L_ed)):
		if L_ed[i] not in selectionnes:
			selectionnes.append(L_ed[i])
	if len(selectionnes) < 3:
		return False
	return True

def score(L_ce,L_ed,L_dd): #Calculates the objective function value for a given solution
	score = 0
	for i in range(1,len(L_ce)+1): #Cost of connecting customers to end offices
		if L_ce[i-1] != 0:
			score += hij[(i,L_ce[i-1])]

	for i in range(1,len(L_ed)+1): #Cost of connecting end offices to digital hubs and of selecting digital hubs
		score += cjk[(i,L_ed[i-1])]

	selected = []
	for i in range(1,len(L_dd)+1): #Cost of connecting digital hubs to each other
		if L_dd[i-1] != 0:
			score += gkm[(i,L_dd[i-1])]
			if L_dd[i-1] not in selected:
				score += fk[i-1]
				selected.append(L_dd[i-1])
	#score += gkm(1,L_dd(len(L_dd)))

	return score


def neighbor(Lce,Led,Ldd):
	Lce_n = swap_ce(Lce)
	Led_n = swap_ed(Led)
	Ldd_n = swap_dd(Ldd)

	Lce_n = insertion_ce(Lce_n)
	Lce_n, Led_n, Ldd_n = insertion_ed(Lce_n, Led_n, Ldd_n)
	Lce_n, Led_n, Ldd_n = insertion_dd(Lce_n, Led_n, Ldd_n)

	if score(Lce_n, Led_n, Ldd_n) < score(Lce, Led, Ldd):
		if verif(Lce_n,Led_n,Ldd_n):
			return Lce_n, Led_n, Ldd_n, True
		else:
			return Lce, Led, Ldd, False

	else:
		return Lce, Led, Ldd, False


def swap_ce(Lce):
	L_ce = Lce.copy()
	k1,k2 = randint(0, len(L_ce)-1),randint(0, len(L_ce)-1)
	
	L_ce[k1],L_ce[k2] = L_ce[k2],L_ce[k1]
	return L_ce

def insertion_ce(Lce):
	L_ce = Lce.copy()
	k = randint(0, len(L_ce)-1)
	nouveau_end_office = randint(0,M)
	L_ce[k] = nouveau_end_office
	return L_ce

def swap_ed(Led):
	L_ed = Led.copy()
	k1,k2 = randint(0, len(L_ed)-1),randint(0, len(L_ed)-1)
	
	L_ed[k1],L_ed[k2] = L_ed[k2],L_ed[k1]

	return L_ed

def insertion_ed(Lce,Led,Ldd):
	L_ce, L_ed, L_dd = Lce.copy(), Led.copy(), Ldd.copy()
	k = randint(0, len(L_ed)-1)
	nouveau_digital_hub = choice(liste_hub_utilises(L_dd))

	if nouveau_digital_hub == 0: #Le cas ou on enleve un end office (cas impossible en fait on doit tous les utiliser)
		for i in range(len(L_ce)):
			if L_ce[i] == k+1:
				L_ce[i] = end_office_aleatoire(L_ce)

	elif not est_plein_digital_hub(nouveau_digital_hub, L_ed, L_ce):
		L_ed[k] = nouveau_digital_hub

	return L_ce,L_ed,L_dd

def swap_dd(Ldd):
	L_dd = Ldd.copy()

	k1 = choice(liste_hub_utilises(Ldd))
	k2 = choice(liste_hub_utilises(Ldd))
	if not L_dd[k1-1] == k2 and not Ldd[k2-1] == k1:
		for k in range(len(Ldd)):
			if Ldd[k]==k1:
				L_dd[k]=k2
			if Ldd[k]==k2:
				L_dd[k]=k1
			if Ldd[k1-1]==k+1:
				L_dd[k2-1]=k+1
			if Ldd[k2-1]==k+1:
				L_dd[k1-1]=k+1


	return L_dd

def insertion_dd(Lce,Led,Ldd):
	L_ce, L_ed, L_dd = Lce.copy(), Led.copy(), Ldd.copy()
	choix = [i for i in range(1,len(Ldd)+1) if i not in L_dd]
	choix.append(0)
	k = choice(choix)
	
	if k != 0:
		apres_qui = choice(liste_hub_utilises(L_dd))

		L_dd[k-1] = L_dd[apres_qui-1]
		L_dd[apres_qui-1] = k
	elif len(liste_hub_utilises(L_dd)) > 3:
		supprime = choice(liste_hub_utilises(L_dd))

		for i in range(len(L_dd)):
			if L_dd[i] == supprime:
				L_dd[i] = L_dd[supprime-1]
		L_dd[supprime-1] = 0

		for i in range(len(L_ed)):
			if L_ed[i] == supprime:
				L_ed[i] = digital_hub_aleatoire(L_ce, L_ed)

	return L_ce, L_ed, L_dd

def intensification(Lce, Led, Ldd):
	compteur = 0
	while compteur < 50:
		Lce, Led, Ldd, new = neighbor(Lce, Led, Ldd)

		if new:
			compteur = 0

		else:
			compteur += 1

	return Lce, Led, Ldd


def perturbation_v1(Lce,Led,Ldd):
	compteur = 0
	while compteur < 100:
		Lce_n = swap_ce(Lce)
		Led_n = swap_ed(Led)
		Ldd_n = swap_dd(Ldd)


		Lce_n = insertion_ce(Lce_n)
		Lce_n, Led_n, Ldd_n = insertion_ed(Lce_n, Led_n, Ldd_n)
		Lce_n, Led_n, Ldd_n = insertion_dd(Lce_n, Led_n, Ldd_n)
		
		if verif(Lce_n, Led_n, Ldd_n):
			Lce,Led,Ldd = Lce_n,Led_n,Ldd_n
			compteur +=1
		else:
			pass
	return Lce, Led, Ldd


def perturbation_v2(Lce,Led,Ldd):
	compteur = 0
	while compteur < 10:
		Lce_n,Led_n,Ldd_n = double_bridge(Lce,Led,Ldd)
		if verif(Lce_n, Led_n, Ldd_n):
			Lce, Led, Ldd = Lce_n, Led_n, Ldd_n
			compteur += 1
		else:
			pass
	Lce, Led, Ldd = perturbation_v1(Lce, Led, Ldd)
	return Lce, Led, Ldd


def double_bridge(Lce, Led, Ldd):
	Lce_n, Led_n, Ldd_n = Lce.copy(), Led.copy(),Ldd.copy()
	k1 = randint(0,len(Lce)-2)
	k2 = (k1 + randint(2,len(Lce)-1))%len(Lce)
	Lce_n[k1],Lce_n[k1+1],Lce_n[k2],Lce_n[(k2+1)%len(Lce)] = Lce[k2],Lce[(k2+1)%len(Lce)],Lce[k1],Lce[k1+1]
	return Lce_n, Led_n, Ldd_n

def main():
	#Creation of the initial solution
	Lce, Led, Ldd = init_random()
	while not verif(Lce,Led,Ldd):
		Lce, Led, Ldd = init_random()

	score_min = score(Lce, Led, Ldd)
	print("score initial = ", score_min, ", solution initiale: ",Lce, Led, Ldd)
	
	for nombre in range(tours):
		Lce, Led, Ldd = intensification(Lce, Led, Ldd)

		score_min = min(score(Lce, Led, Ldd), score_min)
		if nombre % 100 == 0:
			print("tour numéro: ", nombre,"/",str(tours), ",score actuel: ",score(Lce,Led,Ldd),",score minimal :",score_min,",solution actuelle: ",Lce,Led,Ldd)
		Lce, Led, Ldd = perturbation_v2(Lce, Led, Ldd)	

	print("score final = ", score_min,", resultat final = ", Lce, Led, Ldd)
	return None

if __name__=='__main__':
	#Here you can choose if you want to load the Small or the Large problem data
	problem_size = 'Large' #'Small' or 'Large'
	tours = 5000

	#We load the corresponding data
	C,M,alpha,N,hij,cjk,gkm,fk,Uj,Vk = load_excel_data(problem_size)
	
	main()
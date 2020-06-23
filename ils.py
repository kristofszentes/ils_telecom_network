from read_excel import *
from random import *
import numpy as np
"""
Notation utilisée par la suite
L_ce  #liste customer/end office
L_ed  #liste end-office/digital hub
L_dd  #liste digital hub/digital hub le numéro en position k indique à quel hub est relié le hub k
"""


def init():
	Lce=[0 for k in range(C)]
	Led = [0 for k in range(M)]
	Ldd = [0 for k in range(N)]

	capa_end = 0
	capa_digi = 0
	compteur = 1

	for customer in range(C):
		capa_end += 1
		if capa_end <= Uj[compteur-1]:
			Lce[customer] = compteur
		else:
			capa_end = 1 #sous-entend que chaque end office a une capa de 1 minimum
			compteur += 1
			if compteur > M:
				break
			else:
				Lce[customer] = compteur

	compteur = 1

	for end in range(M):
		capa_digi += 1
		if capa_digi <= Uj[compteur-1]:
			Led[end] = compteur
		else:
			capa_digi = 1 #sous-entend que chaque hub a une capa de 1 minimum
			compteur += 1
			if compteur > N:
				break
			else:
				Led[end] = compteur

	for k in range(compteur-1):
		Ldd[k]=k+2
	Ldd[compteur-1]=1

	return Lce,Led,Ldd

def est_plein_end_office(k,L_ce):
	utilisateurs = 0
	for i in range(len(L_ce)):
		if L_ce[i] == k:
			utilisateurs += 1
	if utilisateurs >= Uj[k-1]:
		return True
	return False

def est_plein_digital_hub(k,L_ed):
	utilisateurs = 0
	for j in range(len(L_ed)):
		if L_ed[j] == k:
			utilisateurs += 1
	if utilisateurs >= Vk[k-1]:
		return True
	return False

def est_utilise_digital_hub(k,L_dd):
	return k in L_dd

def end_office_aleatoire(L_ce):
	k = 0
	trouve = False
	while not trouve:
		k = randint(1,M)
		if not est_plein_end_office(k,L_ce):
			trouve = True
	return k

def digital_hub_aleatoire(L_ed):
	k = 0
	trouve = False
	while not trouve:
		k = randint(1,N)
		if not est_plein_digital_hub(k,L_ed):
			trouve = True
	return k

def place_aleatoire(L_dd):
	return None

def init_random():
	Lce=[0 for k in range(C)]
	Led = [0 for k in range(M)]
	Ldd = [0 for k in range(N)]

	clients = sample(range(1,C), int(alpha*C))
	for c in clients:
		end_off = end_office_aleatoire(Lce)
		Lce[c] = end_off

	for i in range(M):
		digital_hub = digital_hub_aleatoire(Led)
		Led[i] = digital_hub

	digital_hubs_obliges = []
	for i in range(len(Led)):
		if Led[i] not in digital_hubs_obliges:
			digital_hubs_obliges.append(Led[i])

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
		for j in range(len(L_ed)):
			if L_ed[j] == 1:
				utilisateurs += 1
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
		selected = []
		score += cjk[(i,L_ed[i-1])]
		if L_ed[i-1] not in selected and L_ed[i-1] != 0:
			score += fk[L_ed[i-1]-1]
			selected.append(L_ed[i-1])

	for i in range(1,len(L_dd)+1): #Cost of connecting digital hubs to each other
		if L_dd[i-1] != 0:
			score += gkm[(i,L_dd[i-1])]
	#score += gkm(1,L_dd(len(L_dd)))

	return score


def neighbor(Lce,Led,Ldd):
	Lce_n, Led_n, Ldd_n = swap_ce(Lce, Led, Ldd)
	Lce_n, Led_n, Ldd_n = swap_ed(Lce_n, Led_n, Ldd_n)

	Lce_n, Led_n, Ldd_n = insertion_ce(Lce_n, Led_n, Ldd_n)
	Lce_n, Led_n, Ldd_n = insertion_ed(Lce_n, Led_n, Ldd_n)
	#Lce_n, Led_n, Ldd_n = swap_dd(Lce_n, Led_n, Ldd_n)

	if score(Lce_n, Led_n, Ldd_n) < score(Lce, Led, Ldd):
		if verif(Lce_n,Led_n,Ldd_n):
			return Lce_n, Led_n, Ldd_n, True
		else:
			return Lce, Led, Ldd, False

	else:
		return Lce, Led, Ldd, False


def swap_ce(Lce, Led, Ldd):
	L_ce, L_ed, L_dd = Lce.copy(),Led.copy(),Ldd.copy()
	k1,k2 = randint(0, len(L_ce)-1),randint(0, len(L_ce)-1)
	
	L_ce[k1],L_ce[k2] = L_ce[k2],L_ce[k1]
	return L_ce, L_ed, L_dd

def insertion_ce(Lce, Led, Ldd):
	L_ce, L_ed, L_dd = Lce.copy(),Led.copy(),Ldd.copy()
	k = randint(0, len(L_ce)-1)
	nouveau_end_office = randint(0,M)
	L_ce[k] = nouveau_end_office
	return L_ce, L_ed, L_dd

def swap_ed(Lce,Led,Ldd):
	L_ce, L_ed, L_dd = Lce.copy(), Led.copy(), Ldd.copy()
	k1,k2 = randint(0, len(L_ed)-1),randint(0, len(L_ed)-1)
	
	L_ed[k1],L_ed[k2] = L_ed[k2],L_ed[k1]

	return L_ce,L_ed,L_dd

def insertion_ed(Lce,Led,Ldd):
	L_ce, L_ed, L_dd = Lce.copy(), Led.copy(), Ldd.copy()
	k = randint(0, len(L_ed)-1)
	nouveau_digital_hub = choice(L_dd)

	if nouveau_digital_hub == 0: #Le cas ou on enleve un end office
		for i in range(len(L_ce)):
			if L_ce[i] == k+1:
				L_ce[i] = end_office_aleatoire(L_ce)

	elif not est_plein_digital_hub(nouveau_digital_hub, L_ed):
		L_ed[k] = nouveau_digital_hub

	return L_ce,L_ed,L_dd

def swap_dd(Lce,Led,Ldd):
	L_ce, L_ed, L_dd = Lce.copy(), Led.copy(), Ldd.copy()

	return L_ce,L_ed,L_dd

def insertion_dd(Lce,Led,Ldd):
	L_ce, L_ed, L_dd = Lce.copy(), Led.copy(), Ldd.copy()
	k = randint(0,len(Ldd)-1)
	choix = [i for i in range(1,len(Ldd)) if i not in L_dd]
	new_digital_hub = choice(choix)
	old_digital_hub = L_dd[k]
	
	if old_digital_hub != 0:
		L_dd[new_digital_hub-1] = L_dd[old_digital_hub-1]
		L_dd[old_digital_hub-1] = 0
		L_dd[k] = new_digital_hub

	else:
		choix2 = [i for i in L_dd if i != 0]
		apres_qui = choice(choix2)

		L_dd[new_digital_hub-1] = L_dd[apres_qui-1]
		L_dd[apres_qui-1] = k+1
		L_dd[k] = new_digital_hub

	for i in range(len(L_ed)):
		if L_ed[i] == old_digital_hub:
			L_ed[i] = new_digital_hub

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
		Lce_n, Led_n, Ldd_n = swap_ce(Lce, Led, Ldd)
		Lce_n, Led_n, Ldd_n = swap_ed(Lce_n, Led_n, Ldd_n)
		
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
	Lce, Led, Ldd = init()
	print("solution initiale: ",Lce, Led, Ldd)
	score_min = score(Lce, Led, Ldd)
	print("score initial = ", score_min)
	for nombre in range(5000):
		Lce, Led, Ldd = intensification(Lce, Led, Ldd)

		score_min = min(score(Lce, Led, Ldd), score_min)
		if nombre % 1000 == 0:
			print(score(Lce,Led,Ldd))
		Lce, Led, Ldd = perturbation_v2(Lce, Led, Ldd)
		if nombre % 1000 == 0:
			print(nombre,score_min)

	print("score final = ", score_min)
	print("resultat final = ", Lce, Led, Ldd)
	return

main()
#Lce, Led, Ldd = init()
#print("init = ", score(Lce,Led,Ldd))

#Lce, Led, Ldd = intensification(Lce, Led, Ldd)
#print("intense = ", score(Lce,Led,Ldd))

#Lce, Led, Ldd = perturbation(Lce,Led,Ldd)
#print("ok?")
#Lce, Led, Ldd = intensification(Lce, Led, Ldd)
#print("intense = ", score(Lce,Led,Ldd))



#print(verif(LCE,LED,LDD))


from read_excel import *
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
	for i in range(len(L_ce)): #Cost of connecting customers to end offices
		score += hij(i,L_ce[i])

	for i in range(len(L_ed)): #Cost of connecting end offices to digital hubs and of selecting digital hubs
		selected = []
		score += cjk(i,L_ed[i])
		if L_ed[i] not in selected:
			score += fk[L_ed[i]]
			selected.append(L_ed[i])

	for i in range(len(L_dd) - 1): #Cost of connecting digital hubs to each other
		score += gkm(L_dd(i,i+1))
	score += gkm(0,L_dd(len(L_dd)))

	return score

def neighbor():
	return None

def swap(Lce,Led,Ldd):


	return None

def intensification():
	return None

def perturbation():
	return None

LCE,LED,LDD=init()

print(verif(LCE,LED,LDD))
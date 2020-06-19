from read_excel import *
"""
Notation utilisée par la suite
L_ce  #liste customer/end office
L_ed  #liste end-office/digital hub
L_dd  #liste digital hub/digital hub
"""



def init():
	Lce=[[0 for k in range(M)]for l in range(C)]
	Led = [[0 for k in range(N)] for l in range(M)]
	Ldd = [[0 for k in range(N)] for l in range(N)]

	capa_end = 0
	capa_digi = 0
	compteur = 0

	for customer in C:
		capa_end += 1
		if capa_end <= Uj[compteur]:
			Lce[customer][compteur] = 1
		else:
			capa_end = 1
			compteur += 1
			if compteur > M:
				break
			else:
				Lce[customer][compteur] = 1

	compteur = 0

	for end in M:
		capa_digi += 1
		if capa_digi <= Uj[compteur]:
			Lce[customer][compteur] = 1
		else:
			compteur += 1
			if compteur > M:
				break
			else:
				Lce[customer][compteur] = 1


	return None

def verif(L_ce,L_ed,L_dd): #verifies it is a solution
	return None

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

def swap():
	return None

def intensification():
	return None

def perturbation():
	return None


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
        score += hij[(i,L_ce[i-1])]

    for i in range(1,len(L_ed)+1): #Cost of connecting end offices to digital hubs and of selecting digital hubs
        selected = []
        score += cjk[(i,L_ed[i-1])]
        if L_ed[i-1] not in selected:
            score += fk[L_ed[i-1]]
            selected.append(L_ed[i-1])

    for i in range(1,len(L_dd)+1): #Cost of connecting digital hubs to each other
        if L_dd[i-1] != 0:
            score += gkm[(i,L_dd[i-1])]
    #score += gkm(1,L_dd(len(L_dd)))

    return score


def neighbor(Lce,Led,Ldd):
    Lce_n, Led_n, Ldd_n = swap(Lce, Led, Ldd)
    if score(Lce_n, Led_n, Ldd_n) < score(Lce, Led, Ldd):
        if verif(Lce_n,Led_n,Ldd_n):
            return Lce_n, Led_n, Ldd_n, True
        else:
            return Lce, Led, Ldd, False

    else:
        return Lce, Led, Ldd, False


def swap(Lce, Led, Ldd):
    L_ce, L_ed, L_dd = Lce.copy(),Led.copy(),Ldd.copy()
    k1, k2 = randint(0, len(L_ce)-1), randint(0, len(L_ce)-1)
    L_ce[k1], L_ce[k2] = L_ce[k2], L_ce[k1]

    k1, k2 = randint(0, len(L_ed) - 1), randint(0, len(L_ed) - 1)
    L_ed[k1], L_ed[k2] = L_ed[k2], L_ed[k1]

    k11, k22 = L_ed[k1], L_ed[k2]

    if L_dd[k11] == 0 and L_dd[k22 != 0]:
        L_dd[k11], L_dd[k22] = L_dd[k22], L_dd[k11]
        for i in range(len(Ldd)):
            if L_dd[i] == k22:
                L_dd[i] = k11

    elif L_dd[k22] == 0 and L_dd[k11 != 0]:
        L_dd[k22], L_dd[k11] = L_dd[k11], L_dd[k22]
        for i in range(len(Ldd)):
            if L_dd[i] == k11:
                L_dd[i] = k22

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



def perturbation(Lce,Led,Ldd):
    compteur = 0
    while compteur < 100:
        Lce_n, Led_n, Ldd_n = swap(Lce, Led, Ldd)
        if verif(Lce_n, Led_n, Ldd_n):
            Lce,Led,Ldd = swap(Lce_n,Led_n,Ldd_n)
            compteur +=1
        else:
            pass
    return Lce, Led, Ldd

def main():
    Lce, Led, Ldd = init()
    score_min = score(Lce, Led, Ldd)
    print("score initial = ", score_min)
    for nombre in range(30):
        Lce, Led, Ldd = intensification(Lce, Led, Ldd)

        score_min = min(score(Lce, Led, Ldd), score_min)

        Lce, Led, Ldd = perturbation(Lce, Led, Ldd)

    print("score final = ", score_min)
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


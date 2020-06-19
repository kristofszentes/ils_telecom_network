from read_excel import *
"""
Notation utilisée par la suite
L_ce  #liste customer/end office
L_ed  #liste end-office/digital hub
L_dd  #liste digital hub/digital hub
"""

#Données
InputData = "InputDataTelecomSmallInstance.xlsx"
# Input Data Preparation #
def read_excel_data(filename, sheet_name):
    data = pd.read_excel(filename, sheet_name=sheet_name, header=None)
    values = data.values
    if min(values.shape) == 1:  # This If is to make the code insensitive to column-wise or row-wise expression #
        if values.shape[0] == 1:
            values = values.tolist()
        else:
            values = values.transpose()
            values = values.tolist()
        return values[0]        
    else:
        data_dict = {}
        if min(values.shape) == 2:  # For single-dimension parameters in Excel
            if values.shape[0] == 2:
                for i in range(values.shape[1]):
                    data_dict[i+1] = values[1][i]
            else:
                for i in range(values.shape[0]):
                    data_dict[i+1] = values[i][1]
                
        else:  # For two-dimension (matrix) parameters in Excel
             for i in range(values.shape[0]):
                for j in range(values.shape[1]):
                    data_dict[(i+1, j+1)] = values[i][j]
        return data_dict
 
   # This section defines the functions used for onstraint 5 #
#Create sets
set_C=[i for i in range (1,16)]
set_M=[j for j in range (1,9)]
set_N=[k for k in range (1,7)]
C=len(set_C)
    
    
    
#parameters
alpha= read_excel_data(InputData, "alpha")
alpha=alpha[0]
# print("alpha: ", alpha)
    
#arrays
Uj= read_excel_data(InputData, "TargetCapicity(Uj)")
#print(Uj)
    
Vk = read_excel_data(InputData, "SteinerCapacity(Vk)")
# print(Vk)
    
fk= read_excel_data(InputData, "SteinerFixedCost(fk)")
#print(fk)
    
gkm= read_excel_data(InputData, "SteinerToSteinerConnctCost(gkm)")
# print(gkm)
    
cjk=read_excel_data(InputData, "TargetToSteinerAllocCost(cjk)")
# print(cjk)
    
hij= read_excel_data(InputData, "CustToTargetAllocCost(hij)")
#print(hij)

def init():
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

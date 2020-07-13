# Import PuLP modeler functions
from pulp import *
import pandas as pd
import numpy as np
import itertools
import math as mt
import os

if __name__ == "__main__":
    
    InputData = os.path.join("inputData","InputDataTelecomSmallInstance.xlsx")

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

    #ensembles
    set_Customer=[i for i in range (1, 16)]
    set_EndOffice=[j for j in range (1, 9)]
    set_Digit=[k for k in range (1, 7)]
    C=len(set_Customer)
    
    
    
    #parametres
    alpha= read_excel_data(InputData, "alpha")
    alpha=alpha[0]
   
    Uj= read_excel_data(InputData, "TargetCapicity(Uj)")
    Vk = read_excel_data(InputData, "SteinerCapacity(Vk)")
    fk= read_excel_data(InputData, "SteinerFixedCost(fk)")
    gkm= read_excel_data(InputData, "SteinerToSteinerConnctCost(gkm)")
    cjk=read_excel_data(InputData, "TargetToSteinerAllocCost(cjk)")
    hij= read_excel_data(InputData, "CustToTargetAllocCost(hij)")
    
    ##Create variables
    x= LpVariable.dicts('x', (set_Customer, set_EndOffice), 0, 1, "Binary")
    y= LpVariable.dicts('y', (set_EndOffice, set_Digit), 0, 1, "Binary")
    z= LpVariable.dicts('z', (set_Digit, set_Digit), 0, 1, "Binary")
    l= LpVariable.dicts('l', set_Digit, 0, 1, "Binary")
    p = LpVariable.dicts('p', (set_Customer, set_EndOffice, set_Digit), 0, 1, "Binary")
    cost=LpProblem("total cost", LpMinimize)
    
    #Objective function 
    cost += lpSum(hij[i,j] * x[i][j] for i in set_Customer for j in set_EndOffice) + lpSum (cjk[j, k] * y[j][k] for j in set_EndOffice for k in set_Digit) + lpSum(fk[k - 1] * l[k] for k in set_Digit) + lpSum(gkm[k, m] * z[k][m] for m in set_Digit for k in set_Digit)
    
    #Contraintes
    for i in set_Customer:
        for j in set_EndOffice:
            for k in set_Digit:
                cost += p[i][j][k] <= x[i][j]
                cost += p[i][j][k] <= y[j][k]
                cost += p[i][j][k] >= x[i][j] + y[j][k] - 1
    
    for k in set_Digit:
        cost += z[k][k] == 0
    
    #Condition 1
    for i in set_Customer:
        cost += lpSum(x[i][j] for j in set_EndOffice) <= 1
    
    #Condition 2
    for j in set_EndOffice:
        cost += lpSum(y[j][k] for k in set_Digit) == 1
    #Condition 3
    for j in set_EndOffice:
        for k in set_Digit:
            cost += y[j][k] <= l[k]
    #Condition 4
    for k in set_Digit:
        cost += lpSum(z[k][m] + z[m][k] for m in set_Digit) == 2 * l[k]
         
    #Condition 5
    for n_hub in range(3, len(set_Digit) + 1): # at least 3 hubs!
        Tuples = itertools.combinations(set_Digit, n_hub)
        for S in Tuples:
            S2 = set_Digit.copy()
            for k in S:
                S2.remove(k)
            for n in S:
                S3 = list(S)
                S3.remove(n)
                if n_hub == len(set_Digit) :
                    cost += lpSum(lpSum(z[k][m] for k in S) for m in S) <= 2*(lpSum(l[k] for k in S3) + 1)
                    for t in S2:
                        cost += lpSum(lpSum(z[k][m] for k in S) for m in S) <= 2*(lpSum(l[k] for k in S3) + 1 - l[t])   
     
    
    #Condition 6
    for j in set_EndOffice:
        cost += lpSum(x[i][j] for i in set_Customer) <= Uj[j - 1]
    
    #Condition 7
    
    for k in set_Digit:
        cost += lpSum(p[i][j][k] for i in set_Customer for j in set_EndOffice) <= Vk[k - 1]
        
    #Condition 8
    cost += lpSum(l[k] for k in set_Digit) >= 3  #int object is not subscriptable
    #Condition 9
    cost += lpSum(x[i][j] for i in set_Customer for j in set_EndOffice) >= alpha * C
    
    cost.solve()
    
    print("Status:", LpStatus[cost.status])
    print("Objective value Cost = ", value(cost.objective))
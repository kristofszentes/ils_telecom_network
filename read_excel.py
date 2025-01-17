import pandas as pd
import numpy as np
import os

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
"""
# This section reads the data from Excel #

"""

def load_excel_data(size):
    InputData = os.path.join("inputData","InputDataTelecom" + size + "Instance.xlsx")
    C = read_excel_data(InputData, "C")[0]
    M = read_excel_data(InputData, "M")[0]
    alpha=read_excel_data(InputData,"alpha")[0]
    N=read_excel_data(InputData,"N")[0]
    hij=read_excel_data(InputData,"CustToTargetAllocCost(hij)")
    cjk=read_excel_data(InputData,"TargetToSteinerAllocCost(cjk)")
    gkm=read_excel_data(InputData, "SteinerToSteinerConnctCost(gkm)")
    fk=read_excel_data(InputData, "SteinerFixedCost(fk)")
    Uj=read_excel_data(InputData,"TargetCapicity(Uj)")
    Vk=read_excel_data(InputData, "SteinerCapacity(Vk)")
    print("excel loaded")
    return C,M,alpha,N,hij,cjk,gkm,fk,Uj,Vk

"""print("C: ",C)
print("M: ", M)
print("alpha: ", alpha)
print("N: ",N)
print("hij: ",hij)
print("cjk: ",cjk)
print("gkm: ", gkm)
print("fk: ",fk)
print("Uj: ", Uj)
print("Vk: ",Vk)"""

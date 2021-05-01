# -*- coding: utf-8 -*-
"""
Created on Sat May  1 12:27:22 2021

@author: Yosshua
"""


import pandas as pd
import numpy as np

def group(df):
    t = len(df.columns.values)
    ans = {}
    names = df.columns.values
    for index,row in df.iterrows():                
        for j in range(t-1): 
            index = str(j)                     
            llaveCol = str(row[j])
            llaveClase = str(row[t-1])  
            if index not in ans:
                ans[index] = {}
            if llaveCol not in ans[index]:
                ans[index][llaveCol] = {}                          
            if llaveClase not in ans[index][llaveCol]:
                ans[index][llaveCol][llaveClase] = 0                  
            ans[index][llaveCol][llaveClase]+=1                        
    return ans
        
def getEntrophy(dct, n):

    ent = [0]*len(dct)
    j = 0
    for col in dct.keys():                         
        for colVal in dct[col].keys():
            det = 0            
            aux = np.zeros(len(dct[col][colVal].keys()))
            i = 0            
            for clas in dct[col][colVal].keys():
                det+= dct[col][colVal][clas]
                aux[i] = dct[col][colVal][clas]
                i+=1
            aux = 1/det*aux
            aux_copy = aux.copy()
            aux = np.log2(aux)            
            s = sum(np.multiply(aux_copy,aux))            
            ent[j] += (-1*det/n*s)
        j+=1                                             
    return ent
        
        

fileName = "car.csv"
df = pd.read_csv(fileName, encoding='utf-8', sep =',')

dct = group(df)
ent = getEntrophy(dct, len(df))
print("Entrophy by column", ent)






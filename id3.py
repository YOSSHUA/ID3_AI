# -*- coding: utf-8 -*-
"""
Created on Sat May  1 12:27:22 2021

@author: Yosshua
"""


import pandas as pd
import numpy as np
import json

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
    """
        dct es un diccionario que agrupa por columna, clase y conteo
        n es el total de registros en la tabla
    """
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
        

def makeID3(df):
    global ans
    if len(df) == 0:
        return
    dct = group(df)
    ent = getEntrophy(dct, len(df))
    indMin = ent.index(min(ent)) #Columna que determina
    dictMin = dct[str(indMin)] #Dict con las dif clases de la col. que determina
    #Recorremos las clases de la col que determina
    for i in dictMin.keys():      
        llaves = list(dictMin[i].keys()) #Clases del valor de la columna i-esima
        if len(llaves) == 1:
            #Ya determina por si sola'
            if df.columns.values[indMin] not in ans.keys():   
                ans[df.columns.values[indMin]] ={}            
            ans[df.columns.values[indMin]].update({i:llaves[0] }) 
        else:                        
            if df.columns.values[indMin] not in ans.keys():   
                ans[df.columns.values[indMin]] ={}            
            ans[df.columns.values[indMin]].update({i:"nextKey"})   
            
            #Sacamos los registros donde la Columna(indMin) que determina es igual a la llave i
            auxDf = df[df[df.columns.values[indMin]] ==  i]
            #Le quitamos la columna que determina(indMin)
            auxDf = auxDf.drop(auxDf.columns[indMin], axis=1)
            makeID3(auxDf)
    

ans = {}
fileName = "clima.csv"
df = pd.read_csv(fileName, encoding='utf-8', sep =',')
makeID3(df)
s1 = json.dumps(ans)
js = json.loads(s1)
print(json.dumps(js, indent=4))

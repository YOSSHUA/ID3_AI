# -*- coding: utf-8 -*-
"""
Created on Sat May  1 12:27:22 2021

@author: Yosshua
"""


import pandas as pd
import numpy as np
import json

def group(df):
    """
    df - A dataFrame where the last column is the Class given the features un the other columns
    This function return  a dictionary that count for each column for each column_value how many records are there, grouped by class_value.
        {
            "col_1":{
                    "key_1":{
                        "class_1":{
                            len(  df[df['col_1'] == "key_1" and df["class"] == "class_1"]  )
                        },
                        ...
                        "class_n":{
                            len(  df[df['col_1'] == "key_1" and df["class"] == "class_n"]  )
                        }
                    
                    }
                    
             },
             ...
             
             "col_n":{
                    "key_1":{
                        "class_1":{
                            len(  df[df['col_n'] == "key_1" and df["class"] == "class_1"]  )
                        },
                        ...
                        "class_n":{
                            len(  df[df['col_n'] == "key_1" and df["class"] == "class_n"]  )
                        }
                    
                    }             
            }                     
        }
    
    """
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
        
def getEntrophy(df):
    """    
        dct es un diccionario que agrupa por columna, clase y conteo
        n es el total de registros en la tabla        
    """
    dct = group(df)
    n = len(df)
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
    return (ent,dct)
        

def makeID3(df, father, key ):
    global ans
    if len(df) == 0:
        return    
    ent,dct = getEntrophy(df)
    indMin = ent.index(min(ent)) #Columna que determina        
    dictMin = dct[str(indMin)] #Dict con las dif clases de la col. que determina
    #Recorremos las clases de la col que determina
    for i in dictMin.keys():           
        llaves = list(dictMin[i].keys()) #Clases del valor de la columna i-esima
        if len(llaves) == 1:
            #Ya determina por si sola'                    
                        
            #Me pongo en el dict de mi padre
            if father != "":
                if father not in ans.keys():   
                    ans[father] ={}                                     
                ans[father].update({key : df.columns.values[indMin]})                
                
            #Lleno el mio
            if df.columns.values[indMin] not in ans.keys():   
                ans[df.columns.values[indMin]] ={}            
            ans[df.columns.values[indMin]].update({i:"final: "+llaves[0] }) 
                
        else:           
            #Me pongo en el dict de mi padre                
            if father != "":
                if father not in ans.keys():   
                    ans[father] ={}                     
                ans[father].update({key : df.columns.values[indMin]})               
            #Sacamos los registros donde la Columna(indMin) que determina es igual a la llave i
            auxDf = df[df[df.columns.values[indMin]] ==  i]
            #Le quitamos la columna que determina(indMin)
            auxDf = auxDf.drop(auxDf.columns[indMin], axis=1)
            
            makeID3(auxDf, df.columns.values[indMin], i)
    

ans = {}
fileName = "car.csv"
df = pd.read_csv(fileName, encoding='utf-8', sep =',')
makeID3(df,"", "")
s1 = json.dumps(ans)
js = json.loads(s1)
print(json.dumps(js, indent=4))

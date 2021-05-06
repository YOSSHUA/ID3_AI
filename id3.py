# -*- coding: utf-8 -*-
"""
Created on Sat May  1 12:27:22 2021

@author: Yosshua

"""


import pandas as pd
import numpy as np
import json
from tkinter import *
import tkinter as tk

def group(df):
    """
    df - A dataFrame where the last column is the Class given the features un the other columns
    This function return  a dictionary of the type, i.e., count for each column for each column_value how many records are there grouped by class_value.
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
            if len(df.columns.values) == 2:
                #Ya llegué a la última columna pero sigue sin determinarse este caso
                #Me pongo en el dict de mi padre
                if father != "":
                    if father not in ans.keys():   
                        ans[father] ={}                                     
                    ans[father].update({key : df.columns.values[indMin]})                
                    
                #Lleno el mio
                if df.columns.values[indMin] not in ans.keys():   
                    ans[df.columns.values[indMin]] ={}            
                ans[df.columns.values[indMin]].update({i:"final: opciones: "+str(llaves) }) 
                
                return
            
                
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
    

def read():    
    fileName = "breast_cancer.csv"           
    #fileName = "clima.csv"
    return fileName
    
def process():    
    fileName = read()
    #df = pd.read_csv(fileName, encoding='utf-8', sep =',') 
    
    #Para el de cancer
    header =["Class","age","menopause","tumor_size","inv_nodes",	"node_caps","deg_malig","breast","breast_quad","irradiat"]    
    df = pd.read_csv(fileName, encoding='utf-8', sep =',', names=header, header=None) 
    header =["age","menopause","tumor_size","inv_nodes","node_caps","deg_malig","breast","breast_quad","irradiat","Class"]    
    df = df[header]
    #Aqui termina
    
    
    df = df.applymap(str)
    global ans
    ans ={}    
    makeID3(df,"","")
    
    return df

def printJson():
    global ans
    s1 = json.dumps(ans)
    js = json.loads(s1)
    return json.dumps(js, indent=4)


def getResult():
    global txtRes
    global strs
    global df
    global ans
    feat = {}
    i = 0
    for a in strs:
        feat.update({str(df.columns.values[i]):str(a.get())})  
        i+=1
    curClass = list(ans.keys())[0]    
    txtRes.set(dfs(ans, curClass, feat))    
    
def dfs( dct,curClass, features): 
    if "final" in str(dct[curClass][features[curClass]]):
        return dct[curClass][features[curClass]]
    else:
        return dfs(dct, dct[curClass][features[curClass]],features)    
    

def getInferenceLaws( dct, nomColumna, reglaAct, father):
    global reglas
    for cat, opc in dct[nomColumna].items():
        aux = reglaAct
        if "final" in opc:
            if len(reglaAct) == 0:
                aux+= ("Si "+ str(nomColumna) + " = " + str(cat) + " entonces la clase es " + str(opc))
            else:
                #Agregar and 
                aux+=(" y si "+ str(nomColumna) + " = " + str(cat) + " entonces la clase es " + str(opc))
            reglas.append(aux)            
        else:
            if father not in reglaAct:
                #Nos manda a otra columna
                if len(aux) == 0:
                    aux+=("Si "+ str(nomColumna) + " = " + str(cat))
                else:
                    #Agregar and 
                    aux+=(" y si "+ str(nomColumna) + " = " + str(cat))            
                getInferenceLaws(dct, opc, aux, nomColumna)            
  
    

import tkinter.scrolledtext as st   
ans = {}
df = process()
reglas = []
getInferenceLaws(ans, list(ans.keys())[0], "","666")


txtJsonStr = printJson()
txtReglas =""
for j in reglas:
    txtReglas+= j+"\n\n"
main = Tk()
txtRes = tk.StringVar()
main.title("ID3")
lbls = []
txts = []
strs = []
for i in range(len(df.columns.values)-1):
    OPTIONS = list(df[df.columns.values[i]].unique())
    stri = tk.StringVar()
    stri.set(OPTIONS[0])
    l1 = Label(main,  text=df.columns.values[i], width=10 )  # added one Label 
    l1.grid(row=i+1,column=1) 
    lbls.append(l1)
    txt = OptionMenu(main, stri, *OPTIONS)
    #txt = Entry(main, textvariable=stri)
    txt.grid(row=i+1,column=2)
    txts.append(txt)    
    strs.append(stri)

btn = Button(main,text='Obtener resultado', command=getResult)
btn.grid(row = 1, column = 4)

resl = Label(main,  text="Resultado de clase "+ df.columns.values[-1]+" :")  # added one Label 
resl.grid(row=3,column=3) 

res = Entry(main, textvariable=txtRes, width=30)
res.grid(row= 3,column = 4)


text_area = st.ScrolledText(main,
                            width = 60, 
                            height = 25, 
                            font = ("Times New Roman",
                                    12))
  
text_area.grid(row=len(df.columns.values)+2,column=1, pady = 10, padx = 10)
  
# Inserting Text which is read only
text_area.insert(tk.INSERT,txtJsonStr)
  
# Making the text read only
text_area.configure(state ='disabled')


laws = st.ScrolledText(main,
                            width = 80, 
                            height = 25, 
                            font = ("Times New Roman",
                                    12))
  
laws.grid(row=len(df.columns.values)+2,column=3)
  
# Inserting Text which is read only
laws.insert(tk.INSERT,txtReglas)
  
# Making the text read only
laws.configure(state ='disabled')




main.mainloop()


    

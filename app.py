from flask import Flask, render_template,  redirect, url_for, escape, request
import json
import datetime
import sys
import os
import pandas as pd
import numpy as np
import random
#import conn

   

app = Flask(__name__)

arreglo = []

def ordenarSegundo(val):
    return val[1]
def getprimero(val):
    return val[0]


def test():
    generacion = 0
    p = Poblacion()
    fin = Criterio(p)
    while (fin == None):
        padres = Seleccionar(p,1)
        p = Emparejar(padres)
        fin = Criterio(p)
        generacion += 1
        #print(generacion)
    print("SOLUCION: ", fin)
    print("GENERACION: ", generacion)
    return "hola"

@app.route("/home")
def clientes():
    return render_template("index.html")

@app.route("/entrenar",methods=['POST'])
def entrenar():
    global arreglo
    f = request.files['archivo']
    f.save(os.path.join("./archivo", "archivo.csv"))
    data = pd.read_csv(os.path.join("./archivo","archivo.csv"))
    arreglo = data.to_numpy()
    test()
    return "hoña"



def Poblacion():
    result = []
    for i in range(16):
        result.append(Inicializar())
    #print(result)    
    return result 

def Criterio(po):
    result = None
    fit = []
    fitnesFinal = 15
    for i in range(16):
        pts = Evaluar(po[i])
        fit.append(pts)
        if(pts < fitnesFinal):
            return po[i]
    return None

            

def Evaluar(p):
    nc = 0
    error = 0 
    print("Evaluando:  ", p)
    for a in arreglo:
        nc = p[0] * a[0] +  p[1] * a[1] + p[2] * a[2]
        error += (a[3] - nc)**2  
    error *= 1/len(arreglo)
    print("Resultado :" , error)
    return error 

def Inicializar():
    mat = []
    for i in range(8):
        mat.append(random.uniform(-1,1))
    return mat


def Seleccionar(p,i):
    #LOS MEJORES 8 PADRES
    resultado = []
    if(i == 1):
        for item in p:
            resultado.append((item,Evaluar(item)))
        resultado.sort(key= ordenarSegundo )
        resultado = resultado[:8]
        resultado = list(map(getprimero,resultado))
        return resultado
    return None

def Emparejar(po):
    h1 = Cruzar(po[0],po[7])
    h2 = Cruzar(po[1],po[6])
    h3 = Cruzar(po[2],po[5])
    h4 = Cruzar(po[3],po[4])
    h5 = Cruzar(po[0],po[1])
    h6 = Cruzar(po[2],po[3])
    h7 = Cruzar(po[4],po[5])
    h8 = Cruzar(po[6],po[7])
    po.append(Mutar(h1))
    po.append(Mutar(h2))
    po.append(Mutar(h3))
    po.append(Mutar(h4))
    po.append(Mutar(h5))
    po.append(Mutar(h6))
    po.append(Mutar(h7))
    po.append(Mutar(h8))
    return po

def Cruzar(p1,p2):
    hijo = [-1,-1,-1]
    hijo[0] = p1[0] if random.uniform(0,1)>0.5 else p2[0]
    hijo[1] = p1[1] if random.uniform(0,1)>0.5 else p2[1]
    hijo[2] = p1[2] if random.uniform(0,1)>0.5 else p2[2]
    return hijo
    

def Mutar(hijo):
    pos = random.randrange(0,3)
    hijo[pos] += random.uniform(-0.3,0.3) 
    return hijo


#@app.route("/ingresoCliente",methods=['POST'])
#def ingresoclientes(): 
#    nit = request.form['nit']
#    usuario = request.form['username']
#    monto = request.form['monto']
#    direccion = request.form['direccion']
#    telefono = request.form['telefono']
#    email = request.form['email']
#    regimen = request.form['regimen']
#    saldo = request.form['saldo']
#    sql = "INSERT INTO cliente (NIT,NOMBRE,MENSUAL,DIRECCION,TELEFONO,EMAIL,REGIMEN,SALDO) VALUES(%i,'%s',%f,'%s','%s','%s','%s',%f)" % (int(nit),usuario,float(monto),direccion,telefono,email,regimen,float(saldo))
#    run_query(sql)
#    return  redirect(url_for('clientes'))
  

if __name__ == "__main__":
    app.run(debug=True)



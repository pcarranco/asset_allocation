# Crear portafolios de renta fija y renta variabled

from numpy.compat.py3k import contextlib_nullcontext
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook as cbook
import matplotlib.ticker as mtick

# ________________________________ Cálculo de variaciones ____________________________

def variaciones():
    df = pd.read_csv('data.csv',header=0,index_col=0, parse_dates=['Fecha'])
    for col in df:
        df[col] = df[col]/df[col].shift(1)
    
    df.dropna(inplace=True)
    return df

# ________________________ Funciones cálculo métricas de portafilios __________________

def rendimiento_port(vars, wgts):
    
    rend=  (vars.mean()**12)-1
    
    rend = rend*wgts
    
    return rend.sum() * 100

def volatilidad_port(vars, wgts):
    
    covs =np.array(vars.cov())
    
    arr = np.array(wgts)
    
    arr = arr*arr.reshape(len(wgts),1)
    
    var = arr * covs
    
    return np.sqrt(np.sum(var))*np.sqrt(12) * 100

# _________________________ Funciones de visualización de datos _____________________

def graficar_portafolios(rends, vols):

    plt.plot(vols, rends)
    plt.show()

# ____________________________ Simulaciones __________________________________

def simulacion_portafilio_2_activos(nportafolios):
    
    var = variaciones()
    var.drop(['RF 0-1', 'RF 1-5'],axis=1,inplace=True)

    wgtsList = []
    n = 0
    salto = 1/nportafolios
    
    for _ in range(nportafolios):
       w = [round(1-n,2),round(n,2)]
       wgtsList.append(w)
       n+=salto
    
    rends = []
    vols = []
    
    for comb in wgtsList:
        rport = rendimiento_port(var,comb) 
        vport = volatilidad_port(var, comb)

        rends.append(rport)
        vols.append(vport)
        
    graficar_portafolios(rends, vols)
    
if __name__ == '__main__':
    simulacion_portafilio_2_activos(100)
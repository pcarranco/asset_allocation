# Crear portafolios de renta fija y renta variabled

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ________________________________ Cálculo de variaciones ____________________________

def variaciones_csv(filepath):
    df = pd.read_csv(filepath,header=0,index_col=0, parse_dates=[0])
    df = df/df.shift(1)
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
    plt.xlabel = 'Volatilidad'
    plt.ylabel = 'Rendimiento'
    plt.legend()
    plt.show()

def graficar_3_curvas(rends, vols):

    plt.plot(vols[0], rends[0], label='Largo Plazo')
    plt.plot(vols[1], rends[1], label='Mediano Plazo')
    plt.plot(vols[2], rends[2], label='Corto Plazo')
    plt.xlabel = 'Volatilidad'
    plt.ylabel = 'Rendimiento'
    plt.legend()
    plt.show()
    
def graficar_retornos(filepath, start=None, end=None, series=[]):

    var = variaciones_csv(filepath)
    
    if not series:
        fig = var.loc[start:end,:]
    else:
        fig = var.loc[start:end, series]
    fig = fig.cumprod() * 100
    
    fig.plot()
    plt.show()
    
def graficar_retorno_volatilidad(filepath, start=None, end=None,series=[]):

    var = variaciones_csv(filepath)
    
    if not series:
        fig = var.loc[start:end,:]
    else:
        fig = var.loc[start:end, series]
    
    rend = ((fig.mean() ** 12) -1) * 100
    vols = fig.std() * np.sqrt(12) * 100
    

    for i in range(len(rend)):
        plt.scatter(vols[i],rend[i], label = rend.index[i], alpha=0.8, edgecolors='none')
    plt.legend()
    plt.grid(True)
    plt.show()
    
# ____________________________ Simulaciones __________________________________

def simulacion_portafilio_2_activos(filepath, series, start=None, end=None, nportafolios=20):
    
    var = variaciones_csv(filepath)
    
    var = var.loc[start:end, series]
        
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
    
def simulacion_3_curvas(nportafolios):
    
    
    cols = [[0,1],[1,2],[2,3]]
    

    wgtsList = []
    n = 0
    salto = 1/nportafolios
    
    for _ in range(nportafolios):
       w = [round(1-n,2),round(n,2)]
       wgtsList.append(w)
       n+=salto
    
    rends = []
    vols = []
    for n in cols:
        
        var = variaciones_csv()
        var.drop(var.columns[n],axis=1,inplace=True)
        
        curvar = []
        curvav = []

        for comb in wgtsList:
            rport = rendimiento_port(var,comb) 
            vport = volatilidad_port(var, comb)

            curvar.append(rport)
            curvav.append(vport)
        
        rends.append(curvar)
        vols.append(curvav)
    
    
    graficar_3_curvas(rends, vols)
    
if __name__ == '__main__':
    f = r'Insumos\sectoresmx.csv'
    graficar_retorno_volatilidad(f)
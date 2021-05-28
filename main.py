# Crear portafolios de renta fija y renta variabled

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook as cbook

def variaciones():
    df = pd.read_csv('data.csv',header=0,index_col=0, parse_dates=['Fecha'])
    for col in df:
        df[col] = df[col]/df[col].shift(1)
    
    df.dropna(inplace=True)
    return df

def graficar_rendimiento(var):
    
    var = variaciones()
    rend = var.cumprod()
    
    
    plt.plot(rend.index, rend.values)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    var = variaciones()
    
    rf = [var['RF 0-1'].std(), var['RF 0-1'].prod()]
    rv = [var['RV'].std(), var['RV'].prod()]
    
    i = 0
    port_list = [] 
    port_max_rend = []
    max_rend = 0
    
    for _ in range(10):
    
        port = [rf[1]*i, rv[1]*(1-i),(rf[1]*i) + (rv[1]*(1-i))]
        i+=.1
        
        if port[2] > max_rend:
            port_max_rend = port
            max_rend = port[2]
        
         
        port_list.append(port)
    
    
    print(max_rend, port_max_rend)
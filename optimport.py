import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


# _______________________ lectura de datos __________________________________

def lectura_datos_csv(filepath):
    datos = pd.read_csv(filepath, header=0, index_col=0, parse_dates=[0],dayfirst=True)
    datos = np.log(datos / datos.shift(1))
    datos.dropna(inplace=True)

    return datos

# ________________________ Funciones cálculo métricas de portafilios __________________

def rendimiento_port(vars, wgts, periodicidad):

    periodicidades = {
        'anual': 1,
        'semestral': 2,
        'cuatrimestral': 3,
        'trimestral': 4,
        'bimestral': 6,
        'mensual': 12,
        'semanal': 52,
        'diaria': 252
    }

    rend = (vars.mean() ** periodicidades[periodicidad]) - 1

    rend = rend * wgts

    return rend.sum() * 100


def volatilidad_port(vars, wgts):
    covs = np.array(vars.cov() * 12)

    wgts = np.array(wgts)

    return np.sqrt(np.dot(wgts.T, np.dot(covs, wgts)))

# ____________________________ Generador de ponderaciones ________________________________


def wghts_generator_random(nports, nseries):
    all_weights = np.zeros((nports, nseries))

    for ind in range(nports):
        weights = np.array(np.random.random(nseries))
        # Rebalancear pesos
        weights = weights / np.sum(weights)
        # Almacenar Pesos
        all_weights[ind, :] = weights

    return all_weights


def generador_ponderaciones_2_activos():

    wghts_port_1 = np.linspace(0,1,11).reshape(11,1)
    wghts_port_2 = np.flip(wghts_port_1)
    all_weigts = np.concatenate((wghts_port_1,wghts_port_2),axis=1)

    return all_weigts


def wghts_generator_3_assets():
    wghts_iniciales = np.linspace(0,1,11).reshape(11,1)
    wghts_port = np.flip(wghts_iniciales)
    for i in range(11):

        upper_limit = np.around(1-(i/10),decimals=2)
        n_wghts = ((np.around(1-(i/10),decimals=2)*100)/10)+1

        wghts_asset_1 = np.linspace(0,upper_limit,int(n_wghts))
        wghts_asset_2 = wghts_asset_1[:,np.newaxis]
        wghts_asset_3 = np.full((int(n_wghts),1),i*.1)
        w = np.concatenate((wghts_port[i:int(n_wghts)+i], wghts_asset_2, wghts_asset_3), axis=1)

        if i == 0:
            wghts = w
        else:
            wghts = np.concatenate((wghts,w), axis=0)
    
    return wghts

# ___________________________________ Simulaciones _______________________________________

def generar_curva_portafolio_2_activos(datos):

    wgtslist = generador_ponderaciones_2_activos()

    rends = datos['data']['rendimiento']
    cov = datos['data']['volatilidad']

    ports_rends = []
    ports_vols = []

    for comb in wgtslist:
        rport = np.array(rends) * comb
        vport = np.sqrt(np.dot(comb.T, np.dot(cov, comb)))

        ports_rends.append(rport.sum() * 100)
        ports_vols.append(vport * 100)

    result = {
        'tipo': 'curva',
        'curva': {
            'rendimiento': ports_rends,
            'volatilidad': ports_vols
        },
        'ponderaciones': wgtslist
    }

    return result

# _________________________ Funciones de visualización de datos _____________________


def graficar_curva_2_activos(rends, vols):
    
    fig, ax = plt.subplots()
    ax.plot(vols, rends, color='blue', marker='o')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_xlabel('Volatilidad')
    ax.set_ylabel('Rendimiento')
    ax.set_title('Curva 2 activos')
    ax.grid(True)
    plt.show()
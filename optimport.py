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


def generador_ponderaciones_aleatorias(nports, nseries):
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


def generador_ponderaciones_3_activos():
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

def generar_curva_portafolio_3_activos(datos):

    wgtslist = generador_ponderaciones_3_activos()

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
        'ponderaciones': wgtslist,
        'activos': datos['data']['activos']
    }

    return result

# _________________________ Funciones de visualización de datos _____________________


def graficar_curva_2_activos(rends, vols):

    # ____ Determinación portafolio eficiente ______

    max_val=None
    min_val=None

    for i in range(0, len(rends)-1):

        if not max_val:
            max_val = rends[i]
            min_val = vols[i]
        else:
            if rends[i] >= max_val:
                if vols[i] <= min_val:
                    max_val = rends[i]
                    min_val = vols[i]
    
    fig, ax = plt.subplots()
    ax.plot(vols, rends, color='blue', marker='o')
    ax.plot(min_val,max_val, color='red', marker='o')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_xlabel('Volatilidad')
    ax.set_ylabel('Rendimiento')
    ax.set_title('Curva 2 activos')
    ax.grid(True)
    plt.show()

def graficar_curva_3_activos(curva_data):

    rends=curva_data['curva']['rendimiento']
    vols=curva_data['curva']['volatilidad']
    ponderaciones=curva_data['ponderaciones']
    activos = curva_data['activos']
    
    # ____ Determinación portafolio eficiente ______

    max_val=None
    min_val=None
    pos_index=None

    for i in range(0, len(rends)-1):

        if not max_val:
            max_val = rends[i]
            min_val = vols[i]
            pos_index = i
        else:
            if rends[i] >= max_val:
                if vols[i] <= min_val:
                    max_val = rends[i]
                    min_val = vols[i]
                    pos_index = i
            else:
                if vols[i] <= min_val:
                    max_val = rends[i]
                    min_val = vols[i]
                    pos_index = i
    
    fig, axd = plt.subplot_mosaic([['A panel','A panel','R panel','V panel'],
                                   ['A panel','A panel','B panel','B panel'],
                                   ['A panel','A panel','B panel','B panel']],
                                  layout='constrained', figsize=(9.5,6.5))
    
    #fig, ax = plt.subplots()
    axd['A panel'].scatter(vols, rends, color='blue', marker='o')
    axd['A panel'].plot(min_val,max_val, color='red', marker='o')
    axd['A panel'].yaxis.set_major_formatter(mtick.PercentFormatter())
    axd['A panel'].xaxis.set_major_formatter(mtick.PercentFormatter())
    axd['A panel'].set_xlabel('Volatilidad')
    axd['A panel'].set_ylabel('Rendimiento')
    axd['A panel'].set_title('Curva 3 activos')
    axd['A panel'].grid(True)

    axd['B panel'].set_title('Distribución de activos')
    axd['B panel'].bar(activos, ponderaciones[pos_index]*100, color='green')
    axd['B panel'].yaxis.set_major_formatter(mtick.PercentFormatter())
    axd['B panel'].grid(True)

    axd['R panel'].set_title("Rendimiento ('E)")
    axd['R panel'].tick_params(left=False, bottom=False, labelleft=False,labelbottom=False)
    axd['R panel'].annotate("{:.2%}".format(max_val/100), xy=(2,2), xytext=(2,2),xycoords='data',ha='center', va='center',
                            fontsize=30, color='darkgrey')
    axd['R panel'].set_ylim(0,4)
    axd['R panel'].set_xlim(0,4)

    axd['V panel'].set_title("Riesgo ('E)")
    axd['V panel'].tick_params(left=False, bottom=False, labelleft=False,labelbottom=False)
    axd['V panel'].annotate("{:.2%}".format(min_val/100), xy=(2,2), xytext=(2,2),xycoords='data',ha='center', va='center',
                            fontsize=30, color='darkgrey')
    axd['V panel'].set_ylim(0,4)
    axd['V panel'].set_xlim(0,4)
    plt.show()
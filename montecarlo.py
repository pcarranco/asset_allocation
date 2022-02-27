import matplotlib.pyplot as plt
import numpy as np


def wghts_generator_random(nports, nseries):
    all_weights = np.zeros((nports, nseries))

    for ind in range(nports):
        weights = np.array(np.random.random(nseries))
        # Rebalancear pesos
        weights = weights / np.sum(weights)
        # Almacenar Pesos
        all_weights[ind, :] = weights

    return all_weights


def wghts_generator_2_assets():

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

def simular_portafolios(assets, weights):
    
    rend = (np.exp(assets.sum())-1)/14
    rends = weights*np.array(rend)
    exp_rends = rends.sum(axis=1)

    exp_vol = np.zeros(weights.shape[0])

    for i in range(len(weights)):
        exp_vol[i] = np.sqrt(np.dot(weights[i],np.dot(assets.cov(),weights[i])))*np.sqrt(252)
    
    plt.figure(figsize=(12, 8))
    plt.scatter(exp_vol, exp_rends, cmap='plasma')
    plt.colorbar(label='Sharpe Ratio')
    plt.xlabel('Volatilidad')
    plt.ylabel('Rendimiento')


    plt.show()

def simulcion_wghts_portafolios(log_ret, nports):
    # Almacenar datos de simulación
    exp_ret = np.zeros(nports)
    exp_vol = np.zeros(nports)
    sr = np.zeros(nports)

    all_weights = wghts_generator_random(nports, len(list(log_ret.columns)))

    for ind in range(len(all_weights)):
        # Rendimiento esperado
        exp_ret[ind] = np.sum((log_ret.mean() * all_weights[ind]) * 12)

        # Volatilidad esperada
        exp_vol[ind] = np.sqrt(np.dot(all_weights[ind].T, np.dot(log_ret.cov() * 12, all_weights[ind])))

        # Sharpe Ratio

        sr[ind] = exp_ret[ind] / exp_vol[ind]

    # Mejor portafolio de acuerdo al Sharpe Ratio
    max_sr_ret = exp_ret[sr.argmax()]
    max_sr_vol = exp_vol[sr.argmax()]

    plt.figure(figsize=(12, 8))
    plt.scatter(exp_vol, exp_ret, c=sr, cmap='plasma')
    plt.colorbar(label='Sharpe Ratio')
    plt.xlabel('Volatilidad')
    plt.ylabel('Rendimiento')

    plt.scatter(max_sr_vol, max_sr_ret, c='red', s=50, edgecolors='black')

    plt.show()

if __name__ == '__main__':
    from main import variaciones_csv
    f = r'.\Insumos\rv.csv'
    a = variaciones_csv(f)
    w = wghts_generator_3_assets()
    simular_portafolios(a,w)
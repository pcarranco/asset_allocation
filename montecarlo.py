import matplotlib.pyplot as plt
import numpy as np


def wghts_gen(nports, nseries):
    all_weights = np.zeros((nports, nseries))

    for ind in range(nports):
        weights = np.array(np.random.random(nseries))
        # Rebalancear pesos
        weights = weights / np.sum(weights)
        # Almacenar Pesos
        all_weights[ind, :] = weights

    return all_weights


def wghts_gen_2ports(nports):
    all_weigts = np.zeros((nports, 2))
    n = 0
    salto = 1 / nports

    for ind in range(nports):
        weights = [round(1 - n, 2), round(n, 2)]
        all_weigts[ind, :] = np.array(weights)
        n += salto

    print(all_weigts)


def simulcion_wghts_portafolios(log_ret, nports):
    # Almacenar datos de simulación
    exp_ret = np.zeros(nports)
    exp_vol = np.zeros(nports)
    sr = np.zeros(nports)

    all_weights = wghts_gen(nports, len(list(log_ret.columns)))

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
    wghts_gen_2ports(3)

"""Prueba de Grubbs"""
import pandas as pd
import matplotlib.pyplot as plt
from outliers import smirnov_grubbs as grubbs
import numpy as np


COLUMNS = ['X', 'Y']
DF = pd.read_csv("./data.csv", names=COLUMNS)
DF_X = DF['X']
DF_Y = DF['Y']
MEAN_X = np.mean(DF_X.to_numpy())
STD_X = np.std(DF_X.to_numpy())


print("El valor esperado de las coordenadas en X es: ", MEAN_X)
print("La desviación estándar  de las coordenadas en X es: ", STD_X)

P = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1]
T_MIN = []
T_MAX = []

for i in range(0, 6):
    print("P-Value: ", P[i])
    for j in range(0, 5000):
        DF = pd.read_csv("./data.csv", names=COLUMNS)
        new_value_min = MEAN_X-j
        new_value_max = MEAN_X+j
        new_data_min = pd.DataFrame({'X':[new_value_min], 'Y':[0]})
        new_data_max = pd.DataFrame({'X':[new_value_max], 'Y':[0]})
        DF_min = DF.append(new_data_min, ignore_index=True)
        DF_max = DF.append(new_data_max, ignore_index=True)
        x_min = DF_min['X']
        x_max = DF_max['X']
        data_y = DF_min['Y']
        data_x_min = x_min.to_numpy()
        data_x_max = x_max.to_numpy()
        print("Experimento #", j)
        #Realizar la prueba de Grubbs para ver si el valor mínimo es una anomalía
        print("Resultado Prueba Grubbs:")
        anomalia_min = grubbs.min_test_indices(data_x_min, alpha=P[i])
        anomalia_max = grubbs.max_test_indices(data_x_max, alpha=P[i])
        if not anomalia_min:
            print("No hay anomalía mínima en conjunto")
        else:
            T_MIN.append(data_x_min[anomalia_min[0]])
            print('El valor: "', data_x_min[anomalia_min[0]],
                  '" con una p-value de :"', P[i], 'es una anomalía')
            plt.scatter(data_x_min, data_y)
            plt.show()
            anomalia_min = []
        if not anomalia_max:
            print("No hay anomalía máxima en conjunto")
        else:
            T_MAX.append(data_x_max[anomalia_max[0]])
            print('El valor: "', data_x_max[anomalia_max[0]],
                  '" con una p-value de :"', P[i], 'es una anomalía')
            plt.scatter(data_x_max, data_y)
            plt.show()
            break

def graficar_anomalias(titulo, res_anomalias, p_y):
    """Graficar Resultados"""
    plt.title(titulo)
    plt.xlabel("P")
    plt.ylabel("T")
    plt.plot(res_anomalias, p_y)
    plt.show()
graficar_anomalias("Anomalías Máximas", P, T_MAX)
graficar_anomalias("Anomalías Mínimas", P, T_MIN)

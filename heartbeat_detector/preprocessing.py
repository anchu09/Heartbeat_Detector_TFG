#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 16:27:37 2022

@author: dani
"""

import glob
import os

import numpy as np
import pandas as pd

os.chdir(os.getcwd()[:-len("heartbeat_detector")])

path = 'semi_preprocessed_signals/original_ecg'

files = glob.glob(path + "/*.csv")

diccionarioDatos = {}

for filename in files:
    diccionarioDatos[filename[(len(path) + 1):len(filename) - 4]] = pd.read_csv(filename, index_col=None,
                                                                                on_bad_lines='skip', delimiter="\t",
                                                                                header=None)

path = 'semi_preprocessed_signals/original_annotations'

files = glob.glob(path + "/*.csv")
diccionarioAnotaciones = {}

for filename in files:
    data = []
    with open(filename) as file:
        for line in file:
            try:
                line_data = line.strip().split()
                data.append(line_data)
            except:
                continue
    diccionarioAnotaciones[filename[(len(path) + 1):len(filename) - 4]] = pd.DataFrame(data)


def fillzeros():
    for key in diccionarioAnotaciones.keys():
        f = open("./semi_preprocessed_signals/annotations_padding/" + key + ".csv", "w")
        limite_inferior = 0
        print(key)

        for index, fila in diccionarioAnotaciones[key].iterrows():

            limite_superior = int(fila[1])
            for i in np.arange(limite_inferior, limite_superior):
                t = i / 360
                t = np.round(t, 4)

                new_row = np.array([t, i, "Z", "0", "0", "0"])
                for valor in new_row:
                    f.write(str(valor) + " ")
                f.write("\n")
            f.write(str(int(fila[1]) / 360) + " ")
            for valor in fila[1:-1]:
                f.write(str(valor) + " ")
            f.write("\n")
            limite_inferior = int(fila[1]) + 1

        for k in np.arange(limite_superior + 1, 650000):
            t = k / 360
            t = np.round(t, 4)
            new_row = np.array([t, k, "Z", "0", "0", "0"])
            for valor in new_row:
                f.write(str(valor) + " ")
            f.write("\n")

        f.close()


def window():
    path = 'semi_preprocessed_signals/annotations_padding'

    files = glob.glob(path + "/*.csv")

    for filename in files:
        data = []
        with open(filename) as file:
            for line in file:
                try:
                    line_data = line.strip().split()
                    data.append(line_data)
                except:
                    continue
        diccionarioAnotacionesCeros[filename[(len(path) + 1):len(filename) - 4]] = pd.DataFrame(data)
        window_separado(0.15)
        diccionarioAnotacionesCeros.pop(filename[(len(path) + 1):len(filename) - 4])


def normalizarX():
        from sklearn.preprocessing import MinMaxScaler

        scaler = MinMaxScaler(feature_range=(-1, 1))
        for key in diccionarioDatos.keys():
            print(key)
            canal1 = diccionarioDatos[key][1]
            canal1_normalizado = scaler.fit_transform(canal1.values.reshape(-1, 1))
            diccionarioDatos[key][1] = canal1_normalizado

            canal2 = diccionarioDatos[key][2]
            canal2_normalizado = scaler.fit_transform(canal2.values.reshape(-1, 1))
            diccionarioDatos[key][2] = canal2_normalizado

            print(len(diccionarioDatos[key]))
            diccionarioDatos[key].iloc[:, 1:3].to_csv(
                "./semi_preprocessed_signals/normalized_ecg/" + key + ".csv", index=False, header=False, sep=' ')


diccionarioAnotacionesCeros = {}


def window_separado(bandwidth):
    muestras = bandwidth * 360
    muestras = round(muestras)
    for key in diccionarioAnotacionesCeros.keys():
        print(key)

        # ya tenemos el vector de las filas que hay que copiar
        listaMuestras = diccionarioAnotaciones[key].iloc[:, 1].values.astype(int)
        for valor in listaMuestras:
            if valor == 0:
                valor = 1
            fila_a_copiar = diccionarioAnotacionesCeros[key].loc[valor, diccionarioAnotacionesCeros[key].columns[2:]]
            if valor - muestras < 0:
                valor_menos_muestras = 0
            else:
                valor_menos_muestras = valor - muestras

            if valor + muestras > 650000:
                valor_mas_muestras = 650000

            else:
                valor_mas_muestras = valor + muestras

            for muestraVentana in np.arange(valor_menos_muestras, valor_mas_muestras):
                diccionarioAnotacionesCeros[key].loc[
                    muestraVentana, diccionarioAnotacionesCeros[key].columns[2:]] = fila_a_copiar

        diccionarioAnotacionesCeros[key].iloc[:, :].to_csv("./semi_preprocessed_signals/annotations_padding_and_window/" + key + ".csv", index=False,
                                                           header=False, sep=' ')

# fillzeros()
#
window()

# normalizarX()

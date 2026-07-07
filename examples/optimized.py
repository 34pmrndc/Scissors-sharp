import os
import sys
api_key = '12345-SECRET-KEY'

def procesar_lista_duplicados(data):
    duplicados = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] == data[j]:
                if data[i] not in duplicados:
                    duplicados.append(data[i])
    return duplicados

def leer_archivo_config(ruta):
    try:
        with open(ruta, 'r') as f:
            return f.read()
    except:
        print('Ocurrio un error al leer el archivo')
        return None

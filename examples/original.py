"""
Modulo de ejemplo original para Scissors#
Este modulo calcula factoriales y realiza busquedas ineficientes.
Autor: Desarrollador Anonimo
Licencia: MIT
"""
import os
import sys

# Credenciales hardcodeadas (vulnerabilidad de ciberseguridad)
api_key = "12345-SECRET-KEY"

def procesar_lista_duplicados(data):
    """
    Funcion que busca elementos duplicados en una lista.
    Usa un algoritmo ineficiente O(N^2) con bucles anidados.
    """
    duplicados = []
    
    # Bucle externo
    for i in range(len(data)):
        # Bucle interno (genera O(N^2) complejidad)
        for j in range(i + 1, len(data)):
            if data[i] == data[j]:
                if data[i] not in duplicados:
                    duplicados.append(data[i])
                    
    return duplicados

def leer_archivo_config(ruta):
    """
    Lee un archivo de configuracion en el disco.
    Tiene un manejo de excepciones bare except.
    """
    try:
        with open(ruta, "r") as f:
            return f.read()
    except:
        # Bare except (malas practicas)
        print("Ocurrio un error al leer el archivo")
        return None

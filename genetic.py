import random
import datetime
import sys

# Representación del polinomio
# [a,b,c,d,e,f,g] -> ax^6 + bx^5 + cx^4 + dx^3 + ex^2 + fx + g

# Funcion generadora de coeficientes aleatorios
def generar_padre(grado):
    pass

# Funcion para determinar que tan buenos son los coeficientes
def obtener_fitness(coeficientes):
    pass

# Funcion para mutar al padre y generar nuevo hijo
def mutar(padre):
    pass

# Funcion para mostrar los coeficientes para monitorizar
def mostrar(coeficientes):
    pass

# Funcion para leer el archivo con los datos (.csv)
def leerArchivo():
    if len(sys.argv) <= 1:
        print("Debe ingresar un archivo")
        exit(1)
    return []

# Funcion principal
def main():
    targetData = leerArchivo()

main()

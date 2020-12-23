import random
import datetime
import time
import sys
import os
from matplotlib import pyplot as plt

# Representación del polinomio
# [a,b,c,d,e,f,g] -> ax^6 + bx^5 + cx^4 + dx^3 + ex^2 + fx + g

# Funcion generadora de coeficientes aleatorios
def generar_padre(grado, minVal, maxVal):
    nuevoPadre = [0,0,0,0,0,0,0]
    indice = len(nuevoPadre) - 1
    for i in range(gradoMax + 1):
        num = random.randint(minVal,maxVal)
        nuevoPadre[indice] = num
        if i == grado:
            break
        indice -= 1
    return nuevoPadre

# Funcion para mutar al padre y generar nuevo hijo
def mutar(padreOriginal):

    padre = padreOriginal[:]
    indice = random.randint(0, 6)
    if mejorFitness >= 0.9:
        proporcionCambio = random.uniform(0,2.0)
    elif mejorFitness < 0.9 and mejorFitness >= 0.6:
        proporcionCambio = random.uniform(0,4.0)
    else:
        proporcionCambio = random.uniform(0,8.0)

    incremento = random.choice([True, False]) 

    if padre[indice] == 0:
        padre[indice] = random.randint(-10,10)
        return padre

    if incremento:
        padre[indice] += padre[indice] * proporcionCambio
    else:
        padre[indice] -= padre[indice] * proporcionCambio
    return padre


# Funcion para leer el archivo con los datos (.csv)
# Retorna una lista de tuplas de la forma [(x, y),...]
def leerArchivo():
    if len(sys.argv) <= 1:
        print("Debe ingresar un archivo .csv como entrada")
        exit(1)
    datos = []
    archivo = open(sys.argv[1], "r")
    lineas = archivo.readlines()
    for linea in lineas:
        splitLinea = linea.split(',')
        itemTuple = (float(splitLinea[0].strip()), float(splitLinea[1].strip()))
        datos.extend([itemTuple])
    return datos

# Toma los coeficientes actuales y genera una lista de nuevos valores 'y'
# Retorna una lista de enteros que corresponde a la evaluación de cada valor de x
# de entrada en el polinomio actual
def evaluarPolinomio(coeficientes):
    newYData = []
    for t in targetData:
        newY = 0
        exp = 6
        for c in coeficientes:
            newY += c * (t[0]**exp)
            exp -= 1
        newYData.extend([ newY ])
    return newYData

# Obtener promedio dada una lista de tuplas
def obtenerPromedioY(datos):
    suma = 0
    for t in datos:
        suma += t[1]
    return suma / len(datos)

# Funcion para determinar que tan buenos son los coeficientes
# Se utiliza el coeficiante de determinación (R cuadrado)
def obtener_fitness(coeficientes):
    datosYActuales = evaluarPolinomio(coeficientes) 
    denominador = 0
    numerador = 0
    
    for indice in range(len(targetData)):
        numerador += (targetData[indice][1] - datosYActuales[indice])**2
        denominador += (targetData[indice][1] - promedioY)**2

    res = 1 - (numerador / denominador)
    # if res > 1:
        # return 1
    return res

# Funcion para mostrar los coeficientes para monitorizar
def mostrar(coeficientes):
    timeDiff = datetime.datetime.now() - startTime
    fitness = obtener_fitness(coeficientes)
    
    exp = 6
    polinomio = ""
    for i in range(len(coeficientes)):
        if exp != 0:
            if coeficientes[i] != 0:
                if coeficientes[i] > 0:
                    polinomio += "+ {0} x^{1} ".format(round(coeficientes[i],3), exp)
                else: 
                    polinomio += "{0} x^{1} ".format(round(coeficientes[i],3), exp)
        else:
            if coeficientes[i] != 0:
                if coeficientes[i] > 0:
                    polinomio += "+ {0} ".format(round(coeficientes[i],3))
                else: 
                    polinomio += "{0} ".format(round(coeficientes[i],3))
        exp -= 1

    print("{0}\t \nFitness: {1}\t{2}".format(polinomio, fitness, str(timeDiff)))

def generarPoblacionInicial(grado):
    p = []
    gradoAux = 0
    for i in range(poblacionMax):
        # gradoAleatorio = random.randint(0, gradoMax)
        p.append(generar_padre(gradoAux, minRangeVal, maxRangeVal))
        gradoAux = (gradoAux + 1) % 7
    return p

def fitnessCriteria(e):
    return obtener_fitness(e)

def imprimirPoblacion(datos):
    print("------------------------")
    for p in datos:
        print("{0}\t\t fitness: {1}".format(p, obtener_fitness(p)))
    print("------------------------")

def getPromedio(num1, num2):
    return (num1 + num2) / 2

def getExtremos(datos, indice):
    menor = datos[0][indice]
    mayor = datos[0][indice]
    for dato in datos:
        if dato[indice] < menor:
            menor = dato[indice]
        if dato[indice] > mayor:
            mayor = dato[indice]
    return (menor, mayor)

def plotData(originalXY, mejoresCoeficientes):
    calculatedY = evaluarPolinomio(mejoresCoeficientes)
    xData = []
    yData = []
    for par in originalXY:
        xData.append(par[0])
        yData.append(par[1])
    plt.clf()
    plt.plot(xData, yData)
    plt.plot(xData, calculatedY, 'r')
    plt.pause(0.1)
    # plt.show()

def obtenerGrado(datos):
    mejorActual = datos[0]
    gradoActual = 0
    indice = -1
    while gradoActual < len(mejorActual):
        if(mejorActual[indice] == 0):
            return (gradoActual, indice)
        indice -= 1
        gradoActual += 1
    return  (gradoActual - 1, 0)

def revisarSiAumentarGrado(datos):
    mejorActual = round(obtener_fitness(datos[0]), 2)
    peorActual = round(obtener_fitness(datos[len(datos) - 1]), 2)
    if mejorActual == peorActual:
        return True
    return False


# Datos iniciales
plt.ion()
random.seed()
targetData = leerArchivo()                  # Datos XY dados por el profe
promedioY = obtenerPromedioY(targetData)    # promedio para sacar el coeficiente de determinación
startTime = datetime.datetime.now()
gradoMax = 6
mejorFitness = 0
poblacion = []
poblacionMax = 200 # 52
minRangeVal = -100
maxRangeVal = 100

# Funcion principal
def main():
    generacion = 1
    startTime = datetime.datetime.now()

    # 1. Generar la poblacion inicial
    poblacion = generarPoblacionInicial(1)

    # Ordenar poblacion de mayor a menor fitness
    poblacion.sort(key=fitnessCriteria,reverse=True)

    # 2. Repetidamente:
    #   2.1 Seleccionar padres para crossover
    #   2.2 Generar decendencia
    #   2.3 Mutar algunos padres
    #   2.4 Mezclar la decendencia y los mutantes en la poblacion
    #   2.5 Recortar la poblacion para mantener un tamano fijo

    while True:
        time.sleep(1)

        # print("Poblacion inicial")
        # imprimirPoblacion(poblacion)

        # 2.1 seleccionar la mitad mejor (primera mitad como ya estan ordenados)
        mejoresPadres = poblacion[:int( poblacionMax/2 )]
        # print("Mejores padres")
        # imprimirPoblacion(mejoresPadres)

        # 2.2 generar decendencia con crossover
        decendencia = []
        for indicePadre in range(len(mejoresPadres)):
            if indicePadre == len(mejoresPadres) - 1:
                nuevoHijo = []
                for indiceCoef in range(len(mejoresPadres[indicePadre])):
                    nuevoHijo.append(getPromedio(mejoresPadres[indicePadre][indiceCoef], mejoresPadres[0][indiceCoef]))
            else:
                nuevoHijo = []
                for indiceCoef in range(len(mejoresPadres[indicePadre])):
                    nuevoHijo.append(getPromedio(mejoresPadres[indicePadre][indiceCoef], mejoresPadres[indicePadre + 1][indiceCoef]))
            decendencia.append(nuevoHijo)

        # print("Decendencia")
        # imprimirPoblacion(decendencia)

        # 2.3 mutar la mitad de los padres

        # se obtiene los rangos max y min de cada coeficiente
        mutantesRangos = []
        for i in range(len(poblacion[0])):
            mutantesRangos.append(getExtremos(poblacion,i))

        # print("Extremos")        
        # print(mutantesRangos)

        mutantes = []
        factor = 12 # 12
        for k in range(int(poblacionMax/2)):
            nuevoHijo = []
            numAleatorio = random.randint(0, len(poblacion)-1)
            for c in poblacion[numAleatorio]:
                nuevoC = random.uniform(c - c*factor, c + c*factor)
                nuevoHijo.append(nuevoC)
            # for rango in mutantesRangos:
                # mitad = getPromedio(rango[0], rango[1])
                # # nuevoHijo.append(random.uniform(rango[0]*factor, rango[1]*factor))
                # nuevoHijo.append(random.uniform(-mitad*factor, mitad*factor))
            mutantes.append(nuevoHijo)
        
            
        # print("mutantes")
        # imprimirPoblacion(mutantes)

        # 2.4 mezclar los mutantes y la decendencia
        poblacion.extend(decendencia)
        poblacion.extend(mutantes)

        # print("Mezclados")
        # imprimirPoblacion(poblacion)

        # 2.5 recortar la poblacion
        poblacion.sort(key=fitnessCriteria,reverse=True)
        poblacion = poblacion[:poblacionMax]

        # print("recortar")
        # imprimirPoblacion(poblacion)

        timeDiff = datetime.datetime.now() - startTime
        print("------------------------")
        print("Mejores 5")
        imprimirPoblacion(poblacion[:5])
        # imprimirPoblacion(poblacion)
        print("\n{0}\n".format(timeDiff))
        print("Generacion: {0}".format(generacion))
        generacion += 1

        # 2.6 revisar si aumento grado
        # if revisarSiAumentarGrado(poblacion):
        #     # ingresar 25 de un grado mayor a poblacion
        #     (gradoActual, indiceActual) = obtenerGrado(poblacion)
        #     factorScale = 2
        #     if gradoActual <= gradoMax:
        #         print("------Aumentando Grado------")
        #         print("Mejor: {0}".format(poblacion[0]))
        #         if indiceActual <= -2:
        #             rangeVal = poblacion[0][indiceActual + 1]
        #         else:
        #             rangeVal = poblacion[0][indiceActual]

        #         for i in range(25):
        #             nuevoValor = random.uniform(-rangeVal * factorScale, rangeVal * factorScale)
        #             nuevoCoef = poblacion[0][:]
        #             nuevoCoef[indiceActual] = nuevoValor
        #             print("Nuevo: {0}, Val: {1}".format(nuevoCoef, rangeVal))
        #             poblacion.append(nuevoCoef)


        # 2.6 determinar si ya llegamos al fitness objetivo
        mejorFitness = obtener_fitness(poblacion[0])
        plotData(targetData, poblacion[0])
        if mejorFitness >= 0.97:
            print("-----------------------------------------------------")
            mostrar(poblacion[1])
            print("-----------------------------------------------------")
            input("Presione una tecla para continuar...")
            break


main()

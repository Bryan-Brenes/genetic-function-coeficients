import random
import datetime
import time
import sys

# Representación del polinomio
# [a,b,c,d,e,f,g] -> ax^6 + bx^5 + cx^4 + dx^3 + ex^2 + fx + g

# Funcion generadora de coeficientes aleatorios
def generar_padre(grado):
    nuevoPadre = [0,0,0,0,0,0,0]
    indice = len(nuevoPadre) - 1
    for i in range(gradoMax + 1):
        num = random.randint(-10,10)
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
        itemTuple = (float(splitLinea[0]), float(splitLinea[1].strip()))
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
                    polinomio += "+ {0} x^{1} ".format(coeficientes[i], exp)
                else: 
                    polinomio += "{0} x^{1} ".format(coeficientes[i], exp)
        else:
            if coeficientes[i] != 0:
                if coeficientes[i] > 0:
                    polinomio += "+ {0} ".format(coeficientes[i])
                else: 
                    polinomio += "{0} ".format(coeficientes[i])
        exp -= 1

    print("{0}\t{1}\t{2}".format(polinomio, fitness, str(timeDiff)))


# Datos iniciales
random.seed()
targetData = leerArchivo()                  # Datos XY dados por el profe
promedioY = obtenerPromedioY(targetData)    # promedio para sacar el coeficiente de determinación
startTime = datetime.datetime.now()
gradoMax = 6
mejorFitness = 0

# time.sleep(1)

# Funcion principal
def main():
    coeficientes = generar_padre(0)
    mejorFitness = obtener_fitness(coeficientes)
    while True:
        time.sleep(0.2)
        hijo = mutar(coeficientes)
        fitnessHijo = obtener_fitness(hijo)
        mostrar(hijo)
        print("Fitness actual: {0}, Fitness mejor: {1}".format(fitnessHijo,mejorFitness))
        print(hijo)
        if mejorFitness >= fitnessHijo:
            print("Continuando...\n")
            continue
        if fitnessHijo >= 0.96:
            break
        mejorFitness = fitnessHijo
        coeficientes = hijo
        print()
                                                    

main()

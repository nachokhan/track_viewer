"""
Problema problem¡atico:

Descripción.

Tenemos un arreglo de puntos en el espacio (bidimensaional) de coordenadas (x,y).
Esas coordenadas representan puntos consecutivos, o sea, puntos de una ruta.
La idea es el que tenga huevos de armar una función en python llamada "contar_curvas"
que reciva como parámetros:

    - Arreglo con los putos x,y
    - Un angulo mínimo que indica que una curva es una curva.

Y que devuelva la cantidad de curvas que se hacen en el trayecto, la intesidad de las mismas, 
y las posiciones (puntos x,y) donde comienza cada una.

Si por ejemplo, hay un desvio del trayecto de 5 grados, es muy bajo el cambio de direccion
para calificarlo como curva. Pero si es de 80, ya estamos hablando de un lindo volantazo.

Entonces, definir la funcion:

def contar_curvas(puntos, min_angulo):
    # TODO

"""

from math import atan, degrees, atan2, pi, ceil, sqrt

def contar_curvas(puntos, min_angulo):
    
    curvas = 0
    intensidad = []
    puntos_c = []

    cont = len(puntos) - 2

    for i in range(0,cont):
        p1 = puntos[i]
        p2 = puntos[i+1]
        p3 = puntos[i+2]

        b1 = bearing(p1, p2)
        b2 = bearing(p2, p3)
       
        diff = abs(abs(b2) - abs(b1))

        if diff >= min_angulo:
            curvas += 1
            intensidad.append(diff)
            puntos_c.append(i+1)

        
    return curvas, intensidad, puntos_c

def bearing(p1, p2):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    dx = x2-x1
    dy = y2-y1

    if dx == 0:
        if dy < 0:
            return 180
        else:
            return 0

    tan = dy/dx
    
    ang = degrees(atan(tan))

    if dx < 0:
        pepe = -90
    else:
        pepe = 90

    return round (pepe-ang, 2)


puntos_1 = [
    (1,1),
    (2,4),
    (2,7),
    (4,8),
    (5,11),
    (8,11),
    (13,10),
    (14,8),
    (14,5),
    (16,5),
    (18,5),
    (19,7),
    (21,13)
]

puntos_2 = [
    (1,-1),
    (2,-4),
    (2,-7),
    (4,-8),
    (5,-11),
    (8,-11),
    (13,-10),
    (14,-8),
    (14,-5),
    (16,-5),
    (18,-5),
    (19,-7),
    (21,-13)
]

puntos_3 = [
    (-1,-1),
    (-2,-4),
    (-2,-7),
    (-4,-8),
    (-5,-11),
    (-8,-11),
    (-13,-10),
    (-14,-8),
    (-14,-5),
    (-16,-5),
    (-18,-5),
    (-19,-7),
    (-21,-13)
]

puntos_4 = [
    (-1,1),
    (-2,4),
    (-2,7),
    (-4,8),
    (-5,11),
    (-8,11),
    (-13,10),
    (-14,8),
    (-14,5),
    (-16,5),
    (-18,5),
    (-19,7),
    (-21,13)
]


#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy as np

"""
 Cada linea de simulación es una llamada
 La unidad de tiempo es el minuto (tomado como entero)
"""

class OcupadoException(Exception):
    pass

class IOperador:
    tipo = None
    def getTipo():
        raise NotImplementedError
    
    def ocupar(self, tiempo, duracion):
        try:
            if self.is_ocupado(tiempo):
                print("Ocupado!")
                raise OcupadoException
        except IndexError:
            print("Tiempo: %i (error)"%tiempo)
            exit("Error. End of simulation")
        try:
            for i in range(tiempo, tiempo+duracion):
                if self.tiempo[i]==1:
                    raise OcupadoException
                self.tiempo[i] = 1
        except IndexError:
            for i in range( tiempo,len(self.tiempo) ):
                self.tiempo[i] = 1


    def is_ocupado(self, i):
        if self.tiempo[i]==1:
            return True
        else:
            return False

    def getTiempoOcioso(self, tiempo_max):
        tiempo_ocupado = np.count_nonzero( self.tiempo[:tiempo_max] == 1) #
        return (tiempo_max-tiempo_ocupado)
#

class Operador(IOperador):
    def __init__(self, n, M):
        # self.tipo = "Operador"
        self.tiempo = np.ones(n+M)*-1

def genNumero():
    """ Genera un número aleatorio entre 0 y 100 """
    #rn = int(random.random()*100.)
    return int( np.round( random.uniform(0,100) ) )

def getDuracionLlamada(rn):
    """
        número random en [0,1]
        y luego discrimina por F(x), la acumulada
        rn: random number [0,1]
    """
    if rn<20:
        return 2
    elif rn<60:
        return 5
    elif rn<80:
        return 9
    elif rn<95:
        return 13
    else:
        return 15
#()

def getEspacioEntreLlamadas(rn):
    """
        número random en [0,1]
        y luego discrimina por F(x), la acumulada
        rn: random number [0,1]
    """
    if rn<40:
        return 1
    elif rn<60:
        return 2
    elif rn<80:
        return 3
    else:
        return 4
#()

def getTipoLlamada(rn):
    """
        Recibe número random en [0,1]
        y luego discrimina por F(x), la acumulada
        rn: random number [0,1]
    """
    if rn<40:
        return "consulta"
    elif rn<70:
        return "turno"
    elif rn<90:
        return "garantia"
    else:
        return "uso"
#()

def convert_tipo_to_num(tipo):
    if tipo=="consulta":
        return 0
    elif tipo=="turno":
        return 1
    elif tipo=="garantia":
        return 2
    elif tipo=="uso":
        return 3
    else:
        raise Error
#()

def convert_tipo_to_txt(num):
    if num==0:
        return "consulta"
    elif num==1:
        return "turno"
    elif num==2:
        return "garantia"
    elif num==3:
        return "uso"
    else:
        raise Error
#()
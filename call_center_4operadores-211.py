#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Simulación para un callcenter con 4 operadores
    * 2 junior
    * 1 semi-senior
    * 1 senior
"""

from CallCenterModel import *

n = 400 #cant de casos (de llamadas)

# Vectores por cada columna que luego se transforma al .csv (modo planilla)
num_aleat_1 = np.ones(n)*-1
duracion = np.ones(n)*-1

num_aleat_2 = np.ones(n)*-1
distancia_entre_llamadas = np.ones(n)*-1

num_aleat_3 = np.ones(n)*-1
tipo_llamada = np.ones(n)*-1 #codificado con 1..4

M = 1000 # más lugar para poder manejar los lugares de ocupado/libre correctamente
op1_tiempo_inicio = np.ones(n+M)*-1
op1_tiempo_fin = np.ones(n+M)*-1

op2_tiempo_inicio = np.ones(n+M)*-1
op2_tiempo_fin = np.ones(n+M)*-1

op3_tiempo_inicio = np.ones(n+M)*-1
op3_tiempo_fin = np.ones(n+M)*-1

op4_tiempo_inicio = np.ones(n+M)*-1
op4_tiempo_fin = np.ones(n+M)*-1

llamada = np.ones(n)*-1
llegada = np.ones(n)*-1

no_atendido = np.ones(n)*-1

# Simulación
tiempo = 0 # tiempo en el que entra una llamada
op1 = Operador(n, M) #junior
op2 = Operador(n, M) #junior
op3 = Operador(n, M) #semi-senior
op4 = Operador(n, M) #senior
for i in range(n):
    rn_1 = genNumero()
    dur = getDuracionLlamada( rn_1 )

    rn_2 = genNumero()
    tipo = getTipoLlamada( rn_2 )

    dist_entre_llamadas = 0
    if i==0:
        rn_3 = -1
    else:
        rn_3 = genNumero()
        dist_entre_llamadas = getEspacioEntreLlamadas( rn_3 )

    tiempo = int( tiempo + dist_entre_llamadas )
    llegada[i] = tiempo

    print( "Llamado: %i, Tiempo: %i, Duración: %i, Tipo: %s"%(i,tiempo, dur,tipo) )
    
    num_aleat_1[i] = rn_1
    num_aleat_2[i] = rn_2
    num_aleat_3[i] = rn_3
    duracion[i] = dur
    distancia_entre_llamadas[i] = dist_entre_llamadas
    tipo_llamada[i] = convert_tipo_to_num(tipo)

    if tipo=="consulta" or tipo=="turno":
        try: #junior
            op1.ocupar(tiempo, dur)
            op1_tiempo_inicio[i] = int( tiempo )
            op1_tiempo_fin[i] = int( tiempo + dur )
        except OcupadoException:
            try:
                op2.ocupar(tiempo, dur)
                op2_tiempo_inicio[i] = tiempo 
                op2_tiempo_fin[i] = int( tiempo + dur )
            except OcupadoException:
                no_atendido[i] = 1 
    elif tipo=="uso": #semi-senior
        try:
            op3.ocupar(tiempo, dur)
            op3_tiempo_inicio[i] = tiempo 
            op3_tiempo_fin[i] = int( tiempo + dur )
        except OcupadoException:
            no_atendido[i] = 1 
    elif tipo=="garantia": #senior
        try:
            op4.ocupar(tiempo, dur)
            op4_tiempo_inicio[i] = tiempo 
            op4_tiempo_fin[i] = int( tiempo + dur )
        except OcupadoException:
            no_atendido[i] = 1 

# Generación de los archivos .csv
filename = "output-4operadores-2junior.csv"
with open(filename, 'w') as out:
    out.write( "Llamada, Nº Aleat 1, Duracion, Nº Aleat 2, Tipo de Llamada, Nº Aleat 3, Distancia, Llegada,")
    out.write( "Op1 Inicio, Op1 Fin, Op2 Inicio, Op2 Fin, Op3 Inicio, Op3 Fin, Op4 Inicio, Op4 Fin, No Atendido\n")
    for i in range(n):
        out.write("%i,"%(i+1)) # número de llamadas
        out.write( "%i,%i,%i,"%(
            num_aleat_1[i],
            duracion[i],
            num_aleat_2[i]
            ))
        out.write( convert_tipo_to_txt(tipo_llamada[i])+',' )
        out.write( "%i,%i,%i,"%(
            num_aleat_3[i],
            distancia_entre_llamadas[i],
            llegada[i]
            ))
        if( op1_tiempo_inicio[i]!=-1 ):
            out.write( "%i,"%op1_tiempo_inicio[i] )
        else:
            out.write(',')
        if( op1_tiempo_fin[i]!=-1 ):
            out.write( "%i,"%op1_tiempo_fin[i] )
        else:
            out.write(',')
        if( op2_tiempo_inicio[i]!=-1 ):
            out.write( "%i,"%op2_tiempo_inicio[i] )
        else:
            out.write(',')
        if( op2_tiempo_fin[i]!=-1 ):
            out.write( "%i,"%op2_tiempo_fin[i] )
        else:
            out.write(',')
        if( op3_tiempo_inicio[i]!=-1 ):
            out.write( "%i,"%op3_tiempo_inicio[i] )
        else:
            out.write(',')
        if( op3_tiempo_fin[i]!=-1 ):
            out.write( "%i,"%op3_tiempo_fin[i] )
        else:
            out.write(',')
        if( op4_tiempo_inicio[i]!=-1 ):
            out.write( "%i,"%op4_tiempo_inicio[i] )
        else:
            out.write(',')
        if( op4_tiempo_fin[i]!=-1 ):
            out.write( "%i,"%op4_tiempo_fin[i] )
        else:
            out.write(',')
        if( no_atendido[i]!=-1 ):
            out.write( "%i"%no_atendido[i] )
        out.write('\n')

print("=== Reporte ===")
print("2 junior, 1 semi-senior, 1 senior")
print("Cantidad de no atendidos: %i"%np.count_nonzero(no_atendido == 1))
tiempo_max = int( np.max( np.array([np.max(op1_tiempo_fin),np.max(op2_tiempo_fin),np.max(op3_tiempo_fin),np.max(op4_tiempo_fin)]) ) )
print("Tiempo máximo de simulación: %i"%tiempo_max)
print("Tiempo ocioso Op1 (junior): %i minutos"%op1.getTiempoOcioso(tiempo_max) )
print("Tiempo ocioso Op2 (junior): %i minutos"%op2.getTiempoOcioso(tiempo_max) )
print("Tiempo ocioso Op3 (semi-senior): %i minutos"%op3.getTiempoOcioso(tiempo_max) )
print("Tiempo ocioso Op4 (senior): %i minutos"%op4.getTiempoOcioso(tiempo_max) )

#TODO: sumar horas de descanso ocupando el tiempo de los operadores con la función ocupar (por ej escalados cada 30minutos, la unidad de tiempo)

# Hacer varias simulaciones y tomar promedio y desvio (average y std-dev en planilla) media + desvio (error)
with open("simulaciones-4op.csv", 'w') as out:
    out.write("No atendidos, T.Ocioso Op1 (junior), T.Ocioso Op2 (junior), T.Ocioso Op3 (SemiSenior), T.Ocioso Op4 (senior)\n")
# with open("simulaciones-4op.csv", 'a') as out:
    out.write("%i,%i,%i,%i,%i\n"%(
       np.count_nonzero(no_atendido == 1),
       op1.getTiempoOcioso(tiempo_max),
       op2.getTiempoOcioso(tiempo_max),
       op3.getTiempoOcioso(tiempo_max),
       op4.getTiempoOcioso(tiempo_max)
     ))
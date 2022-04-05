from fun import *
from byte import *
from bloque import *

run = True
conf = configuracion()
# bytes
size_memoria = 16


while run:
    print ("1.Byte")
    print ("2.Bloque")
    print ("3.Salir")
    opc = int(input("Ingresa una opcion: "))

    if (opc == 1):
        conf = configuracion(byte=True, bloque=False, size_bloque=1, size_memoria=size_memoria)
    elif (opc == 2):
        size_bloque = int(input("Ingrese el tamaño de los bloques:"))
        conf = configuracion(byte=False, bloque=True, size_bloque=size_bloque, size_memoria=size_memoria)
    elif (opc == 3):
        print("Saliendo....")
        run = False
    
# -------------------------------------------------------------------------------------------


    while run:
        if conf['byte']:
            run = opc_byte(conf)

        elif conf['bloque']:
            run = opc_byte(conf)
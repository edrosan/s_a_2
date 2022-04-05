from fun import *




def opc_byte(configuracion):
    run = True
    (total_bloques, ultimo_bloque) = cant_bloques(configuracion['size_memoria'], configuracion['size_bloque'])
    ram = [ {'id_file':0, 'no_parte':0, 'ocupado':0, 'size':configuracion['size_bloque']} ] * total_bloques
    ram[-1] = {'id_file':0, 'no_parte':0, 'ocupado':0, 'size':ultimo_bloque}
    info_ram = {'disponible':configuracion['size_memoria'], 'bloques':configuracion['size_memoria']}
    tabla_file = []
    while run:

        print()
        print("1.Crear archivo")
        print("2.Eliminar archivo")
        print("3.Desfragmentar")
        print("4.Visualizar")
        print("5.Salir")
        opc = int(input("Ingresa una opcion: "))

        if (opc == 1):
            file_name = str(input("Ingrese nombre del archivo: "))
            file_size = int(input("Ingrese el tamaño del archivo: "))

            espacio_disponible = espacio_memoria(espacio_disponible=info_ram['disponible'], file_size=file_size)

            if espacio_disponible:

                bloques_file = bloques_usados(size_bloque=configuracion['size_bloque'], file_size=file_size)
                file = archivo_nuevo (nombre=file_name, file_size=file_size, bloques_usados=bloques_file)
                tabla_file.append(file)
                ram = add_memoria (ram, file, configuracion)
                info_ram = actualizar_info(info_ram, ram)
                
            else:
                print('Espacion no disponible')
        
        elif (opc == 2):
            (ram, tabla_file) = eliminar_file(ram, tabla_file)
            info_ram = actualizar_info(info_ram, ram)

        elif (opc == 3):
            ram = desfragmentar(ram, tabla_file, configuracion)

        elif (opc == 4):
            print("1.Memoria")
            # print("2.Mapa")
            print("2.Listas")
            opc = int(input("Ingresa una opcion: "))

            if (opc == 1):
                print()
                print("Memoria:")
                print_memoria(ram)
                print()
                print("Archivos en memoria:")
                print_tabla(tabla_file)
            elif (opc == 2):
                lista_memoria = lista_nombre(ram)
                print()
                for nodo in lista_memoria:
                    print(f"{nodo}->", end="")
                print()

        elif (opc == 5):
            run = False
            return run

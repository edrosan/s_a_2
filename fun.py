import datetime
import math

def configuracion (byte=False, bloque=False, size_bloque=0, size_memoria=1):
    return {'byte': byte, 'bloque': bloque, 'size_bloque': size_bloque, 'size_memoria':size_memoria} 

def espacio_memoria (espacio_disponible=1, file_size=1):
    if espacio_disponible >= file_size:
        return True
    else:
        return False

def add_tabla (tabla_archivos, file):
    tabla = tabla_archivos.append(file)
    return tabla



    # Estructura nodo:
    # [{'id_file':0, 'no_parte':0, 'ocupado':0, 'total':1}]
    # Estructura memoria:
    # [{nodo},{nodo},{nodo}]
    # Estructura archivo:
    # {'file', 'id', 'hora_creacion', 'file_size', 'bloques_usados'}
    # ram = [ {'id_file':0, 'no_parte':0, 'ocupado':0, 'size':1} ]

def add_memoria (memoria, file, conf):
    memoria_aux = memoria
    no_bloques = 0
    total_bytes = file['file_size']

    if file['bloques_usados'] == 1:
        iniciales = total_bytes
        final = iniciales
    else:
        iniciales = conf['size_bloque']
        final = file['file_size'] - ((file['file_size']//conf['size_bloque'])*conf['size_bloque'])
        if final == 0:
            final = iniciales

    for (indice, nodo) in enumerate(memoria):
        if nodo['id_file'] == 0:
            if no_bloques <= (file['bloques_usados'] - 1):
                size = nodo['size']
                if no_bloques == file['bloques_usados'] - 1:
                    memoria_aux[indice] = {'id_file': file['id'], 'no_parte': no_bloques, 'ocupado': final, 'size':size}
                else:
                    memoria_aux[indice] = {'id_file': file['id'], 'no_parte': no_bloques, 'ocupado': iniciales, 'size':size}
                no_bloques += 1
            else:
                return memoria_aux
    return memoria_aux


    # info_ram = {'disponible':configuracion['size_memoria'], 'bloques':configuracion['size_memoria']}
    # Estructura archivo:
    # {'file', 'id', 'hora_creacion', 'file_size', 'bloques_usados'}
def actualizar_info(info_ram, memoria):

    espacio_disponible = 0
    for file in memoria:
        if file['id_file'] == 0:
            espacio_disponible += file['size']

    info_ram['disponible'] = espacio_disponible

    return info_ram




def sub_bytes (sub_bloque, disponible):
    return disponible - sub_bloque['total']

def bloques_usados (size_bloque=1.0, file_size=1.0):
    bloques_usados = math.ceil(file_size / size_bloque)
    print(f"Bloques usados: {bloques_usados}")
    return bloques_usados


def archivo_nuevo (nombre='undefined', file_size=0, bloques_usados=0):
    time = datetime.datetime.now()
    id = nombre.upper()[0] +'-'+ str(time.hour) + str(time.minute) + str(time.second)
    time = time.strftime("%X")

    file = {'file':nombre, 'id':id, 'hora_creacion':time, 'file_size':file_size, 'bloques_usados':bloques_usados}


    return file

# file = [{cabecera}, {parte_1}, {parte_2},{parte_3},.....,{parte_n}]
# file = [{file: nombre, size_file: size}, {}, {},{},.....,{}]
# conf = {byte: false, bloque: false, size_bloque: 0}
    # {'file', 'id', 'hora_creacion', 'file_size', 'bloques_usados'}


def print_tabla(tabla):
    print("--"*48)
    b = '\x1b[48;5;231m'
    r = '\x1b[0m'
    print(f"|\tNombre\t\t| ID\t\t|Hora Creacion\t|Tamaño en Bytes\t|Bloques usados|")
    print("--"*48)
    for file in tabla:
        print(f"|\t  {file['file']}\t\t| {file['id']}\t| {file['hora_creacion']}\t|    {file['file_size']}\t\t\t|  {file['bloques_usados']}\t       |")
    print("--"*48)

def print_memoria(memoria):
    print("[", end="")
    for file in memoria:
        print(f"{file['id_file']}:{file['no_parte']}", end=" | ")
    print("]")
    # for file in memoria:
    #     print(file)


def cant_bloques(size_memoria, size_bloques):
    total_bloques = math.ceil(size_memoria/size_bloques)
    # print(f"division: {size_memoria//size_bloques}")

    ultimo_bloque =  size_memoria - (size_memoria//size_bloques)*size_bloques

    if ultimo_bloque == 0:
        ultimo_bloque = size_bloques
    return (total_bloques, ultimo_bloque)

def eliminar_file(memoria, tabla_file):
    print()
    print("Archivos en memoria:")
    print_tabla(tabla_file)
    print()
    id_file = input("Ingresa el id del archivo a eliminar: ")

    for file in tabla_file:
        if(file['id'] == id_file):
            print("Archivo encontrado")
            tabla_file.remove(file)
            print(".................")
            print("Archivo eliminado")

    for (indice, file) in enumerate(memoria):
        size = file['size']
        if(file['id_file'] == id_file):
            memoria[indice] = {'id_file': 0, 'no_parte': 0, 'ocupado': 0, 'size':size}
        
    return (memoria, tabla_file)

def desfragmentar(memoria, tabla_file, conf):
    memoria_aux = memoria

    for (indice,file) in enumerate(memoria):
        size = file['size']
        memoria_aux[indice] = {'id_file': 0, 'no_parte': 0, 'ocupado': 0, 'size':size}

    for file in tabla_file:
        add_memoria (memoria_aux, file, conf)

    return memoria_aux


def crear_mapa_bits(tam_memoria):
    mapaBits = []
    n = (tam_memoria // 8)
    for i in range(n): 
        mapaBits.append([0] * 8)
    return mapaBits


def lista_nombre (ram):
    contHueco = 0
    contProce = 0
    procesoActual = 0
    tam = len (ram)
    lista = []

    for (i, elemento) in  enumerate(ram):
        if (elemento['id_file'] == 0):
            contHueco+= 1
            if (contProce != 0):
                posFinal = i-1
                posInicial = posFinal-contProce+1
                tam_proceso = (posFinal - posInicial) + 1
                lista.append([str(procesoActual),posInicial,posFinal])
                contProce = 0
        elif (elemento['id_file'] != 0):  
            if (contHueco != 0):
                posFinal = i-1
                posInicial = posFinal-contHueco+1
                tam_proceso = (posFinal - posInicial) + 1
                lista.append(['H',0,posInicial,posFinal])
                contHueco = 0 
            if (contProce == 0):
                procesoActual = elemento['id_file']
                parte_actual = elemento['no_parte']
                size_actual = elemento['ocupado']
                contProce+= 1
            else:
                if (procesoActual == elemento['id_file']):
                    contProce+=1
                else:
                    posFinal = i-1
                    posInicial = posFinal-contProce+1
                    tam_proceso = (posFinal - posInicial) + 1
                    lista.append([str(procesoActual),posInicial,posFinal])
                    contProce = 0
                    procesoActual = elemento['id_file']
                    parte_actual = elemento['no_parte']
                    size_actual = elemento['ocupado']
                    contProce+= 1

    if (contHueco != 0):
        posFinal = tam-1
        posInicial = posFinal-contHueco+1
        tam_proceso = (posFinal - posInicial) + 1
        lista.append(['H',0,posInicial,posFinal])
        contHueco = 0
    if (contProce != 0):
        posFinal = tam-1
        posInicial = posFinal-contProce+1
        tam_proceso = (posFinal - posInicial) + 1
        lista.append([str(ram[-1]['id_file']),posInicial,posFinal])
        contProce = 0
    return lista 


def lista_archivo (memoria):
    id_file = -1
    memoria_original = memoria
    memoria_aux = memoria

    for (indice,file) in enumerate(memoria_aux):
        if file['id_file'] != 0 and id_file != file['id_file'] and file['no_parte'] == 0:
            id_file = file['id_file']
            for file in memoria_aux:
                if id_file == file['id_file']:
                    print(f"{file['id_file']}:{file['no_parte']}-> ", end="")
                    # memoria_aux[indice]['id_file'] = 0
            print()

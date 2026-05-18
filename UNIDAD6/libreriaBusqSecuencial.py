# ==========================================================
# LIBRERÍA: BÚSQUEDA SECUENCIAL
# ==========================================================

def busqueda_secuencial(lista, valor):

    # RECORRER LISTA
    for i in range(len(lista)):

        # COMPARAR ELEMENTO
        if lista[i] == valor:

            return i

    # NO ENCONTRADO
    return -1

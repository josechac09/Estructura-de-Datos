# ==========================================================
# ORDENAMIENTO EXTERNO
# ==========================================================

def intercalacion_pasos(a, b):

    pasos = []
    resultado = []

    i = j = 0

    a = sorted(a)
    b = sorted(b)

    while i < len(a) and j < len(b):

        pasos.append((resultado + a[i:] + b[j:], [i, len(a)+j]))

        if a[i] <= b[j]:

            resultado.append(a[i])
            i += 1

        else:

            resultado.append(b[j])
            j += 1

    resultado += a[i:]
    resultado += b[j:]

    pasos.append((resultado.copy(), []))

    return resultado, pasos


# ==========================================================

def mezcla_directa_pasos(lista):

    pasos = []

    def merge_sort(arr):

        if len(arr) <= 1:
            return arr

        mid = len(arr)//2

        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])

        return merge(left, right)

    def merge(L, R):

        result = []

        while L and R:

            if L[0] <= R[0]:
                result.append(L.pop(0))
            else:
                result.append(R.pop(0))

            pasos.append((result + L + R, []))

        result += L + R

        pasos.append((result.copy(), []))

        return result

    resultado = merge_sort(lista.copy())

    return resultado, pasos


# ==========================================================

def mezcla_equilibrada_pasos(lista, k=3):

    pasos = []

    sublistas = [[] for _ in range(k)]

    for i, val in enumerate(lista):

        sublistas[i % k].append(val)

    sublistas = [sorted(s) for s in sublistas]

    pasos.append(([x for s in sublistas for x in s], []))

    while len(sublistas) > 1:

        nueva = []

        for i in range(0, len(sublistas), 2):

            if i + 1 < len(sublistas):

                mezcla = sorted(sublistas[i] + sublistas[i+1])

                nueva.append(mezcla)

                pasos.append((mezcla.copy(), []))

            else:
                nueva.append(sublistas[i])

        sublistas = nueva

    return sublistas[0], pasos

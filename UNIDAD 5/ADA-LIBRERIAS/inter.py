# ==========================================================
# ORDENAMIENTO INTERNO
# ==========================================================

def burbuja_pasos(lista):

    arr = lista.copy()
    pasos = []

    n = len(arr)

    for i in range(n):

        for j in range(0, n - i - 1):

            pasos.append((arr.copy(), [j, j + 1]))

            if arr[j] > arr[j + 1]:

                arr[j], arr[j + 1] = arr[j + 1], arr[j]

                pasos.append((arr.copy(), [j, j + 1]))

    return arr, pasos


# ==========================================================

def insercion_pasos(lista):

    arr = lista.copy()
    pasos = []

    for i in range(1, len(arr)):

        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:

            arr[j + 1] = arr[j]

            pasos.append((arr.copy(), [j, j + 1]))

            j -= 1

        arr[j + 1] = key

        pasos.append((arr.copy(), [j + 1]))

    return arr, pasos


# ==========================================================

def seleccion_pasos(lista):

    arr = lista.copy()
    pasos = []

    n = len(arr)

    for i in range(n):

        min_idx = i

        for j in range(i + 1, n):

            pasos.append((arr.copy(), [min_idx, j]))

            if arr[j] < arr[min_idx]:

                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]

        pasos.append((arr.copy(), [i, min_idx]))

    return arr, pasos


# ==========================================================

def shell_pasos(lista):

    arr = lista.copy()
    pasos = []

    n = len(arr)
    gap = n // 2

    while gap > 0:

        for i in range(gap, n):

            temp = arr[i]
            j = i

            while j >= gap and arr[j-gap] > temp:

                arr[j] = arr[j-gap]

                pasos.append((arr.copy(), [j, j-gap]))

                j -= gap

            arr[j] = temp

            pasos.append((arr.copy(), [j]))

        gap //= 2

    return arr, pasos


# ==========================================================

def quick_pasos(lista):

    arr = lista.copy()
    pasos = []

    def quick(low, high):

        if low < high:

            pi = partition(low, high)

            quick(low, pi - 1)
            quick(pi + 1, high)

    def partition(low, high):

        pivot = arr[high]

        i = low - 1

        for j in range(low, high):

            pasos.append((arr.copy(), [j, high]))

            if arr[j] < pivot:

                i += 1

                arr[i], arr[j] = arr[j], arr[i]

                pasos.append((arr.copy(), [i, j]))

        arr[i+1], arr[high] = arr[high], arr[i+1]

        pasos.append((arr.copy(), [i+1, high]))

        return i + 1

    quick(0, len(arr)-1)

    return arr, pasos


# ==========================================================

def heap_pasos(lista):

    arr = lista.copy()
    pasos = []

    def heapify(n, i):

        largest = i

        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and arr[l] > arr[largest]:
            largest = l

        if r < n and arr[r] > arr[largest]:
            largest = r

        if largest != i:

            arr[i], arr[largest] = arr[largest], arr[i]

            pasos.append((arr.copy(), [i, largest]))

            heapify(n, largest)

    n = len(arr)

    for i in range(n//2 -1, -1, -1):
        heapify(n, i)

    for i in range(n-1, 0, -1):

        arr[i], arr[0] = arr[0], arr[i]

        pasos.append((arr.copy(), [0, i]))

        heapify(i, 0)

    return arr, pasos


# ==========================================================

def radix_pasos(lista):

    arr = lista.copy()
    pasos = []

    if any(x < 0 for x in arr):
        raise ValueError("Radix no acepta negativos")

    exp = 1
    max_num = max(arr)

    while max_num // exp > 0:

        output = [0] * len(arr)
        count = [0] * 10

        for num in arr:
            index = (num // exp) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = len(arr) - 1

        while i >= 0:

            index = (arr[i] // exp) % 10

            output[count[index] - 1] = arr[i]

            count[index] -= 1

            i -= 1

        for i in range(len(arr)):

            arr[i] = output[i]

            pasos.append((arr.copy(), [i]))

        exp *= 10

    return arr, pasos

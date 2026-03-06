import random
from typing import List, Any

def fisher_yates_shuffle(arr: List[Any]) -> List[Any]:
    """
    Implementación del algoritmo de Fisher-Yates para barajar una lista.
    Este algoritmo asegura una aleatoriedad uniforme y máxima entropía.
    """
    n = len(arr)
    # Hacemos una copia para no mutar la original si no es deseado
    # por seguridad en la lógica de negocio
    shuffled = list(arr)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
    return shuffled

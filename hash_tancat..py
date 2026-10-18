# Estats d'una posició de la taula (hash tancat). NO canvieu aquests valors.
LLIURE = "L"
OCUPAT = "O"
ESBORRAT = "B"


class MyHashMap:
    """Taula de hash amb UNA SOLA parella per posició (versió de l'escalfament).

    Cada posició de self._table és None o una parella [clau, valor].
    Si dues claus van a la mateixa posició, put() llança KeyError (col·lisió).
    """

    def __init__(self, cap=13):
        self._table = cap * [None]    # m posicions, inicialment buides
        self._state = cap * [LLIURE] 
        self._n = 0                   # nombre de claus desades

    def _hash_function(self, key):
        return key % len(self._table)    # h(x) = x % m

    def put(self, key: int, value: int) -> None:
        m = len(self._table)
        j = self._hash_function(key)
        primera_esborrada = None

        for _ in range(m):

            if self._state[j] == OCUPAT:    
                if self._table[j][0] == key:
                    self._table[j][1] = value
                    return

            elif self._state[j] == ESBORRAT:
                if primera_esborrada is None:
                    primera_esborrada = j

            else:  
                if primera_esborrada is not None:
                    j = primera_esborrada

                self._table[j] = [key, value]
                self._state[j] = OCUPAT
                self._n += 1
                return

            j = (j + 1) % m

        if primera_esborrada is not None:
            self._table[primera_esborrada] = [key, value]
            self._state[primera_esborrada] = OCUPAT
            self._n += 1
            return

        raise KeyError("La taula hash està plena")

    def get(self, key: int) -> int:
        m = len(self._table)
        j = self._hash_function(key)

        for _ in range(m):

            if self._state[j] == LLIURE:
                return -1

            if self._state[j] == OCUPAT:
                if self._table[j][0] == key:
                    return self._table[j][1]

            j = (j + 1) % m

        return -1

    def remove(self, key: int) -> None:
        m = len(self._table)
        j = self._hash_function(key)

        for _ in range(m):

            if self._state[j] == LLIURE:
                return

            if self._state[j] == OCUPAT:
                if self._table[j][0] == key:
                    self._table[j] = None
                    self._state[j] = ESBORRAT
                    self._n -= 1
                    return

            j = (j + 1) % m

    def __len__(self):
        return self._n
# Estats d'una posició de la taula (hash tancat). NO canvieu aquests valors.
LLIURE = "L"
OCUPAT = "O"
ESBORRAT = "B"


class MyHashMap:
    """Taula de hash amb adreçament obert i sondeig lineal.

    Cada posició de self._table és una llista [clau, valor, estat].
    Si dues claus van a la mateixa posició, es busca la següent posició disponible.
    """

    def __init__(self, cap=13):
        self._table = [[None, None, LLIURE] for _ in range(cap)]  # m posicions, inicialment buides
        self._n = 0                  # nombre de claus desades

    def _hash_function(self, key):
        return key % len(self._table)          # h(x) = x % m

    def _find(self, key):
        m = len(self._table)
        j = self._hash_function(key)

        for _ in range(m):
            if self._table[j][2] == LLIURE:
                return None

            if self._table[j][2] == OCUPAT:
                if self._table[j][0] == key:
                    return j

            j = (j + 1) % m

        return None

    def put(self, key: int, value: int) -> None:
        m = len(self._table)
        j = self._hash_function(key)
        primera_esborrada = None

        for _ in range(m):
            estat = self._table[j][2]

            if estat == OCUPAT:
                if self._table[j][0] == key:  # mateixa clau: actualitzem
                    self._table[j][1] = value
                    return

            elif estat == ESBORRAT:
                if primera_esborrada is None:
                    primera_esborrada = j

            else:                             # posició lliure
                if primera_esborrada is not None:
                    j = primera_esborrada

                self._table[j] = [key, value, OCUPAT]
                self._n += 1

                if self._n > len(self._table) // 2:
                    self._resize(2 * len(self._table) - 1)

                return

            j = (j + 1) % m

        # Si no hi ha posicions lliures, reutilitzem una posició esborrada
        if primera_esborrada is not None:
            self._table[primera_esborrada] = [key, value, OCUPAT]
            self._n += 1

            if self._n > len(self._table) // 2:
                self._resize(2 * len(self._table) - 1)

            return

        raise KeyError("La taula hash està plena")

    def get(self, key: int) -> int:
        j = self._find(key)

        if j is not None:
            return self._table[j][1]

        return -1

    def remove(self, key: int) -> None:
        j = self._find(key)

        if j is not None:
            self._table[j] = [None, None, ESBORRAT]
            self._n -= 1

    def __len__(self):
        return self._n

    def _resize(self, c):
        old_table = self._table

        # Creem una taula nova amb totes les posicions lliures
        self._table = [[None, None, LLIURE] for _ in range(c)]
        self._n = 0

        # Tornem a inserir només les parelles ocupades
        for parella in old_table:
            if parella[2] == OCUPAT:
                self.put(parella[0], parella[1])
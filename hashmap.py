class MyHashMap:
    """Taula de hash amb UNA SOLA parella per posició (versió de l'escalfament).

    Cada posició de self._table és None o una parella [clau, valor].
    Si dues claus van a la mateixa posició, put() llança KeyError (col·lisió).
    """

    def __init__(self, cap=13):
        self._table = cap * [None]   # m posicions, inicialment buides
        self._n = 0                  # nombre de claus desades

    def _hash_function(self, key):
        return key % len(self._table)          # h(x) = x % m

    def put(self, key: int, value: int) -> None:
        j = self._hash_function(key)

        if self._table[j] is None:
            self._table[j] = [[key, value]]
            self._n += 1

        else:
            bucket = self._table[j]

            for parella in bucket:
                if parella[0] == key:
                    parella[1] = value
                    return

            bucket.append([key, value])
            self._n += 1

        if self._n > len(self._table) // 2:
            self._resize(2 * len(self._table) - 1)

    def get(self, key: int) -> int:
        j = self._hash_function(key)

        if self._table[j] is None:
            return -1

        bucket = self._table[j]

        for parella in bucket:
            if parella[0] == key:
                return parella[1]

        return -1

    def remove(self, key: int) -> None:
        j = self._hash_function(key)

        if self._table[j] is None:
            return

        bucket = self._table[j]

        for parella in bucket:
            if parella[0] == key:
                bucket.remove(parella)
                self._n -= 1

                if len(bucket) == 0:
                    self._table[j] = None

                return

    def __len__(self):
        return self._n

    def _resize(self, new_cap: int) -> None:
    
        old_table = self._table

        self._table = new_cap * [None]


        self._n = 0

        for bucket in old_table:
            if bucket is not None:
                for parella in bucket:
                    self.put(parella[0], parella[1])
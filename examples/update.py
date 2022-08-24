from filterbox import FilterBox


class Changey:
    """A class containing a variable _n that changes. On change, it will update each FilterBox in its listeners."""

    def __init__(self, n):
        self._n = n
        self.listeners = []

    def add_listener(self, f: FilterBox):
        self.listeners.append(f)

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, new_n):
        for f in self.listeners:
            f.remove(self)
        self._n = new_n
        for f in self.listeners:
            f.add(self)


def main():
    objs = [Changey(1) for _ in range(10)]
    f = FilterBox(objs, ["n"])
    for obj in objs:
        obj.add_listener(f)
    assert len(f[{"n": 1}]) == 10

    # change an object
    objs[0].n = 2

    # see that changes are propagated to FilterBox
    assert len(f[{"n": 1}]) == 9
    assert len(f[{"n": 2}]) == 1
    print("Completed. See code for details.")


if __name__ == "__main__":
    main()


class TapeCell:
    """A single cell in the doubly linked tape."""

    def __init__(self, symbol='_', position=0):
        self.symbol = symbol
        self.position = position
        self.prev = None
        self.next = None


class Tape:
    moves = {
        'S': 0,
        'R': 1,
        'L': -1
    }

    def __init__(self):
        self.first = TapeCell('_', -1)
        self.current = TapeCell('>', 0)
        self.last = TapeCell('_', 1)

        self.first.next = self.current
        self.current.prev = self.first

        self.current.next = self.last
        self.last.prev = self.current

        self._head = 0

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, position):
        node = self.first

        while node is not None and node.position < position:
            node = node.next

        if node is None or node.position != position:
            raise IndexError("Tape position does not exist")

        self.current = node
        self._head = position

    @property
    def min_head(self):
        return self.first.position

    @property
    def max_head(self):
        return self.last.position

    def _blank_first_cell(self):
        if self.first.symbol != '_':
            new_cell = TapeCell('_', self.first.position - 1)
            new_cell.next = self.first
            self.first.prev = new_cell
            self.first = new_cell

    def _blank_last_cell(self):
        if self.last.symbol != '_':
            new_cell = TapeCell('_', self.last.position + 1)
            new_cell.prev = self.last
            self.last.next = new_cell
            self.last = new_cell

    def move(self, key):
        if key not in self.moves:
            raise ValueError(f"Invalid movement: {key}")

        direction = self.moves[key]

        if direction == 1:
            if self.current.next is None:
                new_cell = TapeCell('_', self.current.position + 1)
                new_cell.prev = self.current
                self.current.next = new_cell
                self.last = new_cell

            self.current = self.current.next

        elif direction == -1:
            if self.current.prev is None:
                new_cell = TapeCell('_', self.current.position - 1)
                new_cell.next = self.current
                self.current.prev = new_cell
                self.first = new_cell

            self.current = self.current.prev

        self._head = self.current.position

    def read(self):
        return self.current.symbol

    def write(self, symbol):
        self.current.symbol = symbol
        self._blank_first_cell()
        self._blank_last_cell()

    def __repr__(self):
        symbols = []
        node = self.first

        while node is not None:
            if node == self.current:
                symbols.append('|' + node.symbol)
            else:
                symbols.append(node.symbol)

            node = node.next

        return '..|' + '|'.join(symbols) + '|..'

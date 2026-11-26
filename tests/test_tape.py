
import unittest

from TMsim.tape import Tape


class TapeTests(unittest.TestCase):

    def setUp(self):
        self.tape = Tape()

    def test_initialization(self):
        self.assertEqual(self.tape.read(), '>')

    def test_write_and_read(self):
        self.tape.write('1')
        self.assertEqual(self.tape.read(), '1')

    def test_move_right(self):
        self.tape.move('R')
        self.assertEqual(self.tape.head, 1)
        self.assertEqual(self.tape.read(), '_')

    def test_move_left(self):
        self.tape.move('L')
        self.assertEqual(self.tape.head, -1)
        self.assertEqual(self.tape.read(), '_')

    def test_move_stay(self):
        self.tape.write('0')
        self.tape.move('S')
        self.assertEqual(self.tape.head, 0)
        self.assertEqual(self.tape.read(), '0')

    def test_create_blank_cell_left(self):
        self.tape.move('L')
        self.tape.move('L')
        self.assertEqual(self.tape.head, -2)
        self.assertEqual(self.tape.read(), '_')

    def test_create_blank_cell_right(self):
        self.tape.move('R')
        self.tape.move('R')
        self.assertEqual(self.tape.head, 2)
        self.assertEqual(self.tape.read(), '_')

    def test_invalid_movement(self):
        with self.assertRaises(ValueError):
            self.tape.move('X')


if __name__ == '__main__':
    unittest.main()

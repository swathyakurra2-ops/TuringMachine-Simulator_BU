import unittest

from TMsim.parsing import (
    parse_string,
    parse_text,
    get_delta_dict
)


class ParsingTests(unittest.TestCase):

    def test_parse_string(self):
        result = parse_string("{0,1,2}")
        self.assertEqual(result, {"0", "1", "2"})

    def test_parse_text(self):
        lines = [
            "NUM_TAPES = 1\n",
            "ALPHABET = {0, 1, >, _}\n",
            "STATES = {Qinit, Q1, Qhalt}\n",
            "TRANSITION_FUNC =\n",
            "(Qinit, >) --> (Q1, >, R)\n"
        ]

        num_tapes, alphabet, states, transitions = parse_text(lines)

        self.assertEqual(num_tapes, 1)
        self.assertEqual(alphabet, {"0", "1", ">", "_"})
        self.assertEqual(states, {"Qinit", "Q1", "Qhalt"})
        self.assertEqual(len(transitions), 1)

    def test_get_delta_dict(self):
        transitions = [
            "(Q1, 0) --> (Q1, 1, R)"
        ]

        alphabet = {"0", "1"}

        result = get_delta_dict(transitions, alphabet)

        self.assertIn(("Q1", "0"), result)
        self.assertEqual(
            result[("Q1", "0")],
            ("Q1", "1", "R")
        )


if __name__ == "__main__":
    unittest.main()
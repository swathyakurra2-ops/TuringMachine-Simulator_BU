import unittest
from pathlib import Path

from TMsim.machine import TuringMachine
from TMsim.execution import ExecutionEngine

ROOT = Path(__file__).resolve().parents[1]


class ExecutionEngineTests(unittest.TestCase):
    def make_engine(self, max_steps=1000):
        machine = TuringMachine.from_txt(str(ROOT / "codes" / "1tape_inverse.txt"))
        machine.load_input("0101")
        return ExecutionEngine(machine, input_string="0101", max_steps=max_steps, delay=0)

    def test_single_step_increments_counter_once(self):
        engine = self.make_engine()
        self.assertTrue(engine.execute_step())
        self.assertEqual(engine.machine.steps, 1)
        self.assertEqual(len(engine.get_history()), 1)

    def test_continuous_execution_reaches_halt(self):
        engine = self.make_engine()
        result = engine.run_continuously()
        self.assertEqual(result, "HALTED")
        self.assertGreater(engine.machine.steps, 0)

    def test_reset_restores_initial_configuration(self):
        engine = self.make_engine()
        engine.execute_step()
        engine.reset()
        self.assertEqual(engine.machine.steps, 0)
        self.assertEqual(engine.machine.state, "Qinit")
        self.assertEqual(len(engine.get_history()), 0)

    def test_maximum_step_limit(self):
        engine = self.make_engine(max_steps=1)
        engine.run_continuously()
        self.assertEqual(engine.status, "STEP_LIMIT")


if __name__ == "__main__":
    unittest.main()

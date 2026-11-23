"""Small interactive runner for the TMsimulator project."""
from pathlib import Path
import threading

from TMsim.machine import TuringMachine
from TMsim.execution import ExecutionEngine

ROOT = Path(__file__).resolve().parent


def print_status(engine):
    info = engine.get_status()
    print(f"\nStatus: {info['status']} | State: {info['state']} | Steps: {info['step']}")
    if info["reason"]:
        print(f"Reason: {info['reason']}")
    for index, tape in enumerate(info["configuration"]["tapes"], start=1):
        print(f"Tape {index}: {tape}")


def main():
    default_file = ROOT / "codes" / "1tape_inverse.txt"
    print("TURING MACHINE SIMULATOR — Execution Engine Demo")
    print(f"Default machine: {default_file.name}")
    choice = input("Machine file [press Enter for default]: ").strip()
    machine_file = Path(choice).expanduser() if choice else default_file
    if not machine_file.is_absolute():
        machine_file = ROOT / machine_file
    if not machine_file.exists():
        raise SystemExit(f"Machine definition not found: {machine_file}")

    input_string = input("Input string (binary for the default example): ").strip()
    machine = TuringMachine.from_txt(str(machine_file))
    machine.load_input(input_string)
    engine = ExecutionEngine(machine, input_string=input_string, max_steps=10000, delay=0.15)

    print("\nCommands: step | run | pause | resume | status | history | reset | quit")
    print_status(engine)
    worker = None
    while True:
        command = input("\nTM> ").strip().lower()
        if command == "step":
            engine.execute_step()
            print_status(engine)
        elif command == "run":
            if worker and worker.is_alive():
                print("Execution is already running.")
            else:
                worker = threading.Thread(target=engine.run_continuously, daemon=True)
                worker.start()
                print("Continuous execution started. Use 'pause' to pause it.")
        elif command == "pause":
            engine.pause()
            print_status(engine)
        elif command == "resume":
            engine.resume()
            print_status(engine)
        elif command == "status":
            print_status(engine)
        elif command == "history":
            for item in engine.get_history():
                print(f"Step {item['before']['step']}: {item['before']['state']} -> {item['after']['state']}")
            if not engine.get_history():
                print("No transitions recorded yet.")
        elif command == "reset":
            engine.reset()
            print("Simulation reset.")
            print_status(engine)
        elif command in {"quit", "exit"}:
            engine.stop()
            if worker and worker.is_alive():
                worker.join(timeout=1)
            print("Goodbye.")
            break
        elif command:
            print("Unknown command. Use: step, run, pause, resume, status, history, reset, quit")


if __name__ == "__main__":
    main()

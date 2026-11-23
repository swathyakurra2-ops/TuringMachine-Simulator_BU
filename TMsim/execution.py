"""Execution controls added for the CSET302 team project.

This module wraps the original TuringMachine class instead of replacing its
machine, transition, or tape implementation.
"""
from __future__ import annotations

import threading
import time
from typing import Any, Dict, List, Optional


class ExecutionEngine:
    """Provides step, continuous, pause, resume, reset and history controls."""

    def __init__(self, machine, input_string: str = "", max_steps: int = 1000,
                 delay: float = 0.05):
        if max_steps < 1:
            raise ValueError("max_steps must be at least 1")
        if delay < 0:
            raise ValueError("delay cannot be negative")
        self.machine = machine
        self.input_string = input_string
        self.max_steps = max_steps
        self.delay = delay
        self.history: List[Dict[str, Any]] = []
        self.status = "READY"
        self.reason: Optional[str] = None
        self._run_event = threading.Event()
        self._run_event.set()
        self._stop_event = threading.Event()
        self._lock = threading.RLock()
        self._worker: Optional[threading.Thread] = None
        self.reset()

    def _configuration(self):
        return {
            "step": self.machine.steps,
            "state": self.machine.state,
            "tapes": [repr(tape) for tape in self.machine.tapes],
        }

    def _finish_if_halted(self) -> bool:
        state = self.machine.state
        if state == "Qaccept":
            self.status, self.reason = "ACCEPTED", "Accepting state reached"
        elif state == "Qreject":
            self.status, self.reason = "REJECTED", "Rejecting state reached"
        elif state == "Qhalt":
            self.status, self.reason = "HALTED", "Halting state reached"
        elif state in self.machine.halt_states:
            self.status, self.reason = "HALTED", "Halting state reached"
        else:
            return False
        self._run_event.set()
        return True

    def execute_step(self) -> bool:
        """Execute exactly one transition; return False if no step was made."""
        with self._lock:
            if self._finish_if_halted():
                return False
            if self.machine.steps >= self.max_steps:
                self.status, self.reason = "STEP_LIMIT", "Maximum step limit reached"
                return False

            before = self._configuration()
            try:
                self.machine.make_step()
            except KeyError:
                self.status = "NO_TRANSITION"
                self.reason = f"No transition defined for configuration {self.machine.get_config()}"
                self._run_event.set()
                return False
            except (ValueError, IndexError) as exc:
                self.status, self.reason = "ERROR", str(exc)
                self._run_event.set()
                return False

            self.machine.steps += 1
            after = self._configuration()
            self.history.append({"before": before, "after": after})
            self.status = "RUNNING"
            self.reason = None
            self._finish_if_halted()
            if self.machine.steps >= self.max_steps and self.status == "RUNNING":
                self.status, self.reason = "STEP_LIMIT", "Maximum step limit reached"
            return True

    def run_continuously(self, delay: Optional[float] = None) -> str:
        """Run until halt, missing transition, step limit, or pause request.

        Call this in a worker thread if the caller needs to issue pause() while
        the machine is running.
        """
        wait = self.delay if delay is None else delay
        if wait < 0:
            raise ValueError("delay cannot be negative")
        with self._lock:
            if self._finish_if_halted():
                return self.status
            if self.status in {"ACCEPTED", "REJECTED", "HALTED", "NO_TRANSITION", "ERROR", "STEP_LIMIT"}:
                return self.status
            self.status = "RUNNING"
            self._stop_event.clear()
            self._run_event.set()

        while not self._stop_event.is_set():
            self._run_event.wait()
            if self._stop_event.is_set():
                break
            if not self.execute_step():
                break
            if wait:
                time.sleep(wait)

        with self._lock:
            if self.status == "RUNNING":
                self.status, self.reason = "PAUSED", "Execution paused"
            return self.status

    def start_background(self, delay: Optional[float] = None) -> None:
        """Start continuous execution on a background thread."""
        if self._worker and self._worker.is_alive():
            return
        self._worker = threading.Thread(
            target=self.run_continuously, args=(delay,), daemon=True
        )
        self._worker.start()

    def pause(self) -> None:
        if self.status == "RUNNING":
            self._run_event.clear()
            self.status, self.reason = "PAUSED", "Execution paused"

    def resume(self) -> None:
        if self.status == "PAUSED":
            self.status, self.reason = "RUNNING", None
            self._run_event.set()

    def stop(self) -> None:
        """Stop a background run without resetting the current configuration."""
        self._stop_event.set()
        self._run_event.set()

    def reset(self) -> None:
        """Restore the machine and input to their initial configuration."""
        with self._lock:
            self.stop()
            if self._worker and self._worker.is_alive() and self._worker is not threading.current_thread():
                self._worker.join(timeout=1)
            self.machine._initialize()
            if self.input_string:
                self.machine.load_input(self.input_string)
            self.history = []
            self.status, self.reason = "READY", None
            self._stop_event.clear()
            self._run_event.set()

    def get_status(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "status": self.status,
                "reason": self.reason,
                "step": self.machine.steps,
                "state": self.machine.state,
                "configuration": self._configuration(),
            }

    def get_history(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self.history)

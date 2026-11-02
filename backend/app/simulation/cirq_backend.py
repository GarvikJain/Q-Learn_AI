from .adapter import SimulatorAdapter

class CirqBackend(SimulatorAdapter):
    def run(self, circuit_schema: dict, shots: int) -> dict:
        raise NotImplementedError("Cirq backend coming in v2.0")

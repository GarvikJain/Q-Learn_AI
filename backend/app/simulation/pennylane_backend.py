from .adapter import SimulatorAdapter

class PennyLaneBackend(SimulatorAdapter):
    def run(self, circuit_schema: dict, shots: int) -> dict:
        raise NotImplementedError("PennyLane backend coming in v2.0")

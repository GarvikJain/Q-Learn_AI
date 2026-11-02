from abc import ABC, abstractmethod

class SimulatorAdapter(ABC):
    @abstractmethod
    def run(self, circuit_schema: dict, shots: int) -> dict:
        pass

def get_simulator(backend_name: str) -> SimulatorAdapter:
    if backend_name == 'qiskit_aer':
        from .qiskit_backend import QiskitAerBackend
        return QiskitAerBackend()
    elif backend_name == 'pennylane':
        from .pennylane_backend import PennyLaneBackend
        return PennyLaneBackend()
    elif backend_name == 'cirq':
        from .cirq_backend import CirqBackend
        return CirqBackend()
    else:
        raise ValueError(f"Unknown backend: {backend_name}")

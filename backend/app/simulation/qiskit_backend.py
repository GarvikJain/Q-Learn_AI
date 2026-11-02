import time
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
from .adapter import SimulatorAdapter


class QiskitAerBackend(SimulatorAdapter):
    """Qiskit Aer simulation backend (Qiskit 2.x compatible)."""

    def __init__(self):
        self.simulator = AerSimulator()

    def run(self, circuit_schema: dict, shots: int = 1024) -> dict:
        start_time = time.time()

        num_qubits = circuit_schema.get("num_qubits", 1)
        gates = circuit_schema.get("gates", [])

        # Validate circuit
        if not gates:
            raise ValueError(
                "Circuit is empty. Add at least one gate and one measurement before running."
            )
        has_measurement = any(
            g.get("type", "").upper() in ("M", "MEASURE") for g in gates
        )
        if not has_measurement:
            raise ValueError(
                "Circuit has no measurement. Add a Measurement (M) gate to at least one qubit."
            )
        if num_qubits < 1 or num_qubits > 10:
            raise ValueError("Number of qubits must be between 1 and 10.")

        # Build QuantumCircuit
        qc = QuantumCircuit(num_qubits, num_qubits)

        # Sort gates by time step
        sorted_gates = sorted(gates, key=lambda g: g.get("step", 0))

        measurement_qubits = set()
        for gate in sorted_gates:
            gtype = gate.get("type", "").upper()
            if gtype == "MEASURE":
                gtype = "M"
            targets = gate.get("targets", [])
            control = gate.get("control")

            # Validate qubit indices
            for t in targets:
                if t >= num_qubits:
                    raise ValueError(f"Gate target qubit {t} out of range (circuit has {num_qubits} qubits).")
            if control is not None and control >= num_qubits:
                raise ValueError(f"CNOT control qubit {control} out of range.")

            if gtype == "H":
                qc.h(targets[0])
            elif gtype == "X":
                qc.x(targets[0])
            elif gtype == "Y":
                qc.y(targets[0])
            elif gtype == "Z":
                qc.z(targets[0])
            elif gtype == "S":
                qc.s(targets[0])
            elif gtype == "T":
                qc.t(targets[0])
            elif gtype in ("CNOT", "CX"):
                if control is None:
                    raise ValueError("CNOT gate requires a control qubit. Select the control before adding the gate.")
                if control == targets[0]:
                    raise ValueError("CNOT control and target qubits must be different.")
                qc.cx(control, targets[0])
            elif gtype in ("TOFFOLI", "CCX"):
                controls = gate.get("controls") or []
                if len(controls) < 2 and control is not None and len(targets) >= 2:
                    # Fallback: control + first two targets
                    controls = [control, targets[0]]
                    targets = targets[1:]
                if len(controls) < 2:
                    raise ValueError("Toffoli gate requires exactly 2 control qubits.")
                qc.ccx(controls[0], controls[1], targets[0])
            elif gtype == "SWAP":
                if len(targets) >= 2:
                    qc.swap(targets[0], targets[1])
                elif control is not None and len(targets) >= 1:
                    qc.swap(control, targets[0])
                else:
                    raise ValueError("SWAP gate requires exactly 2 target qubits.")
            elif gtype == "M":
                for t in targets:
                    if t not in measurement_qubits:
                        qc.measure(t, t)
                        measurement_qubits.add(t)
            else:
                raise ValueError(f"Unknown gate type: {gtype}")

        # Run shot-based simulation
        transpiled_qc = transpile(qc, self.simulator)
        job = self.simulator.run(transpiled_qc, shots=shots)
        result = job.result()
        counts = result.get_counts(transpiled_qc)

        # Normalize counts keys (remove spaces from multi-qubit results)
        counts = {k.replace(" ", ""): v for k, v in counts.items()}
        probabilities = {k: round(v / shots, 6) for k, v in counts.items()}

        # Extract statevector for small circuits (pre-measurement)
        statevector = None
        if num_qubits <= 5:
            try:
                sv_qc = qc.remove_final_measurements(inplace=False)
                sv = Statevector.from_instruction(sv_qc)
                # Return as list of [real, imag] pairs for JSON serialization
                statevector = [[float(c.real), float(c.imag)] for c in sv.data]
            except Exception:
                statevector = None

        end_time = time.time()

        return {
            "counts": counts,
            "probabilities": probabilities,
            "statevector": statevector,
            "execution_time_ms": round((end_time - start_time) * 1000, 2),
            "backend_used": "qiskit_aer",
            "num_qubits": num_qubits,
        }

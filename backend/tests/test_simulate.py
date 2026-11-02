"""
Direct unit tests for the Qiskit simulation backend — no DB or HTTP server needed.
These map to the traceability matrix test cases TC-04 to TC-10.
"""
import pytest
from app.simulation.qiskit_backend import QiskitAerBackend


@pytest.fixture(scope="module")
def backend():
    return QiskitAerBackend()


# TC-04 / T-05: Single-qubit H gate → ~50% probability each
def test_h_gate_simulation(backend):
    circuit = {
        "num_qubits": 1,
        "gates": [
            {"type": "H", "targets": [0], "step": 0},
            {"type": "M", "targets": [0], "step": 1},
        ],
    }
    result = backend.run(circuit, shots=2048)

    assert "counts" in result
    assert "probabilities" in result
    assert "execution_time_ms" in result
    assert result["backend_used"] == "qiskit_aer"
    assert result["num_qubits"] == 1

    counts = result["counts"]
    assert "0" in counts
    assert "1" in counts
    # With 2048 shots, expect roughly 50/50 — allow ±20% tolerance
    assert 0.30 <= result["probabilities"]["0"] <= 0.70
    assert 0.30 <= result["probabilities"]["1"] <= 0.70


# TC-06 / T-06: Bell state → only |00⟩ and |11⟩ appear
def test_bell_state_simulation(backend):
    circuit = {
        "num_qubits": 2,
        "gates": [
            {"type": "H", "targets": [0], "step": 0},
            {"type": "CNOT", "control": 0, "targets": [1], "step": 1},
            {"type": "M", "targets": [0, 1], "step": 2},
        ],
    }
    result = backend.run(circuit, shots=2048)

    counts = result["counts"]
    # Only |00⟩ and |11⟩ should appear in an ideal simulation
    for key in counts:
        assert key in ("00", "11"), f"Unexpected basis state: {key}"

    # Both should have ~50% probability
    probs = result["probabilities"]
    total_prob = sum(probs.values())
    assert abs(total_prob - 1.0) < 0.01


# X gate: |0⟩ → |1⟩ → always measure 1
def test_x_gate_simulation(backend):
    circuit = {
        "num_qubits": 1,
        "gates": [
            {"type": "X", "targets": [0], "step": 0},
            {"type": "M", "targets": [0], "step": 1},
        ],
    }
    result = backend.run(circuit, shots=256)
    assert result["probabilities"].get("1", 0) == pytest.approx(1.0, abs=0.01)
    assert result["probabilities"].get("0", 0) == pytest.approx(0.0, abs=0.01)


# TC-07 / T-07: Empty circuit → ValueError with descriptive message
def test_empty_circuit_raises_error(backend):
    circuit = {"num_qubits": 1, "gates": []}
    with pytest.raises(ValueError, match="empty"):
        backend.run(circuit, shots=100)


# TC-10: No measurement gate → ValueError
def test_no_measurement_raises_error(backend):
    circuit = {
        "num_qubits": 1,
        "gates": [{"type": "H", "targets": [0], "step": 0}],
    }
    with pytest.raises(ValueError, match="measurement"):
        backend.run(circuit, shots=100)


# CNOT without control → ValueError
def test_cnot_without_control_raises_error(backend):
    circuit = {
        "num_qubits": 2,
        "gates": [
            {"type": "CNOT", "targets": [1], "step": 0},  # Missing 'control'
            {"type": "M", "targets": [0, 1], "step": 1},
        ],
    }
    with pytest.raises(ValueError, match="control"):
        backend.run(circuit, shots=100)


# Statevector should be returned for ≤5 qubit circuits
def test_statevector_returned_for_small_circuits(backend):
    from app.schemas.simulation import SimulationResult

    circuit = {
        "num_qubits": 1,
        "gates": [
            {"type": "H", "targets": [0], "step": 0},
            {"type": "M", "targets": [0], "step": 1},
        ],
    }
    result = backend.run(circuit, shots=256)
    assert result["statevector"] is not None
    assert len(result["statevector"]) == 2  # 2^1 = 2 amplitudes
    # API schema must accept [[real, imag], ...] pairs (JSON-safe)
    parsed = SimulationResult(**result)
    assert parsed.statevector is not None
    assert isinstance(parsed.statevector[0], list)


# Z gate on |0⟩ leaves it unchanged → still 100% |0⟩
def test_z_gate_on_zero(backend):
    circuit = {
        "num_qubits": 1,
        "gates": [
            {"type": "Z", "targets": [0], "step": 0},
            {"type": "M", "targets": [0], "step": 1},
        ],
    }
    result = backend.run(circuit, shots=256)
    assert result["probabilities"].get("0", 0) == pytest.approx(1.0, abs=0.01)

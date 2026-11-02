import os
from typing import Optional
from app.core.config import settings
from .prompts import BEGINNER_EXPLAIN_PROMPT, DEBUG_CIRCUIT_PROMPT, CONCEPT_DEEP_PROMPT, CODE_GENERATE_PROMPT

# Static fallback answers for mock mode
MOCK_ANSWERS = {
    "superposition": (
        "Superposition means a qubit can be in both |0⟩ and |1⟩ at the same time — like a "
        "coin spinning in the air that is both heads and tails until it lands. "
        "The Hadamard (H) gate creates superposition: H|0⟩ = (|0⟩ + |1⟩)/√2, "
        "giving a 50% chance of measuring 0 and 50% chance of measuring 1."
    ),
    "entanglement": (
        "Entanglement links two qubits so that measuring one instantly determines the other, "
        "no matter how far apart they are. Apply H then CNOT to create the Bell state "
        "|Φ+⟩ = (|00⟩ + |11⟩)/√2. Measuring this always gives |00⟩ or |11⟩ — never |01⟩ or |10⟩."
    ),
    "qubit": (
        "A qubit is the quantum equivalent of a classical bit, but it can be 0, 1, or any "
        "superposition α|0⟩ + β|1⟩ where |α|² + |β|² = 1. When measured it collapses to "
        "0 with probability |α|² or 1 with probability |β|²."
    ),
    "hadamard": (
        "The Hadamard (H) gate is a fundamental quantum gate that creates superposition. "
        "H|0⟩ = (|0⟩ + |1⟩)/√2 and H|1⟩ = (|0⟩ - |1⟩)/√2. "
        "Applied twice it returns to the original state (H² = I). "
        "On the Bloch sphere, it rotates the north pole to the equator."
    ),
    "bell state": (
        "Bell states are the four maximally entangled two-qubit states. "
        "The most common, |Φ+⟩ = (|00⟩ + |11⟩)/√2, is made with H on q0 then CNOT(q0→q1). "
        "Measuring always gives perfectly correlated outcomes: both 0 or both 1, never mixed."
    ),
    "cnot": (
        "The CNOT (Controlled-NOT) gate flips the target qubit ONLY when the control qubit is |1⟩. "
        "It is the key two-qubit gate used for entanglement and quantum logic. "
        "CNOT|00⟩=|00⟩, CNOT|10⟩=|11⟩, CNOT|01⟩=|01⟩, CNOT|11⟩=|10⟩."
    ),
    "grover": (
        "Grover's algorithm searches an unsorted database of N items in O(√N) steps, "
        "giving a quadratic speedup over classical O(N) brute-force search. "
        "It uses an oracle to mark the target state and a diffuser to amplify its amplitude "
        "through a process called amplitude amplification."
    ),
    "deutsch": (
        "The Deutsch-Jozsa algorithm determines in ONE quantum query whether a Boolean function "
        "is constant (same output always) or balanced (equal 0s and 1s), versus 2^(n-1)+1 "
        "classical queries. It was the first proof that quantum computers can be exponentially "
        "faster for certain problems."
    ),
    "vqe": (
        "VQE (Variational Quantum Eigensolver) finds molecular ground state energies. "
        "It uses a parameterized ansatz circuit, measures the energy expectation ⟨H⟩, "
        "and a classical optimizer tunes the parameters until ⟨H⟩ is minimized. "
        "This makes it suitable for near-term quantum hardware for chemistry simulations."
    ),
    "qaoa": (
        "QAOA (Quantum Approximate Optimization Algorithm) solves combinatorial problems "
        "like MAXCUT. It alternates cost unitaries (encoding the problem) and mixer unitaries, "
        "with parameters optimized classically. More layers (higher p) give better approximations."
    ),
}


def _find_mock_answer(question: str) -> str:
    q = question.lower()
    for keyword, answer in MOCK_ANSWERS.items():
        if keyword in q:
            return answer
    return (
        "I'm running in mock mode without a Gemini API key. "
        "To enable real AI answers, add your GEMINI_API_KEY to the backend .env file. "
        "Get a free key at https://aistudio.google.com/\n\n"
        f"Your question was: '{question}'\n"
        "Try asking about: superposition, entanglement, qubits, Hadamard gate, "
        "Bell state, CNOT, Grover's algorithm, Deutsch-Jozsa, VQE, or QAOA."
    )


class GeminiTutor:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except ImportError:
                pass

    async def explain(self, question: str, context: str = "", mode: str = "beginner") -> str:
        if not self.client:
            return _find_mock_answer(question)
        try:
            from google import genai
            prompt_template = BEGINNER_EXPLAIN_PROMPT if mode == "beginner" else CONCEPT_DEEP_PROMPT
            full_prompt = prompt_template.format(question=question, context=context)
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=full_prompt,
                config=genai.types.GenerateContentConfig(temperature=0.3),
            )
            return response.text
        except Exception as e:
            return f"AI tutor unavailable: {str(e)}. {_find_mock_answer(question)}"

    async def debug_circuit(self, circuit_json: str, error_msg: str) -> str:
        if not self.client:
            return (
                f"Mock debug mode. Error: {error_msg}\n"
                "Common fixes:\n"
                "• CNOT requires both a control and target qubit\n"
                "• All circuits need at least one measurement\n"
                "• Gates cannot be placed after measurements\n"
                "• CNOT control and target must be different qubits"
            )
        try:
            from google import genai
            from .prompts import DEBUG_CIRCUIT_PROMPT
            prompt = DEBUG_CIRCUIT_PROMPT.format(circuit=circuit_json, error=error_msg)
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=genai.types.GenerateContentConfig(temperature=0.3),
            )
            return response.text
        except Exception as e:
            return f"Debug unavailable: {str(e)}"

    async def generate_code(self, description: str) -> str:
        if not self.client:
            return (
                "# Mock code generation — add GEMINI_API_KEY for real AI generation\n"
                "from qiskit import QuantumCircuit\n"
                "from qiskit_aer import AerSimulator\n"
                "from qiskit import transpile\n\n"
                "# Create a Bell state circuit\n"
                "qc = QuantumCircuit(2, 2)\n"
                "qc.h(0)       # Hadamard on qubit 0\n"
                "qc.cx(0, 1)   # CNOT: control=0, target=1\n"
                "qc.measure([0, 1], [0, 1])\n\n"
                "# Run simulation\n"
                "simulator = AerSimulator()\n"
                "job = simulator.run(transpile(qc, simulator), shots=1024)\n"
                "result = job.result()\n"
                "print(result.get_counts())\n"
            )
        try:
            from google import genai
            from .prompts import CODE_GENERATE_PROMPT
            prompt = CODE_GENERATE_PROMPT.format(description=description)
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=genai.types.GenerateContentConfig(temperature=0.3),
            )
            return response.text
        except Exception as e:
            return f"# Code generation error: {str(e)}"

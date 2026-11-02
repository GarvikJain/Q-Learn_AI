import json
from sqlalchemy.future import select
from app.core.database import AsyncSessionLocal
from app.models.module import Module
from app.models.quiz import Quiz, Question
from app.models.user import User
from app.core.security import hash_password

MODULES_DATA = [
    {
        "slug": "qubit-basics",
        "title": "Qubit Basics",
        "description": "Understand the fundamental unit of quantum information — the qubit.",
        "order": 1,
        "content": {
            "objectives": [
                "Understand what a qubit is and how it differs from a classical bit",
                "Learn the basis states |0⟩ and |1⟩ using Dirac notation",
                "Understand measurement and probability in quantum systems",
                "Explore physical implementations of qubits"
            ],
            "sections": [
                {
                    "title": "What is a Qubit?",
                    "content": "A qubit (quantum bit) is the fundamental unit of quantum information. Unlike a classical bit which can only be 0 or 1, a qubit can exist in a superposition of both states simultaneously. Think of it like a coin spinning in the air — it is both heads and tails until it lands (is measured). This property makes quantum computers exponentially more powerful for certain types of problems."
                },
                {
                    "title": "Dirac Notation: |0⟩ and |1⟩",
                    "content": "We write qubit states using Dirac (bra-ket) notation. |0⟩ is the 'ground' state (analogous to classical 0), and |1⟩ is the 'excited' state (analogous to classical 1). A general qubit state is written as: |ψ⟩ = α|0⟩ + β|1⟩, where α and β are complex numbers called amplitudes, and the constraint |α|² + |β|² = 1 ensures probabilities sum to 1."
                },
                {
                    "title": "Measurement and Probability",
                    "content": "When you measure a qubit, it 'collapses' to either |0⟩ or |1⟩. The probability of measuring |0⟩ is |α|² and |1⟩ is |β|². For example, if α = β = 1/√2, there is a 50% chance of measuring 0 and 50% chance of measuring 1. This irreversible collapse is one of the most counter-intuitive aspects of quantum mechanics — but it is also what makes quantum algorithms work."
                },
                {
                    "title": "Physical Implementations",
                    "content": "Qubits can be realized using many physical systems: Superconducting circuits (used by IBM and Google) — loops of superconducting wire cooled to near absolute zero. Trapped ions (IonQ) — individual atoms held in place by electromagnetic fields. Photons (PsiQuantum) — single particles of light. Electron spin (Intel) — the spin state of individual electrons in silicon. Each implementation has trade-offs in coherence time (how long the qubit stays quantum), gate speed, and error rates."
                },
                {
                    "title": "The X Gate: Quantum NOT",
                    "content": "The simplest quantum gate is the X gate (Pauli-X), which is the quantum equivalent of a classical NOT gate. It flips |0⟩ to |1⟩ and |1⟩ to |0⟩. Try the example circuit below: it applies an X gate to qubit q₀ (starting in |0⟩) and measures. The result should always be |1⟩ (100% probability of measuring 1)."
                }
            ],
            "key_terms": ["qubit", "superposition", "basis state", "amplitude", "measurement", "Dirac notation", "wavefunction collapse", "coherence time"],
            "circuit_example": {
                "num_qubits": 1,
                "gates": [
                    {"type": "X", "targets": [0], "step": 0},
                    {"type": "M", "targets": [0], "step": 1}
                ]
            },
            "summary": "A qubit is the quantum analog of a classical bit, capable of existing in superposition of |0⟩ and |1⟩ states simultaneously. Measurement forces it to collapse to one state with probabilities determined by the amplitude squared."
        },
        "quiz_questions": [
            {
                "question_text": "A qubit has state |ψ⟩ = (1/√2)|0⟩ + (1/√2)|1⟩. What is the probability of measuring |0⟩?",
                "options": ["25%", "50%", "75%", "100%"],
                "correct_answer": "50%",
                "explanation": "The probability is |α|² = |1/√2|² = 1/2 = 50%."
            },
            {
                "question_text": "Which notation do we use to represent qubit states in quantum computing?",
                "options": ["Boolean notation", "Dirac (bra-ket) notation", "Binary notation", "Hexadecimal notation"],
                "correct_answer": "Dirac (bra-ket) notation",
                "explanation": "Dirac notation uses |0⟩ and |1⟩ (called ket vectors) to represent quantum states."
            },
            {
                "question_text": "What does the X gate do to a qubit in state |0⟩?",
                "options": ["Keeps it in |0⟩", "Puts it in superposition", "Flips it to |1⟩", "Destroys the qubit"],
                "correct_answer": "Flips it to |1⟩",
                "explanation": "The X gate is the quantum NOT gate — it flips |0⟩ → |1⟩ and |1⟩ → |0⟩."
            },
            {
                "question_text": "What happens when you measure a qubit that is in superposition?",
                "options": ["It stays in superposition", "It collapses to either |0⟩ or |1⟩", "It always becomes |0⟩", "It disappears"],
                "correct_answer": "It collapses to either |0⟩ or |1⟩",
                "explanation": "Measurement causes wavefunction collapse — the qubit picks a definite state with probabilities given by |α|² and |β|²."
            },
            {
                "question_text": "For a valid qubit state |ψ⟩ = α|0⟩ + β|1⟩, which constraint must hold?",
                "options": ["α + β = 1", "|α|² + |β|² = 1", "α = β", "|α| = |β| = 0.5"],
                "correct_answer": "|α|² + |β|² = 1",
                "explanation": "The normalization condition |α|² + |β|² = 1 ensures total probability equals 1."
            }
        ]
    },
    {
        "slug": "superposition",
        "title": "Superposition & The H Gate",
        "description": "Master the Hadamard gate and the concept of quantum superposition.",
        "order": 2,
        "content": {
            "objectives": [
                "Understand quantum superposition intuitively and mathematically",
                "Learn how the Hadamard (H) gate creates superposition",
                "Interpret measurement results of superposed qubits",
                "Understand the Bloch sphere representation"
            ],
            "sections": [
                {
                    "title": "What is Superposition?",
                    "content": "Superposition is the ability of a quantum system to exist in multiple states simultaneously until measured. Imagine a coin spinning on a table — while spinning it is simultaneously 'heads' and 'tails'. Only when it falls (is observed/measured) does it become one or the other. Superposition allows quantum computers to explore many possibilities simultaneously, giving them exponential parallelism for certain problems."
                },
                {
                    "title": "The Hadamard Gate",
                    "content": "The Hadamard (H) gate is one of the most important quantum gates. It transforms |0⟩ into an equal superposition: H|0⟩ = (|0⟩ + |1⟩)/√2 ≈ |+⟩. And H|1⟩ = (|0⟩ − |1⟩)/√2 ≈ |−⟩. Notice the signs: |+⟩ and |−⟩ differ only in the phase of the |1⟩ amplitude. This phase difference is crucial for quantum interference in algorithms."
                },
                {
                    "title": "Mathematical Representation",
                    "content": "The H gate is represented by the matrix: H = (1/√2) × [[1, 1], [1, -1]]. When applied to |0⟩ = [1, 0]ᵀ: H|0⟩ = (1/√2)[1, 1]ᵀ = (1/√2)(|0⟩ + |1⟩). The probability of measuring 0 is (1/√2)² = 0.5 (50%), and same for 1. If you apply H twice, you get back to the original state: H² = I (identity)."
                },
                {
                    "title": "The Bloch Sphere",
                    "content": "The Bloch sphere is a geometrical representation of a single qubit's state. The north pole represents |0⟩, the south pole |1⟩. The equator represents equal superpositions. |+⟩ = (|0⟩+|1⟩)/√2 is on the +X axis, |−⟩ on the −X axis. After applying H to |0⟩, the state moves from the north pole to the +X axis of the Bloch sphere."
                },
                {
                    "title": "Measurement Results",
                    "content": "When you run the H gate circuit many times (shots), you'll see approximately 50% |0⟩ and 50% |1⟩ results. This is NOT because the qubit randomly picks a side — it genuinely is in both states simultaneously before measurement. The randomness is fundamental (not due to ignorance of a hidden state), as proven by Bell's theorem and experiments."
                }
            ],
            "key_terms": ["superposition", "Hadamard gate", "H gate", "Bloch sphere", "quantum interference", "measurement", "|+⟩ state", "|−⟩ state"],
            "circuit_example": {
                "num_qubits": 1,
                "gates": [
                    {"type": "H", "targets": [0], "step": 0},
                    {"type": "M", "targets": [0], "step": 1}
                ]
            },
            "summary": "The Hadamard gate creates equal superposition from basis states, placing a qubit on the equator of the Bloch sphere. Measuring a superposed qubit gives 50/50 outcomes with fundamental randomness."
        },
        "quiz_questions": [
            {
                "question_text": "What gate creates an equal superposition from |0⟩?",
                "options": ["X gate", "H (Hadamard) gate", "Z gate", "CNOT gate"],
                "correct_answer": "H (Hadamard) gate",
                "explanation": "H|0⟩ = (|0⟩ + |1⟩)/√2, an equal superposition of |0⟩ and |1⟩."
            },
            {
                "question_text": "What is H|0⟩?",
                "options": ["(|0⟩ + |1⟩)/√2", "(|0⟩ − |1⟩)/√2", "|1⟩", "|0⟩"],
                "correct_answer": "(|0⟩ + |1⟩)/√2",
                "explanation": "Applying H to |0⟩ gives the |+⟩ state = (|0⟩ + |1⟩)/√2."
            },
            {
                "question_text": "Where does the |0⟩ state appear on the Bloch sphere?",
                "options": ["South pole", "Equator", "North pole", "X-axis"],
                "correct_answer": "North pole",
                "explanation": "|0⟩ is the north pole of the Bloch sphere by convention."
            },
            {
                "question_text": "If you apply H twice to a qubit, what do you get?",
                "options": ["|+⟩ state", "Random state", "Original state (H² = I)", "|1⟩ state"],
                "correct_answer": "Original state (H² = I)",
                "explanation": "H is its own inverse: H² = I (identity). Applying H twice returns to the starting state."
            },
            {
                "question_text": "Running H|0⟩ 1000 times, approximately how many times will you measure |0⟩?",
                "options": ["Always 0", "Approximately 500", "Approximately 750", "Always 1000"],
                "correct_answer": "Approximately 500",
                "explanation": "H creates equal superposition so each measurement gives 0 or 1 with 50% probability each."
            }
        ]
    },
    {
        "slug": "entanglement",
        "title": "Entanglement & Bell States",
        "description": "Explore quantum entanglement and learn to create Bell states using H and CNOT gates.",
        "order": 3,
        "content": {
            "objectives": [
                "Understand quantum entanglement and why it is surprising",
                "Learn to create Bell states using H + CNOT circuit",
                "Analyze measurement correlations of entangled qubits",
                "Understand the four Bell states"
            ],
            "sections": [
                {
                    "title": "What is Entanglement?",
                    "content": "Quantum entanglement occurs when two or more qubits become correlated in such a way that the state of one cannot be described independently of the others. Einstein called it 'spooky action at a distance'. If two qubits are entangled and you measure one, you instantly know the state of the other — regardless of the distance between them. This correlation is stronger than any classical correlation and cannot be explained by shared hidden variables (Bell's theorem, 1964)."
                },
                {
                    "title": "Creating the Bell State",
                    "content": "The simplest entangled state is the Bell state |Φ+⟩. To create it: Start with two qubits in |00⟩. Apply H gate to qubit 0: creates (|0⟩ + |1⟩)/√2 ⊗ |0⟩ = (|00⟩ + |10⟩)/√2. Apply CNOT with q0 as control, q1 as target: |00⟩ → |00⟩ and |10⟩ → |11⟩. Result: |Φ+⟩ = (|00⟩ + |11⟩)/√2. This two-qubit state CANNOT be written as a product of two single-qubit states — it is entangled!"
                },
                {
                    "title": "Measurement Correlations",
                    "content": "When you measure the Bell state |Φ+⟩, you always get either |00⟩ or |11⟩ — never |01⟩ or |10⟩. This is perfect correlation: if q0 is measured as 0, q1 must also be 0, and vice versa. Run the Bell state circuit with 1024 shots — you should see approximately 512 counts for '00' and 512 for '11'. The '01' and '10' outcomes should be zero (or very near zero due to noise)."
                },
                {
                    "title": "The Four Bell States",
                    "content": "There are four maximally entangled two-qubit Bell states: |Φ+⟩ = (|00⟩ + |11⟩)/√2, |Φ−⟩ = (|00⟩ − |11⟩)/√2, |Ψ+⟩ = (|01⟩ + |10⟩)/√2, |Ψ−⟩ = (|01⟩ − |10⟩)/√2. They form an orthonormal basis for the two-qubit Hilbert space. Bell states are used in quantum teleportation, superdense coding, and quantum key distribution (QKD)."
                },
                {
                    "title": "Applications of Entanglement",
                    "content": "Quantum entanglement is a key resource for many quantum technologies: Quantum teleportation: transfer a quantum state using a Bell pair + classical communication. Superdense coding: send 2 classical bits using 1 qubit + 1 shared Bell pair. Quantum key distribution (BB84, E91): secure communication guaranteed by quantum mechanics. Quantum error correction: logical qubits protected by entangled ancilla qubits."
                }
            ],
            "key_terms": ["entanglement", "Bell state", "CNOT gate", "correlation", "quantum teleportation", "superdense coding", "EPR pair", "separability"],
            "circuit_example": {
                "num_qubits": 2,
                "gates": [
                    {"type": "H", "targets": [0], "step": 0},
                    {"type": "CNOT", "control": 0, "targets": [1], "step": 1},
                    {"type": "M", "targets": [0, 1], "step": 2}
                ]
            },
            "summary": "Entanglement creates non-separable multi-qubit states with perfect measurement correlations. The Bell state (|00⟩+|11⟩)/√2 is created with H+CNOT and always yields correlated measurement outcomes."
        },
        "quiz_questions": [
            {
                "question_text": "Bell states are maximally ___?",
                "options": ["entangled", "superposed", "measured", "classical"],
                "correct_answer": "entangled",
                "explanation": "Bell states are the four maximally entangled two-qubit states."
            },
            {
                "question_text": "What is the circuit to create the |Φ+⟩ Bell state from |00⟩?",
                "options": ["X gate then CNOT", "H gate then CNOT", "CNOT then H gate", "H gate then H gate"],
                "correct_answer": "H gate then CNOT",
                "explanation": "Apply H to q0 (creates superposition), then CNOT (entangles q0 and q1)."
            },
            {
                "question_text": "When measuring |Φ+⟩ = (|00⟩+|11⟩)/√2, which outcomes can appear?",
                "options": ["Only |00⟩", "Only |11⟩", "|00⟩ and |11⟩ with equal probability", "All four: |00⟩, |01⟩, |10⟩, |11⟩"],
                "correct_answer": "|00⟩ and |11⟩ with equal probability",
                "explanation": "The amplitudes for |01⟩ and |10⟩ are zero, so only |00⟩ or |11⟩ appear, each with 50% probability."
            },
            {
                "question_text": "How many maximally entangled Bell states exist for two qubits?",
                "options": ["2", "3", "4", "8"],
                "correct_answer": "4",
                "explanation": "There are 4 Bell states: |Φ+⟩, |Φ−⟩, |Ψ+⟩, |Ψ−⟩."
            },
            {
                "question_text": "What does the CNOT gate do?",
                "options": ["Flips the control qubit", "Flips the target qubit if control is |1⟩", "Applies H to both qubits", "Measures both qubits"],
                "correct_answer": "Flips the target qubit if control is |1⟩",
                "explanation": "CNOT (Controlled-NOT) flips the target qubit only when the control qubit is |1⟩."
            }
        ]
    },
    {
        "slug": "quantum-gates",
        "title": "Single-Qubit Gates",
        "description": "Study the Pauli gates, phase gates, and their matrix representations.",
        "order": 4,
        "content": {
            "objectives": [
                "Understand the Pauli-X, Y, Z gates and their effects",
                "Learn about S and T phase gates",
                "Interpret gates as rotations on the Bloch sphere",
                "Compose gates to build circuits"
            ],
            "sections": [
                {
                    "title": "The Pauli Gates",
                    "content": "The three Pauli gates are fundamental: X gate (Pauli-X): flips |0⟩↔|1⟩. Matrix: [[0,1],[1,0]]. Equivalent to 180° rotation around X-axis on Bloch sphere. Y gate (Pauli-Y): X-rotation + phase flip. Matrix: [[0,-i],[i,0]]. Z gate (Pauli-Z): phase flip — leaves |0⟩ unchanged, multiplies |1⟩ by -1. Matrix: [[1,0],[0,-1]]. Equivalent to 180° rotation around Z-axis."
                },
                {
                    "title": "Phase Gates: S and T",
                    "content": "Phase gates rotate around the Z-axis by smaller angles: S gate: Z-axis rotation by 90° (π/2). S|0⟩ = |0⟩, S|1⟩ = i|1⟩. S² = Z. T gate: Z-axis rotation by 45° (π/4). T|1⟩ = e^(iπ/4)|1⟩. T² = S. Phase gates are crucial for creating non-trivial quantum states and are building blocks of fault-tolerant quantum circuits."
                },
                {
                    "title": "Gates as Rotations",
                    "content": "Every single-qubit gate corresponds to a rotation of the Bloch sphere. The Bloch sphere is a unit sphere where: Rotations around X-axis: X gate (180°), Rx(θ) in general. Rotations around Y-axis: Y gate (180°), Ry(θ). Rotations around Z-axis: Z gate (180°), S (90°), T (45°). This geometric view makes it intuitive to understand gate composition and interference."
                },
                {
                    "title": "Gate Composition",
                    "content": "Gates are composed by matrix multiplication. HZH = X, meaning an H-Z-H sequence acts like an X gate. This is useful for circuit optimization. HXH = Z. Key identities: X² = Y² = Z² = I (each Pauli squared gives identity). HH = I. H transforms between X and Z bases, explaining why HZH = X. Gate composition is the foundation of quantum algorithm design."
                }
            ],
            "key_terms": ["Pauli gates", "X gate", "Y gate", "Z gate", "S gate", "T gate", "phase gate", "Bloch sphere rotation", "gate composition"],
            "circuit_example": {
                "num_qubits": 1,
                "gates": [
                    {"type": "H", "targets": [0], "step": 0},
                    {"type": "Z", "targets": [0], "step": 1},
                    {"type": "H", "targets": [0], "step": 2},
                    {"type": "M", "targets": [0], "step": 3}
                ]
            },
            "summary": "Single-qubit gates are unitary matrices that rotate the Bloch sphere. Pauli gates (X, Y, Z) perform 180° rotations; phase gates (S, T) perform smaller rotations around the Z-axis."
        },
        "quiz_questions": [
            {
                "question_text": "What does the Z gate do to |1⟩?",
                "options": ["Flips it to |0⟩", "Adds a phase of -1", "Creates superposition", "Does nothing"],
                "correct_answer": "Adds a phase of -1",
                "explanation": "Z|1⟩ = -|1⟩. The Z gate multiplies the |1⟩ component by -1 (phase flip)."
            },
            {
                "question_text": "What is the angle of rotation for the T gate around the Z-axis?",
                "options": ["180°", "90°", "45°", "30°"],
                "correct_answer": "45°",
                "explanation": "T gate rotates by π/4 = 45° around the Z-axis. Two T gates equal one S gate (90°)."
            },
            {
                "question_text": "Which identity is correct?",
                "options": ["HZH = Z", "HZH = X", "HXH = X", "HH = Z"],
                "correct_answer": "HZH = X",
                "explanation": "HZH = X is a fundamental gate identity. H converts between X and Z bases."
            },
            {
                "question_text": "What does X² equal?",
                "options": ["X", "Z", "H", "I (identity)"],
                "correct_answer": "I (identity)",
                "explanation": "All Pauli gates squared equal the identity: X² = Y² = Z² = I."
            }
        ]
    },
    {
        "slug": "quantum-circuits",
        "title": "Multi-Qubit Circuits",
        "description": "Learn to design and analyze multi-qubit quantum circuits.",
        "order": 5,
        "content": {
            "objectives": [
                "Understand circuit depth and gate ordering",
                "Learn SWAP and Toffoli gates",
                "Design circuits for quantum algorithms",
                "Understand circuit optimization principles"
            ],
            "sections": [
                {
                    "title": "Circuit Depth and Width",
                    "content": "A quantum circuit has two key dimensions: Width (# qubits): determines the problem size. Depth (# time steps): determines how long the computation takes. Gates in different time steps run sequentially; gates on different qubits in the same step run in parallel. Minimizing depth is critical because qubits decohere (lose their quantum properties) over time. Circuit depth is analogous to runtime complexity."
                },
                {
                    "title": "The SWAP Gate",
                    "content": "The SWAP gate exchanges the states of two qubits: SWAP|00⟩=|00⟩, SWAP|01⟩=|10⟩, SWAP|10⟩=|01⟩, SWAP|11⟩=|11⟩. It can be decomposed into three CNOT gates: CNOT(a,b), CNOT(b,a), CNOT(a,b). SWAP is used in quantum algorithms to move data between qubits and in quantum error correction. On near-term devices, SWAP operations are expensive because not all qubit pairs are connected."
                },
                {
                    "title": "The Toffoli Gate (CCX)",
                    "content": "The Toffoli gate is a controlled-controlled-NOT gate: it flips the target qubit only when BOTH control qubits are |1⟩. CCX|110⟩ = |111⟩, CCX|111⟩ = |110⟩. The Toffoli gate is universal for classical reversible computing, and combined with H gates it is universal for quantum computing. It is used to implement quantum arithmetic and oracle functions."
                },
                {
                    "title": "Circuit Optimization",
                    "content": "Reducing circuit depth and gate count is essential for NISQ (Noisy Intermediate-Scale Quantum) devices. Key optimization techniques: Gate cancellation: X followed by X cancels. Commutation: some gates can be reordered without changing the result. Gate decomposition: complex gates can be expressed as sequences of simpler gates. Circuit compilers (like Qiskit's transpiler) perform these optimizations automatically."
                }
            ],
            "key_terms": ["circuit depth", "circuit width", "SWAP gate", "Toffoli gate", "CCX gate", "NISQ", "gate cancellation", "transpilation"],
            "circuit_example": {
                "num_qubits": 3,
                "gates": [
                    {"type": "H", "targets": [0], "step": 0},
                    {"type": "H", "targets": [1], "step": 0},
                    {"type": "CNOT", "control": 0, "targets": [2], "step": 1},
                    {"type": "CNOT", "control": 1, "targets": [2], "step": 2},
                    {"type": "M", "targets": [0, 1, 2], "step": 3}
                ]
            },
            "summary": "Multi-qubit circuits combine gates across qubits. Circuit depth (sequential steps) must be minimized to reduce decoherence. SWAP and Toffoli gates enable complex multi-qubit operations."
        },
        "quiz_questions": [
            {
                "question_text": "What does 'circuit depth' measure?",
                "options": ["Number of qubits", "Number of sequential time steps", "Number of gates", "Number of measurements"],
                "correct_answer": "Number of sequential time steps",
                "explanation": "Circuit depth measures the number of sequential layers (time steps) of gates, analogous to the runtime of a computation."
            },
            {
                "question_text": "How many CNOT gates are needed to implement a SWAP gate?",
                "options": ["1", "2", "3", "4"],
                "correct_answer": "3",
                "explanation": "SWAP = CNOT(a,b) × CNOT(b,a) × CNOT(a,b) — three CNOT gates."
            },
            {
                "question_text": "The Toffoli gate flips the target qubit when...?",
                "options": ["Control qubit 1 is |1⟩", "Either control is |1⟩", "Both controls are |1⟩", "Target is |0⟩"],
                "correct_answer": "Both controls are |1⟩",
                "explanation": "Toffoli (CCX) is a controlled-controlled-NOT: both control qubits must be |1⟩ to flip the target."
            }
        ]
    },
    {
        "slug": "deutsch-jozsa",
        "title": "Deutsch-Jozsa Algorithm",
        "description": "Learn the first quantum algorithm to demonstrate quantum speedup over classical computing.",
        "order": 6,
        "content": {
            "objectives": [
                "Understand the oracle model of quantum computation",
                "Learn the Deutsch-Jozsa problem and its classical complexity",
                "Understand how the algorithm achieves exponential speedup",
                "Build a Deutsch-Jozsa circuit for a 2-qubit function"
            ],
            "sections": [
                {
                    "title": "The Problem",
                    "content": "Given a function f: {0,1}ⁿ → {0,1}, determine if f is constant (same output for all inputs) or balanced (outputs 0 for exactly half of inputs, 1 for the other half). Classical algorithm: worst case requires 2^(n-1)+1 queries. Quantum algorithm: always determines the answer in exactly 1 query! This was the first demonstration of quantum speedup, published by David Deutsch and Richard Jozsa in 1992."
                },
                {
                    "title": "The Oracle",
                    "content": "A quantum oracle is a black-box unitary operation Uf that computes: Uf|x⟩|y⟩ = |x⟩|y ⊕ f(x)⟩. The oracle encodes f as a quantum gate. For constant f=0: Uf does nothing (identity). For constant f=1: Uf flips the ancilla qubit. For balanced f: Uf flips the ancilla for half the inputs. The algorithm uses quantum parallelism (applying Uf to a superposition of all inputs at once) to distinguish these cases."
                },
                {
                    "title": "The Algorithm",
                    "content": "Step 1: Start with n+1 qubits: |0...0⟩|1⟩. Step 2: Apply H to all qubits (create superposition). Step 3: Apply oracle Uf. Step 4: Apply H to the first n qubits. Step 5: Measure the first n qubits. Result: if all zeros → f is constant. If any non-zero → f is balanced. The algorithm cleverly uses quantum interference to amplify the constant-case answer and cancel the balanced-case answer."
                }
            ],
            "key_terms": ["oracle", "quantum speedup", "constant function", "balanced function", "quantum interference", "quantum parallelism"],
            "circuit_example": {
                "num_qubits": 2,
                "gates": [
                    {"type": "H", "targets": [0], "step": 0},
                    {"type": "H", "targets": [1], "step": 0},
                    {"type": "CNOT", "control": 0, "targets": [1], "step": 1},
                    {"type": "H", "targets": [0], "step": 2},
                    {"type": "M", "targets": [0], "step": 3}
                ]
            },
            "summary": "Deutsch-Jozsa uses quantum superposition and interference to determine if a function is constant or balanced in ONE query vs. 2^(n-1)+1 classical queries — the first proven quantum speedup."
        },
        "quiz_questions": [
            {
                "question_text": "What is the Deutsch-Jozsa algorithm used to determine?",
                "options": ["Whether a function is constant or balanced", "The prime factors of a number", "The shortest path in a graph", "Whether a number is in a list"],
                "correct_answer": "Whether a function is constant or balanced",
                "explanation": "Deutsch-Jozsa distinguishes constant functions (same output always) from balanced functions (equal 0s and 1s)."
            },
            {
                "question_text": "How many oracle queries does Deutsch-Jozsa use?",
                "options": ["2^n", "n", "1", "2^(n-1)+1"],
                "correct_answer": "1",
                "explanation": "The quantum algorithm always solves the problem with exactly 1 oracle query, vs. 2^(n-1)+1 classical queries."
            },
            {
                "question_text": "In Deutsch-Jozsa, if all measured qubits are 0, what does it mean?",
                "options": ["Function is balanced", "Function is constant", "Measurement failed", "Oracle is incorrect"],
                "correct_answer": "Function is constant",
                "explanation": "Measuring all zeros after the algorithm means the function is constant; any non-zero result means balanced."
            }
        ]
    },
    {
        "slug": "grovers-algorithm",
        "title": "Grover's Search Algorithm",
        "description": "Understand amplitude amplification and quadratic speedup for unstructured search.",
        "order": 7,
        "content": {
            "objectives": [
                "Understand the unstructured search problem",
                "Learn amplitude amplification as a technique",
                "Understand the oracle and diffuser components",
                "Analyze the O(√N) complexity advantage"
            ],
            "sections": [
                {
                    "title": "The Search Problem",
                    "content": "Given an unsorted database of N items, find the one that satisfies a given property (the 'marked' item). Classical brute-force search: O(N) queries average. Grover's algorithm: O(√N) queries — a quadratic speedup. For 1 million items: classical needs ~500,000 queries, Grover needs ~1,000 queries. While not exponential speedup, it applies to ANY unstructured search problem, making it broadly applicable."
                },
                {
                    "title": "The Oracle",
                    "content": "Grover's oracle marks the target state by flipping its phase: Uf|x⟩ = -|x⟩ if x is the target, |x⟩ otherwise. This is a phase kickback trick. After the oracle, the target state has amplitude −1/√N while all others remain +1/√N. A single oracle call does not tell us which state is marked — we need amplitude amplification to find it."
                },
                {
                    "title": "Amplitude Amplification",
                    "content": "The Grover diffuser inverts all amplitudes about their mean. Starting with uniform superposition: apply oracle (marks target with − phase), apply diffuser (amplifies marked state, reduces others). Repeat ~π√N/4 times. After enough iterations, the marked state has amplitude ≈ 1 and all others ≈ 0, so measuring gives the target with high probability. Running too many iterations 'overshoots' — the amplitudes oscillate like a rotation."
                },
                {
                    "title": "The Diffuser Circuit",
                    "content": "The diffuser (inversion about mean) can be implemented as: Apply H to all qubits. Apply X to all qubits. Apply a multi-controlled Z gate (phase -1 on |00...0⟩). Apply X to all qubits. Apply H to all qubits. The combination H-X-CZ-X-H implements the 2|s⟩⟨s|−I operator where |s⟩ is the uniform superposition."
                }
            ],
            "key_terms": ["amplitude amplification", "Grover oracle", "diffuser", "phase kickback", "unstructured search", "quadratic speedup", "√N complexity"],
            "circuit_example": {
                "num_qubits": 2,
                "gates": [
                    {"type": "H", "targets": [0], "step": 0},
                    {"type": "H", "targets": [1], "step": 0},
                    {"type": "X", "targets": [0], "step": 1},
                    {"type": "X", "targets": [1], "step": 1},
                    {"type": "H", "targets": [1], "step": 2},
                    {"type": "CNOT", "control": 0, "targets": [1], "step": 3},
                    {"type": "H", "targets": [1], "step": 4},
                    {"type": "X", "targets": [0], "step": 5},
                    {"type": "X", "targets": [1], "step": 5},
                    {"type": "H", "targets": [0], "step": 6},
                    {"type": "H", "targets": [1], "step": 6},
                    {"type": "M", "targets": [0, 1], "step": 7}
                ]
            },
            "summary": "Grover's algorithm uses amplitude amplification (oracle + diffuser) to find a marked item in O(√N) queries, providing quadratic speedup over classical O(N) brute-force search."
        },
        "quiz_questions": [
            {
                "question_text": "What is the time complexity of Grover's algorithm?",
                "options": ["O(N)", "O(log N)", "O(√N)", "O(N²)"],
                "correct_answer": "O(√N)",
                "explanation": "Grover's algorithm needs approximately π√N/4 oracle calls — a quadratic speedup over classical O(N)."
            },
            {
                "question_text": "What does Grover's oracle do to the target state?",
                "options": ["Flips its bit value", "Marks it with a −1 phase", "Removes it from superposition", "Measures it"],
                "correct_answer": "Marks it with a −1 phase",
                "explanation": "The oracle applies a phase flip (−1) to the target state, marking it without revealing which state it is."
            },
            {
                "question_text": "What is the Grover diffuser also called?",
                "options": ["Phase oracle", "Inversion about the mean", "Quantum Fourier Transform", "Hadamard diffusion"],
                "correct_answer": "Inversion about the mean",
                "explanation": "The diffuser reflects all amplitudes about their mean, amplifying the marked state and reducing others."
            }
        ]
    },
    {
        "slug": "qaoa-intro",
        "title": "QAOA Introduction",
        "description": "Introduction to the Quantum Approximate Optimization Algorithm for combinatorial problems.",
        "order": 8,
        "content": {
            "objectives": [
                "Understand variational quantum algorithms",
                "Learn the QAOA structure: cost and mixer Hamiltonians",
                "Understand the MAXCUT problem as an example",
                "Appreciate the role of classical optimization in QAOA"
            ],
            "sections": [
                {
                    "title": "Variational Quantum Algorithms",
                    "content": "Variational Quantum Algorithms (VQAs) use a classical optimizer to tune the parameters of a quantum circuit (called the ansatz). The quantum circuit prepares a parameterized state; measurements estimate a cost function; the classical optimizer updates parameters to minimize cost. This quantum-classical hybrid approach is designed for near-term quantum hardware."
                },
                {
                    "title": "QAOA Overview",
                    "content": "QAOA (Quantum Approximate Optimization Algorithm, Farhi et al. 2014) is a VQA for combinatorial optimization. It has p layers, each containing: Cost unitary: UC(γ) = e^(-iγHC) encoding the problem Hamiltonian HC. Mixer unitary: UM(β) = e^(-iβHM) typically using Rx rotations. Parameters γ = (γ1,...,γp) and β = (β1,...,βp) are optimized classically. As p→∞, QAOA approximates the exact solution."
                },
                {
                    "title": "MAXCUT Example",
                    "content": "MAXCUT asks: given a graph G, partition vertices into two sets to maximize the number of edges between the sets. This is NP-hard classically. QAOA maps MAXCUT to a Hamiltonian: HC = Σ(i,j)∈E (1 - ZiZj)/2. Each term gives energy 1 if qubits i and j are in different partitions (the edge is 'cut') and 0 otherwise. QAOA maximizes the expected value of HC to find good partitions."
                },
                {
                    "title": "Limitations",
                    "content": "QAOA with fixed depth p gives only an approximation (not guaranteed optimal). Classical solvers often outperform QAOA on current hardware due to noise. The real potential lies in large, fault-tolerant quantum computers where the circuit depth can be large. Research is ongoing to find problem instances where QAOA achieves quantum advantage."
                }
            ],
            "key_terms": ["QAOA", "variational quantum algorithm", "ansatz", "cost Hamiltonian", "mixer Hamiltonian", "MAXCUT", "quantum-classical hybrid", "parameterized circuit"],
            "circuit_example": {
                "num_qubits": 2,
                "gates": [
                    {"type": "H", "targets": [0], "step": 0},
                    {"type": "H", "targets": [1], "step": 0},
                    {"type": "CNOT", "control": 0, "targets": [1], "step": 1},
                    {"type": "Z", "targets": [1], "step": 2},
                    {"type": "CNOT", "control": 0, "targets": [1], "step": 3},
                    {"type": "X", "targets": [0], "step": 4},
                    {"type": "X", "targets": [1], "step": 4},
                    {"type": "M", "targets": [0, 1], "step": 5}
                ]
            },
            "summary": "QAOA is a variational quantum algorithm that uses parameterized circuits (cost + mixer unitaries) optimized by a classical algorithm to solve combinatorial optimization problems like MAXCUT."
        },
        "quiz_questions": [
            {
                "question_text": "What does QAOA stand for?",
                "options": ["Quantum Amplitude Optimization Algorithm", "Quantum Approximate Optimization Algorithm", "Quantum Ansatz Operator Algorithm", "Quantum Adaptive Oracle Algorithm"],
                "correct_answer": "Quantum Approximate Optimization Algorithm",
                "explanation": "QAOA = Quantum Approximate Optimization Algorithm, introduced by Farhi, Goldstone, and Gutmann in 2014."
            },
            {
                "question_text": "What are the two components of each QAOA layer?",
                "options": ["Hadamard + Measurement", "Cost unitary + Mixer unitary", "Oracle + Diffuser", "Preparation + Encoding"],
                "correct_answer": "Cost unitary + Mixer unitary",
                "explanation": "Each QAOA layer has a cost unitary UC(γ) encoding the problem and a mixer unitary UM(β) for exploration."
            },
            {
                "question_text": "In QAOA, who optimizes the circuit parameters?",
                "options": ["The quantum computer", "A classical optimizer", "Random sampling", "The Hadamard gate"],
                "correct_answer": "A classical optimizer",
                "explanation": "QAOA is a hybrid algorithm: the quantum circuit prepares states, and a classical optimizer updates the parameters."
            }
        ]
    },
    {
        "slug": "vqe-intro",
        "title": "VQE Introduction",
        "description": "Learn the Variational Quantum Eigensolver for quantum chemistry and materials simulation.",
        "order": 9,
        "content": {
            "objectives": [
                "Understand the variational principle in quantum mechanics",
                "Learn the VQE algorithm structure",
                "Understand ansatz circuits for molecular simulation",
                "Appreciate VQE's application to quantum chemistry"
            ],
            "sections": [
                {
                    "title": "The Variational Principle",
                    "content": "The variational principle states: for any quantum state |ψ⟩, the expectation value of the Hamiltonian H is always ≥ the ground state energy E₀: ⟨ψ|H|ψ⟩ ≥ E₀. By minimizing ⟨ψ(θ)|H|ψ(θ)⟩ over parameterized states, we approach the ground state energy. VQE uses this principle with a parameterized quantum circuit (ansatz) to find molecular ground state energies."
                },
                {
                    "title": "VQE Algorithm",
                    "content": "Step 1: Choose an ansatz circuit U(θ) with parameters θ = (θ₁,...,θₖ). Step 2: Prepare |ψ(θ)⟩ = U(θ)|0⟩. Step 3: Measure the energy expectation value ⟨H⟩ = ⟨ψ(θ)|H|ψ(θ)⟩. Step 4: Use a classical optimizer (COBYLA, BFGS, ADAM) to update θ to minimize ⟨H⟩. Repeat until convergence. The ansatz is chosen to match the problem structure (chemistry-inspired or hardware-efficient)."
                },
                {
                    "title": "Ansatz Circuits",
                    "content": "The ansatz circuit must balance: Expressibility: can it represent the true ground state? Trainability: can gradients be computed efficiently? Hardware efficiency: matches device connectivity. Common ansätze: Hardware-efficient ansatz: Ry and CNOT layers, easy to implement. UCCSD (Unitary Coupled Cluster): chemistry-inspired, theoretically motivated. RYRZ: alternating Ry and Rz rotations."
                },
                {
                    "title": "Applications",
                    "content": "VQE is designed to simulate quantum systems that are classically intractable: Quantum chemistry: ground state energies of molecules (H₂, LiH, BeH₂, FeMoco). Materials science: band structures, magnetic properties. Drug discovery: protein-ligand binding energies. Finance: portfolio optimization (mapped to Ising Hamiltonian). VQE is considered one of the most promising near-term quantum applications."
                }
            ],
            "key_terms": ["VQE", "variational principle", "ansatz", "Hamiltonian", "ground state energy", "quantum chemistry", "UCCSD", "expectation value"],
            "circuit_example": {
                "num_qubits": 2,
                "gates": [
                    {"type": "H", "targets": [0], "step": 0},
                    {"type": "H", "targets": [1], "step": 0},
                    {"type": "CNOT", "control": 0, "targets": [1], "step": 1},
                    {"type": "Z", "targets": [0], "step": 2},
                    {"type": "Z", "targets": [1], "step": 2},
                    {"type": "M", "targets": [0, 1], "step": 3}
                ]
            },
            "summary": "VQE uses the variational principle to find molecular ground state energies by minimizing ⟨H⟩ over parameterized ansatz circuits, with a classical optimizer tuning the parameters."
        },
        "quiz_questions": [
            {
                "question_text": "What does the variational principle guarantee?",
                "options": ["⟨ψ|H|ψ⟩ ≤ E₀", "⟨ψ|H|ψ⟩ ≥ E₀", "⟨ψ|H|ψ⟩ = E₀", "⟨ψ|H|ψ⟩ = 0"],
                "correct_answer": "⟨ψ|H|ψ⟩ ≥ E₀",
                "explanation": "The variational principle guarantees that any trial state gives energy ≥ ground state energy E₀."
            },
            {
                "question_text": "What is the role of the ansatz in VQE?",
                "options": ["To measure the Hamiltonian", "A parameterized quantum circuit that approximates the ground state", "The classical optimizer", "A type of quantum gate"],
                "correct_answer": "A parameterized quantum circuit that approximates the ground state",
                "explanation": "The ansatz U(θ) is a parameterized circuit whose output state approximates the molecular ground state when optimally tuned."
            },
            {
                "question_text": "What is a primary application of VQE?",
                "options": ["Searching databases", "Breaking encryption", "Simulating molecular ground state energies", "Image recognition"],
                "correct_answer": "Simulating molecular ground state energies",
                "explanation": "VQE is designed for quantum chemistry — computing ground state energies of molecules like H₂ and LiH."
            }
        ]
    }
]


DEMO_USERS = [
    {
        "email": "demo@qlearn.ai",
        "username": "demo",
        "password": "Demo@1234",
        "role": "student",
    },
    {
        "email": "instructor@qlearn.ai",
        "username": "instructor",
        "password": "Teach@1234",
        "role": "instructor",
    },
]


async def seed_demo_users(db):
    for u in DEMO_USERS:
        result = await db.execute(select(User).filter(User.email == u["email"]))
        if result.scalars().first():
            continue
        db.add(
            User(
                email=u["email"],
                username=u["username"],
                hashed_password=hash_password(u["password"]),
                role=u["role"],
            )
        )


async def seed_db():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Module))
        already_seeded = result.scalars().first() is not None

        if not already_seeded:
            for m_data in MODULES_DATA:
                module = Module(
                    slug=m_data["slug"],
                    title=m_data["title"],
                    description=m_data["description"],
                    order_index=m_data["order"],
                    content_json=json.dumps(m_data["content"], ensure_ascii=False),
                )
                db.add(module)
                await db.flush()

                quiz = Quiz(module_id=module.id, title=f"{m_data['title']} — Quiz")
                db.add(quiz)
                await db.flush()

                for q_data in m_data.get("quiz_questions", []):
                    question = Question(
                        quiz_id=quiz.id,
                        question_text=q_data["question_text"],
                        question_type="mcq",
                        options=json.dumps(q_data["options"]),
                        correct_answer=q_data["correct_answer"],
                        explanation=q_data.get("explanation", ""),
                    )
                    db.add(question)

        await seed_demo_users(db)
        await db.commit()

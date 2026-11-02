# QLearnAI ⚛️
## AI-Based Interactive Quantum Algorithm Learning Platform

> An intelligent, web-based quantum computing education platform featuring a drag-and-drop circuit builder, real-time Qiskit simulation, Bloch sphere visualization, AI tutoring (Google Gemini), quizzes, and progress tracking.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 15+ (or Docker)

### Option A — Docker Compose (Recommended)

```bash
# 1. Clone and configure
copy backend\.env.example backend\.env
copy frontend\.env.example frontend\.env
# Edit backend\.env and add your GEMINI_API_KEY (optional — works without it)

# 2. Start all services
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Demo login: `demo@qlearn.ai` / `Demo@1234` (instructor: `instructor@qlearn.ai` / `Teach@1234`)

---

### Option B — Manual Setup (Development)

#### Backend

```powershell
# 1. Create virtual environment
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start PostgreSQL and create database
# (or use: docker run -e POSTGRES_USER=qlearn -e POSTGRES_PASSWORD=qlearn -e POSTGRES_DB=qlearnai -p 5432:5432 postgres:15-alpine)

# 4. Configure environment
copy .env.example .env
# Edit .env with your DATABASE_URL and optionally GEMINI_API_KEY

# 5. Start server (tables + 9 modules seeded automatically on startup)
uvicorn app.main:app --reload --port 8000
```

Demo accounts (seeded on first startup):
- Student: `demo@qlearn.ai` / `Demo@1234`
- Instructor: `instructor@qlearn.ai` / `Teach@1234`


#### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

---

## 📁 Project Structure

```
QLearnAI/
├── backend/                    # FastAPI Python backend
│   ├── app/
│   │   ├── api/routes/         # REST API endpoints
│   │   ├── core/               # Config, DB, Security
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── simulation/         # Qiskit Aer adapter
│   │   ├── ai/                 # Gemini AI tutor
│   │   └── content/            # Lesson seed data
│   ├── tests/                  # Pytest test suite
│   ├── alembic/                # DB migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                   # React + TypeScript SPA
│   ├── src/
│   │   ├── components/         # UI components
│   │   ├── pages/              # Route-level pages
│   │   ├── stores/             # Zustand state
│   │   ├── hooks/              # Custom React hooks
│   │   ├── lib/                # API client, utilities
│   │   └── types/              # TypeScript interfaces
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🎓 Features

### Learning Content (9 Modules)
| # | Module | Topics |
|---|---|---|
| 1 | Qubit Basics | Qubits, Dirac notation, measurement, X gate |
| 2 | Superposition & H Gate | Hadamard gate, Bloch sphere, |+⟩ and |−⟩ |
| 3 | Entanglement & Bell States | Bell states, CNOT, EPR pairs |
| 4 | Single-Qubit Gates | Pauli X/Y/Z, S, T, gate composition |
| 5 | Multi-Qubit Circuits | Circuit depth, SWAP, Toffoli, optimization |
| 6 | Deutsch-Jozsa Algorithm | Oracle model, exponential speedup |
| 7 | Grover's Search | Amplitude amplification, O(√N) |
| 8 | QAOA Introduction | Variational circuits, MAXCUT |
| 9 | VQE Introduction | Molecular simulation, ansatz circuits |

### Quantum Circuit Designer
- **Drag-and-drop** visual circuit builder (H, X, Y, Z, S, T, CNOT, SWAP, Toffoli, Measure)
- **Monaco code editor** with Python/Qiskit syntax highlighting
- Up to 5 qubits, 12 time steps
- Real-time validation with descriptive error messages
- Export as JSON, Qiskit Python code, or PNG (circuit toolbar)


### Simulation Engine
- **Qiskit Aer** backend (primary) — shot-based sampling + statevector
- Adapter pattern for future PennyLane and Cirq backends
- Results: measurement counts, probabilities, execution timing
- Supports up to 5-qubit statevector extraction

### Visualization
- 📊 **Probability Histogram** — Recharts bar chart with Dirac notation labels
- 🔵 **Bloch Sphere** — Interactive 3-D Three.js visualization for single-qubit states
- 🔢 **Statevector Table** — Amplitude, phase, and probability per basis state
- ⚡ **Execution Info** — Backend, shots, timing, qubit count

### AI Tutor (Google Gemini)
- Contextual explanations in Beginner / Intermediate / Advanced modes
- "Explain this circuit" context-aware prompting
- Circuit error debugging assistance
- Qiskit code generation from natural language
- Mock mode when no API key is provided

### Assessment & Progress
- Multiple-choice quizzes per module (3-5 questions)
- Automatic grading with explanations
- Per-module progress tracking (not started / in progress / completed)
- Overall progress dashboard with completion %, avg quiz score
- Instructor dashboard with learner analytics

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Create account |
| POST | `/auth/login` | Get JWT token |
| GET | `/auth/me` | Current user profile |
| GET | `/modules` | List all 9 modules |
| GET | `/modules/{slug}` | Module content |
| POST | `/simulate` | Run circuit simulation |
| POST | `/circuits` | Save circuit |
| GET | `/circuits` | User's saved circuits |
| POST | `/ai/explain` | AI concept explanation |
| POST | `/ai/debug` | AI circuit debugging |
| POST | `/ai/generate-code` | AI code generation |
| GET | `/quizzes/{slug}` | Get quiz for module |
| POST | `/quizzes/{slug}/submit` | Submit quiz answers |
| GET | `/progress` | User's progress data |
| GET | `/progress/summary` | Progress summary stats |
| PUT | `/progress/{slug}` | Update module progress |
| GET | `/progress/instructor/learners` | Instructor learner analytics |

Full interactive API docs: http://localhost:8000/docs

### Demo credentials
| Role | Email | Password |
|---|---|---|
| Student | demo@qlearn.ai | Demo@1234 |
| Instructor | instructor@qlearn.ai | Teach@1234 |

---

## 🧪 Running Tests

```powershell
# Backend tests
cd backend
pytest tests/ -v

# Frontend lint check
cd frontend
npm run lint
```

---

## ⚙️ Configuration

### Backend `.env`
```env
DATABASE_URL=postgresql+asyncpg://qlearn:qlearn@localhost:5432/qlearnai
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
GEMINI_API_KEY=           # Optional — enables real AI tutor (get from aistudio.google.com)
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
```

### Frontend `.env`
```env
VITE_API_URL=http://localhost:8000
```

---

## 🗺️ Requirements Traceability

| Requirement | Status | How Verified |
|---|---|---|
| FR-01 Auth | ✅ | JWT login/register, T-01 |
| FR-02 Learning Modules | ✅ | 9 modules seeded, T-02 |
| FR-03 Circuit Builder | ✅ | Drag-and-drop canvas, T-03/T-04 |
| FR-04 Code Editor | ✅ | Monaco editor, Qiskit templates |
| FR-05 Simulation | ✅ | Qiskit Aer, T-05/T-06 |
| FR-06 Visualization | ✅ | Bloch sphere + histogram, T-05 |
| FR-07 AI Tutor | ✅ | Gemini + mock fallback, T-08 |
| FR-08 Error Detection | ✅ | Circuit validation, T-07 |
| FR-09 Assessment | ✅ | MCQ quizzes + auto-grade, T-09 |
| FR-10 Progress Tracking | ✅ | Progress dashboard, T-10 |
| FR-11 Instructor Dashboard | ✅ | Real learner analytics from DB |
| FR-12 Export | ✅ | JSON / Qiskit `.py` / PNG from toolbar |
| NFR-01 Usability | ✅ | Beginner-friendly UI, TC-09 |
| NFR-02 Performance | ✅ | Aer < 2s for ≤5 qubits |
| NFR-03 Security | ✅ | JWT + bcrypt, TC-10 |
| NFR-06 Error Messages | ✅ | Descriptive validation messages |

---

## 🏗️ Architecture

```
React SPA ──── REST API ──── FastAPI Backend
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
               Qiskit Aer    Gemini AI        PostgreSQL
               Simulator      Tutor            Database
```

Design principles applied: Abstraction, Modularity, High Cohesion, Low Coupling, Adapter Pattern.

---

## 📋 DA Assignment Mapping

| Assignment | Coverage |
|---|---|
| DA-1 (Requirements) | 12 FR + 7 NFR + 7 Use Cases + RTM |
| DA-2 (Project Plan) | 6-Sprint Agile + WBS + Risk Register |
| DA-3 (Architecture) | Layered modular architecture + Testing strategy |

---

## 🔮 Roadmap (Post-MVP)

- [ ] PennyLane and Cirq backend adapters
- [ ] Real IBM Quantum hardware execution via qBraid
- [ ] Quantum error correction modules
- [ ] Collaborative multi-user circuit editing
- [ ] Advanced instructor analytics
- [ ] Mobile app (React Native)
- [ ] Quantum game: "Build the Circuit" challenge mode

---

*Built with ❤️ for quantum education — QLearnAI*

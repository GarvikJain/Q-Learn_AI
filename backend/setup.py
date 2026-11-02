import os
import json

base_dir = r"d:\QuantumComputing-AI\backend"

files = {
    "requirements.txt": """fastapi
uvicorn[standard]
sqlalchemy[asyncio]
asyncpg
alembic
pydantic[email]
pydantic-settings
python-jose[cryptography]
passlib[bcrypt]
python-multipart
qiskit
qiskit-aer
google-generativeai
httpx
python-dotenv
pytest
pytest-asyncio
""",
    ".env.example": """DATABASE_URL=postgresql+asyncpg://qlearn:qlearn@localhost:5432/qlearnai
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
GEMINI_API_KEY=your-gemini-api-key-here
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
""",
    "app/__init__.py": "",
    "app/main.py": """from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes import auth, modules, circuits, simulate, ai, assess, progress
from app.content.seed import seed_db

app = FastAPI(title="QLearnAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(modules.router, prefix="/modules", tags=["modules"])
app.include_router(circuits.router, prefix="/circuits", tags=["circuits"])
app.include_router(simulate.router, prefix="/simulate", tags=["simulate"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])
app.include_router(assess.router, prefix="/quizzes", tags=["assess"])
app.include_router(progress.router, prefix="/progress", tags=["progress"])

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_db()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}")
    return JSONResponse(status_code=500, content={"message": "Internal server error"})
""",
    "app/core/__init__.py": "",
    "app/core/config.py": """from pydantic_settings import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://qlearn:qlearn@localhost:5432/qlearnai"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    GEMINI_API_KEY: str = ""
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
""",
    "app/core/database.py": """from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
""",
    "app/core/security.py": """from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user
""",
    "app/models/__init__.py": """from .user import User
from .module import Module
from .circuit import Circuit
from .progress import UserProgress
from .quiz import Quiz, Question, QuizAttempt
from app.core.database import Base
""",
    "app/models/user.py": """from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="student")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
""",
    "app/models/module.py": """from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.database import Base

class Module(Base):
    __tablename__ = "modules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    order_index = Column(Integer, default=0)
    content_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
""",
    "app/models/circuit.py": """from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.database import Base

class Circuit(Base):
    __tablename__ = "circuits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    circuit_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
""",
    "app/models/progress.py": """from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.database import Base

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    module_id = Column(UUID(as_uuid=True), ForeignKey("modules.id"), nullable=False)
    status = Column(String, default="not_started")
    quiz_score = Column(Float, nullable=True)
    quiz_attempts = Column(Integer, default=0)
    time_spent_minutes = Column(Integer, default=0)
    last_accessed = Column(DateTime, default=datetime.utcnow)
""",
    "app/models/quiz.py": """from sqlalchemy import Column, String, Float, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.database import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    module_id = Column(UUID(as_uuid=True), ForeignKey("modules.id"), nullable=False)
    title = Column(String, nullable=False)

class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String, default="mcq")
    options = Column(Text, nullable=False)
    correct_answer = Column(String, nullable=False)
    explanation = Column(Text, nullable=True)

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"), nullable=False)
    score = Column(Float, nullable=False)
    answers_json = Column(Text, nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)
""",
    "app/schemas/__init__.py": "",
    "app/schemas/auth.py": """from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
""",
    "app/schemas/module.py": """from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ModuleResponse(BaseModel):
    id: UUID
    slug: str
    title: str
    description: Optional[str]
    order_index: int
    content_json: str

    class Config:
        from_attributes = True

class ModuleListItem(BaseModel):
    id: UUID
    slug: str
    title: str
    description: Optional[str]
    order_index: int

    class Config:
        from_attributes = True
""",
    "app/schemas/circuit.py": """from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class GateSchema(BaseModel):
    type: str
    targets: List[int]
    control: Optional[int] = None
    step: int

class CircuitSchema(BaseModel):
    num_qubits: int
    gates: List[GateSchema]
    metadata: Optional[Dict[str, Any]] = None

class CircuitCreate(BaseModel):
    title: str
    circuit_json: str

class CircuitResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    circuit_json: str
    created_at: datetime

    class Config:
        from_attributes = True
""",
    "app/schemas/simulation.py": """from pydantic import BaseModel
from typing import Dict, List, Optional
from app.schemas.circuit import CircuitSchema

class SimulationRequest(BaseModel):
    circuit: CircuitSchema
    backend: str = 'qiskit_aer'
    shots: int = 1024

class SimulationResult(BaseModel):
    counts: Dict[str, int]
    statevector: Optional[List[complex]] = None
    probabilities: Dict[str, float]
    execution_time_ms: float
    backend_used: str
    num_qubits: int
""",
    "app/schemas/ai.py": """from pydantic import BaseModel
from typing import Optional, List

class AIRequest(BaseModel):
    question: str
    context: Optional[str] = None
    mode: str = 'beginner'

class AIResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = None
    mode: str
""",
    "app/schemas/progress.py": """from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class ProgressResponse(BaseModel):
    module_id: UUID
    status: str
    quiz_score: Optional[float]
    quiz_attempts: int
    time_spent_minutes: int
    last_accessed: datetime

    class Config:
        from_attributes = True

class ProgressUpdate(BaseModel):
    status: Optional[str] = None
    time_spent_minutes: Optional[int] = None
""",
    "app/schemas/quiz.py": """from pydantic import BaseModel
from typing import List, Optional, Dict
from uuid import UUID

class QuestionResponse(BaseModel):
    id: UUID
    question_text: str
    question_type: str
    options: str
    explanation: Optional[str] = None

    class Config:
        from_attributes = True

class QuizResponse(BaseModel):
    id: UUID
    module_id: UUID
    title: str
    questions: List[QuestionResponse]

    class Config:
        from_attributes = True

class QuizSubmit(BaseModel):
    answers: Dict[str, str]

class QuizResult(BaseModel):
    score: float
    max_score: float
    percentage: float
    feedback: Dict[str, bool]
""",
    "app/simulation/__init__.py": "",
    "app/simulation/adapter.py": """from abc import ABC, abstractmethod

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
""",
    "app/simulation/qiskit_backend.py": """import time
import math
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
from .adapter import SimulatorAdapter

class QiskitAerBackend(SimulatorAdapter):
    def run(self, circuit_schema: dict, shots: int) -> dict:
        start_time = time.time()
        
        num_qubits = circuit_schema.get('num_qubits', 1)
        gates = circuit_schema.get('gates', [])
        
        has_measurement = any(g.get('type') == 'M' for g in gates)
        
        if not gates:
            raise ValueError("Circuit must have at least one gate or measurement")
        if not has_measurement:
            raise ValueError("Circuit must have at least one measurement")
            
        qc = QuantumCircuit(num_qubits, num_qubits)
        
        # Sort gates by step
        gates = sorted(gates, key=lambda x: x.get('step', 0))
        
        for gate in gates:
            gtype = gate['type'].upper()
            targets = gate['targets']
            if gtype == 'H':
                qc.h(targets[0])
            elif gtype == 'X':
                qc.x(targets[0])
            elif gtype == 'Y':
                qc.y(targets[0])
            elif gtype == 'Z':
                qc.z(targets[0])
            elif gtype == 'S':
                qc.s(targets[0])
            elif gtype == 'T':
                qc.t(targets[0])
            elif gtype == 'CNOT' or gtype == 'CX':
                qc.cx(gate['control'], targets[0])
            elif gtype == 'CCX':
                # assuming targets[0], targets[1] are controls, targets[2] is target
                qc.ccx(gate['control'][0], gate['control'][1], targets[0])
            elif gtype == 'SWAP':
                qc.swap(targets[0], targets[1])
            elif gtype == 'M':
                for t in targets:
                    qc.measure(t, t)
        
        simulator = Aer.get_backend('qasm_simulator')
        transpiled_qc = transpile(qc, simulator)
        job = simulator.run(transpiled_qc, shots=shots)
        result = job.result()
        counts = result.get_counts(transpiled_qc)
        
        probabilities = {k: v/shots for k, v in counts.items()}
        
        statevector = None
        if num_qubits <= 5:
            try:
                sv_qc = qc.remove_final_measurements(inplace=False)
                sv = Statevector.from_instruction(sv_qc)
                statevector = [complex(c.real, c.imag) for c in sv.data]
            except Exception:
                pass
                
        end_time = time.time()
        
        return {
            "counts": counts,
            "probabilities": probabilities,
            "statevector": statevector,
            "execution_time_ms": (end_time - start_time) * 1000,
            "backend_used": "qiskit_aer",
            "num_qubits": num_qubits
        }
""",
    "app/simulation/pennylane_backend.py": """from .adapter import SimulatorAdapter

class PennyLaneBackend(SimulatorAdapter):
    def run(self, circuit_schema: dict, shots: int) -> dict:
        raise NotImplementedError("PennyLane backend coming in v2.0")
""",
    "app/simulation/cirq_backend.py": """from .adapter import SimulatorAdapter

class CirqBackend(SimulatorAdapter):
    def run(self, circuit_schema: dict, shots: int) -> dict:
        raise NotImplementedError("Cirq backend coming in v2.0")
""",
    "app/ai/__init__.py": "",
    "app/ai/prompts.py": """BEGINNER_EXPLAIN_PROMPT = "Explain the following quantum concept simply, using no heavy math, and use everyday analogies:\\n{question}\\nContext:\\n{context}"
DEBUG_CIRCUIT_PROMPT = "Analyze this quantum circuit and the following error message. Suggest a fix.\\nCircuit:\\n{circuit}\\nError:\\n{error}"
CONCEPT_DEEP_PROMPT = "Provide a detailed explanation of this quantum concept suitable for intermediate/advanced users:\\n{question}\\nContext:\\n{context}"
CODE_GENERATE_PROMPT = "Generate Qiskit Python code for the following described circuit:\\n{description}"
SYSTEM_CONTEXT = "You are an AI Tutor for QLearnAI, a platform helping students learn quantum computing. Be encouraging and clear."
""",
    "app/ai/tutor.py": """import os
import google.generativeai as genai
from app.core.config import settings
from .prompts import BEGINNER_EXPLAIN_PROMPT, DEBUG_CIRCUIT_PROMPT, CONCEPT_DEEP_PROMPT, CODE_GENERATE_PROMPT, SYSTEM_CONTEXT

class GeminiTutor:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_CONTEXT)
        else:
            self.model = None

    async def explain(self, question: str, context: str = "", mode: str = "beginner") -> str:
        if not self.model:
            return self._mock_explain(question)
            
        prompt = BEGINNER_EXPLAIN_PROMPT if mode == "beginner" else CONCEPT_DEEP_PROMPT
        full_prompt = prompt.format(question=question, context=context)
        response = self.model.generate_content(full_prompt, generation_config={"temperature": 0.3})
        return response.text

    def _mock_explain(self, question: str) -> str:
        q = question.lower()
        if "superposition" in q:
            return "Superposition is like a spinning coin, it is both heads and tails until it lands."
        elif "entanglement" in q:
            return "Entanglement is when two qubits are connected such that changing one instantly affects the other."
        elif "qubit" in q:
            return "A qubit is the basic unit of quantum information, able to be 0, 1, or both."
        return "I am a mock AI tutor. To get real answers, please provide a Gemini API key."

    async def debug_circuit(self, circuit_json: str, error_msg: str) -> str:
        if not self.model:
            return "Mock debug: Check your gate targets."
        prompt = DEBUG_CIRCUIT_PROMPT.format(circuit=circuit_json, error=error_msg)
        response = self.model.generate_content(prompt, generation_config={"temperature": 0.3})
        return response.text

    async def generate_code(self, description: str) -> str:
        if not self.model:
            return "# Mock code\\nfrom qiskit import QuantumCircuit\\nqc = QuantumCircuit(1)"
        prompt = CODE_GENERATE_PROMPT.format(description=description)
        response = self.model.generate_content(prompt, generation_config={"temperature": 0.3})
        return response.text
""",
    "app/api/routes/__init__.py": "",
    "app/api/routes/auth.py": """from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.models.user import User
from app.schemas.auth import UserCreate, UserResponse, Token

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == user_in.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_pwd = hash_password(user_in.password)
    new_user = User(email=user_in.email, username=user_in.username, hashed_password=hashed_pwd)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_me(username: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    current_user.username = username
    await db.commit()
    await db.refresh(current_user)
    return current_user
""",
    "app/api/routes/modules.py": """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.core.database import get_db
from app.models.module import Module
from app.schemas.module import ModuleResponse, ModuleListItem

router = APIRouter()

@router.get("", response_model=List[ModuleListItem])
async def list_modules(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Module).order_by(Module.order_index))
    return result.scalars().all()

@router.get("/{slug}", response_model=ModuleResponse)
async def get_module(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Module).filter(Module.slug == slug))
    module = result.scalars().first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module
""",
    "app/api/routes/circuits.py": """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.circuit import Circuit
from app.schemas.circuit import CircuitCreate, CircuitResponse

router = APIRouter()

@router.post("", response_model=CircuitResponse)
async def create_circuit(circuit_in: CircuitCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    new_circuit = Circuit(user_id=current_user.id, title=circuit_in.title, circuit_json=circuit_in.circuit_json)
    db.add(new_circuit)
    await db.commit()
    await db.refresh(new_circuit)
    return new_circuit

@router.get("", response_model=List[CircuitResponse])
async def list_circuits(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Circuit).filter(Circuit.user_id == current_user.id))
    return result.scalars().all()

@router.get("/{circuit_id}", response_model=CircuitResponse)
async def get_circuit(circuit_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Circuit).filter(Circuit.id == circuit_id, Circuit.user_id == current_user.id))
    circuit = result.scalars().first()
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return circuit

@router.put("/{circuit_id}", response_model=CircuitResponse)
async def update_circuit(circuit_id: UUID, circuit_in: CircuitCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Circuit).filter(Circuit.id == circuit_id, Circuit.user_id == current_user.id))
    circuit = result.scalars().first()
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    circuit.title = circuit_in.title
    circuit.circuit_json = circuit_in.circuit_json
    await db.commit()
    await db.refresh(circuit)
    return circuit

@router.delete("/{circuit_id}")
async def delete_circuit(circuit_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Circuit).filter(Circuit.id == circuit_id, Circuit.user_id == current_user.id))
    circuit = result.scalars().first()
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    await db.delete(circuit)
    await db.commit()
    return {"message": "Deleted successfully"}
""",
    "app/api/routes/simulate.py": """from fastapi import APIRouter, HTTPException
from app.schemas.simulation import SimulationRequest, SimulationResult
from app.simulation.adapter import get_simulator

router = APIRouter()

@router.post("", response_model=SimulationResult)
async def simulate_circuit(req: SimulationRequest):
    try:
        simulator = get_simulator(req.backend)
        schema_dict = req.circuit.model_dump()
        result = simulator.run(schema_dict, req.shots)
        return result
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
""",
    "app/api/routes/ai.py": """from fastapi import APIRouter, Request, HTTPException
from app.schemas.ai import AIRequest, AIResponse
from app.ai.tutor import GeminiTutor
from pydantic import BaseModel
import time

router = APIRouter()
tutor = GeminiTutor()

rate_limits = {}

def check_rate_limit(ip: str):
    now = time.time()
    if ip not in rate_limits:
        rate_limits[ip] = []
    # Filter out requests older than 60 seconds
    rate_limits[ip] = [t for t in rate_limits[ip] if now - t < 60]
    if len(rate_limits[ip]) >= 20:
        raise HTTPException(status_code=429, detail="Too many requests")
    rate_limits[ip].append(now)

class DebugRequest(BaseModel):
    circuit_json: str
    error_msg: str

class GenerateRequest(BaseModel):
    description: str

@router.post("/explain", response_model=AIResponse)
async def explain(req: AIRequest, request: Request):
    check_rate_limit(request.client.host)
    answer = await tutor.explain(req.question, req.context or "", req.mode)
    return AIResponse(answer=answer, mode=req.mode)

@router.post("/debug", response_model=AIResponse)
async def debug(req: DebugRequest, request: Request):
    check_rate_limit(request.client.host)
    answer = await tutor.debug_circuit(req.circuit_json, req.error_msg)
    return AIResponse(answer=answer, mode="debug")

@router.post("/generate-code")
async def generate_code(req: GenerateRequest, request: Request):
    check_rate_limit(request.client.host)
    code = await tutor.generate_code(req.description)
    return {"code": code}
""",
    "app/api/routes/assess.py": """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import json
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.module import Module
from app.models.quiz import Quiz, Question, QuizAttempt
from app.models.progress import UserProgress
from app.schemas.quiz import QuizResponse, QuizSubmit, QuizResult

router = APIRouter()

@router.get("/{module_slug}", response_model=QuizResponse)
async def get_quiz(module_slug: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Module).filter(Module.slug == module_slug))
    module = result.scalars().first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
        
    result = await db.execute(select(Quiz).filter(Quiz.module_id == module.id))
    quiz = result.scalars().first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
        
    result = await db.execute(select(Question).filter(Question.quiz_id == quiz.id))
    questions = result.scalars().all()
    
    quiz_dict = {
        "id": quiz.id,
        "module_id": quiz.module_id,
        "title": quiz.title,
        "questions": questions
    }
    return quiz_dict

@router.post("/{module_slug}/submit", response_model=QuizResult)
async def submit_quiz(module_slug: str, submit: QuizSubmit, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Module).filter(Module.slug == module_slug))
    module = result.scalars().first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
        
    result = await db.execute(select(Quiz).filter(Quiz.module_id == module.id))
    quiz = result.scalars().first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
        
    result = await db.execute(select(Question).filter(Question.quiz_id == quiz.id))
    questions = result.scalars().all()
    
    score = 0.0
    max_score = len(questions)
    feedback = {}
    
    for q in questions:
        ans = submit.answers.get(str(q.id))
        is_correct = ans == q.correct_answer
        feedback[str(q.id)] = is_correct
        if is_correct:
            score += 1.0
            
    percentage = (score / max_score) * 100 if max_score > 0 else 0
    
    attempt = QuizAttempt(user_id=current_user.id, quiz_id=quiz.id, score=score, answers_json=json.dumps(submit.answers))
    db.add(attempt)
    
    result = await db.execute(select(UserProgress).filter(UserProgress.user_id == current_user.id, UserProgress.module_id == module.id))
    progress = result.scalars().first()
    if progress:
        progress.quiz_attempts += 1
        progress.quiz_score = max(progress.quiz_score or 0.0, score)
    else:
        progress = UserProgress(user_id=current_user.id, module_id=module.id, quiz_attempts=1, quiz_score=score, status="completed")
        db.add(progress)
        
    await db.commit()
    
    return QuizResult(score=score, max_score=max_score, percentage=percentage, feedback=feedback)
""",
    "app/api/routes/progress.py": """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.module import Module
from app.models.progress import UserProgress
from app.schemas.progress import ProgressResponse, ProgressUpdate
import datetime

router = APIRouter()

@router.get("", response_model=List[ProgressResponse])
async def get_all_progress(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserProgress).filter(UserProgress.user_id == current_user.id))
    return result.scalars().all()

@router.put("/{module_slug}", response_model=ProgressResponse)
async def update_progress(module_slug: str, update: ProgressUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Module).filter(Module.slug == module_slug))
    module = result.scalars().first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
        
    result = await db.execute(select(UserProgress).filter(UserProgress.user_id == current_user.id, UserProgress.module_id == module.id))
    progress = result.scalars().first()
    
    if not progress:
        progress = UserProgress(user_id=current_user.id, module_id=module.id)
        db.add(progress)
        
    if update.status:
        progress.status = update.status
    if update.time_spent_minutes is not None:
        progress.time_spent_minutes += update.time_spent_minutes
        
    progress.last_accessed = datetime.datetime.utcnow()
    await db.commit()
    await db.refresh(progress)
    return progress

@router.get("/summary")
async def get_summary(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Module))
    total_modules = len(result.scalars().all())
    
    result = await db.execute(select(UserProgress).filter(UserProgress.user_id == current_user.id))
    progress_list = result.scalars().all()
    
    completed = sum(1 for p in progress_list if p.status == "completed")
    in_progress = sum(1 for p in progress_list if p.status == "in_progress")
    total_time = sum(p.time_spent_minutes for p in progress_list)
    scores = [p.quiz_score for p in progress_list if p.quiz_score is not None]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    return {
        "total_modules": total_modules,
        "completed": completed,
        "in_progress": in_progress,
        "avg_quiz_score": avg_score,
        "total_time_minutes": total_time
    }

@router.get("/instructor/learners")
async def get_learners(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role != "instructor" and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    # Stub response
    return [{"user_id": str(current_user.id), "progress": "50%"}]
""",
    "app/content/seed.py": """import json
from sqlalchemy.future import select
from app.core.database import AsyncSessionLocal
from app.models.module import Module
from app.models.quiz import Quiz, Question

async def seed_db():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Module))
        if result.scalars().first():
            return # Already seeded
            
        modules_data = [
            {
                "slug": "qubit-basics", "title": "Qubit Basics", "order": 1,
                "content": {
                    "objectives": ["Understand what a qubit is", "Compare classical bit vs qubit", "Learn basis states |0⟩ and |1⟩"],
                    "sections": [
                        {"title": "What is a Qubit?", "content": "A qubit (quantum bit) is the fundamental unit of quantum information..."},
                    ],
                    "key_terms": ["qubit"],
                    "circuit_example": {"num_qubits": 1, "gates": [{"type": "X", "targets": [0], "step": 0}, {"type": "M", "targets": [0], "step": 1}]},
                    "summary": "A qubit is the quantum analog..."
                }
            },
            {
                "slug": "superposition", "title": "Superposition & The H Gate", "order": 2,
                "content": {"objectives": ["superposition"], "sections": [], "circuit_example": {"num_qubits":1, "gates":[{"type":"H","targets":[0],"step":0},{"type":"M","targets":[0],"step":1}]}}
            },
            {
                "slug": "entanglement", "title": "Entanglement & Bell States", "order": 3,
                "content": {"objectives": ["entanglement"], "sections": [], "circuit_example": {"num_qubits":2, "gates":[{"type":"H","targets":[0],"step":0},{"type":"CNOT","control":0,"targets":[1],"step":1},{"type":"M","targets":[0,1],"step":2}]}}
            },
            {"slug": "quantum-gates", "title": "Single-Qubit Gates", "order": 4, "content": {}},
            {"slug": "quantum-circuits", "title": "Multi-Qubit Circuits", "order": 5, "content": {}},
            {"slug": "deutsch-jozsa", "title": "Deutsch-Jozsa Algorithm", "order": 6, "content": {}},
            {"slug": "grovers-algorithm", "title": "Grover's Search Algorithm", "order": 7, "content": {}},
            {"slug": "qaoa-intro", "title": "QAOA Introduction", "order": 8, "content": {}},
            {"slug": "vqe-intro", "title": "VQE Introduction", "order": 9, "content": {}}
        ]
        
        for m_data in modules_data:
            m = Module(slug=m_data['slug'], title=m_data['title'], order_index=m_data['order'], content_json=json.dumps(m_data['content']))
            db.add(m)
            await db.flush()
            
            q = Quiz(module_id=m.id, title=f"Quiz for {m.title}")
            db.add(q)
            await db.flush()
            
            qq = Question(quiz_id=q.id, question_text=f"Sample question for {m.slug}", options=json.dumps(["A", "B"]), correct_answer="A")
            db.add(qq)
            
        await db.commit()
""",
    "tests/__init__.py": "",
    "tests/test_auth.py": """import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={"email": "test@test.com", "username": "testuser", "password": "password"})
    assert response.status_code in [200, 400]

@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/login", data={"username": "test@test.com", "password": "password"})
    assert response.status_code in [200, 400]
""",
    "tests/test_simulate.py": """import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_simulate_h_gate():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "circuit": {
                "num_qubits": 1,
                "gates": [
                    {"type": "H", "targets": [0], "step": 0},
                    {"type": "M", "targets": [0], "step": 1}
                ]
            }
        }
        response = await ac.post("/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "counts" in data
    
@pytest.mark.asyncio
async def test_simulate_empty_circuit():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "circuit": {
                "num_qubits": 1,
                "gates": []
            }
        }
        response = await ac.post("/simulate", json=payload)
    assert response.status_code in [400, 422]
""",
    "alembic.ini": """[alembic]
script_location = alembic
sqlalchemy.url = postgresql+asyncpg://qlearn:qlearn@localhost:5432/qlearnai
""",
    "alembic/env.py": """import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.core.config import settings
from app.models import Base

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    connectable = async_engine_from_config(config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
""",
    "alembic/versions/.gitkeep": ""
}

for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Files created successfully.")

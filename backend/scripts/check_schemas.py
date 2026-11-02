import uuid
from app.schemas.simulation import SimulationResult
from app.schemas.quiz import QuestionResponse
from app.schemas.module import ModuleResponse

r = SimulationResult(
    counts={"0": 1},
    probabilities={"0": 1.0},
    statevector=[[1.0, 0.0], [0.0, 0.0]],
    execution_time_ms=1.0,
    backend_used="qiskit_aer",
    num_qubits=1,
)
assert r.statevector[0] == [1.0, 0.0]

q = QuestionResponse(
    id=uuid.uuid4(),
    question_text="t",
    question_type="mcq",
    options='["a", "b"]',
)
assert q.options == ["a", "b"]

m = ModuleResponse(
    id=uuid.uuid4(),
    slug="x",
    title="t",
    description=None,
    order_index=1,
    content_json='{"sections": []}',
)
assert m.content_json["sections"] == []
print("schema checks OK")

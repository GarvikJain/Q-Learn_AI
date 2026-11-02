import { useCircuitStore } from '../../stores/circuitStore';
import { getGateColor, cn } from '../../lib/utils';
import { Gate } from '../../types';

export default function CircuitCanvas() {
  const { circuit, addGate, removeGate, selectedTool } = useCircuitStore();
  const numSteps = 12;

  const handleDrop = (e: React.DragEvent, target: number, step: number) => {
    e.preventDefault();
    const gateType = e.dataTransfer.getData('gateType');
    if (gateType) {
      addGateToCircuit(gateType, target, step);
    }
  };

  const handleClickCell = (target: number, step: number) => {
    if (selectedTool) {
      addGateToCircuit(selectedTool, target, step);
    }
  };

  const neighborQubit = (target: number): number | null => {
    if (target > 0) return target - 1;
    if (target + 1 < circuit.num_qubits) return target + 1;
    return null;
  };

  const addGateToCircuit = (gateType: string, target: number, step: number) => {
    let newGate: Gate = { type: gateType, targets: [target], step };

    if (gateType === 'CNOT') {
      const control = neighborQubit(target);
      if (control === null) {
        alert('CNOT requires at least 2 qubits');
        return;
      }
      newGate.control = control;
    } else if (gateType === 'SWAP') {
      const other = neighborQubit(target);
      if (other === null) {
        alert('SWAP requires at least 2 qubits');
        return;
      }
      newGate.targets = [target, other];
    } else if (gateType === 'Toffoli') {
      if (circuit.num_qubits < 3) {
        alert('Toffoli requires at least 3 qubits');
        return;
      }
      // Use two qubits other than the target as controls
      const controls = Array.from({ length: circuit.num_qubits }, (_, i) => i)
        .filter((i) => i !== target)
        .slice(0, 2);
      if (controls.length < 2) {
        alert('Toffoli requires exactly 2 control qubits');
        return;
      }
      newGate.controls = controls;
    } else if (gateType === 'Measure') {
      newGate.type = 'M';
    }

    addGate(newGate);
  };

  const displayLabel = (gate: Gate) => {
    if (gate.type === 'CNOT') return '⊕';
    if (gate.type === 'M') return 'M';
    return gate.type.length > 4 ? gate.type.substring(0, 3) : gate.type;
  };

  const renderGate = (gate: Gate, index: number) => {
    const primaryTarget = gate.targets[0];
    const top = primaryTarget * 64 + 32;
    const left = gate.step * 64 + 100;

    const linePartner =
      gate.control !== undefined
        ? gate.control
        : gate.controls?.[0] !== undefined
          ? gate.controls[0]
          : gate.type === 'SWAP' && gate.targets[1] !== undefined
            ? gate.targets[1]
            : undefined;

    return (
      <div key={index} className="absolute pointer-events-none" style={{ top, left, zIndex: 10 }}>
        {linePartner !== undefined && (
          <div
            className="absolute bg-indigo-500 w-0.5 left-1/2 transform -translate-x-1/2"
            style={{
              top:
                Math.min(primaryTarget, linePartner) === primaryTarget
                  ? '16px'
                  : `-${Math.abs(primaryTarget - linePartner) * 64 - 16}px`,
              height: `${Math.abs(primaryTarget - linePartner) * 64}px`,
            }}
          >
            <div
              className="absolute w-3 h-3 bg-indigo-500 rounded-full -left-1.5"
              style={{
                top: linePartner > primaryTarget ? '100%' : '0',
                transform: 'translateY(-50%)',
              }}
            />
          </div>
        )}
        {gate.controls?.[1] !== undefined && (
          <div
            className="absolute bg-teal-500 w-0.5 left-1/2 transform -translate-x-1/2 opacity-80"
            style={{
              top:
                Math.min(primaryTarget, gate.controls[1]) === primaryTarget
                  ? '16px'
                  : `-${Math.abs(primaryTarget - gate.controls[1]) * 64 - 16}px`,
              height: `${Math.abs(primaryTarget - gate.controls[1]) * 64}px`,
            }}
          >
            <div
              className="absolute w-3 h-3 bg-teal-500 rounded-full -left-1.5"
              style={{
                top: gate.controls[1] > primaryTarget ? '100%' : '0',
                transform: 'translateY(-50%)',
              }}
            />
          </div>
        )}

        <div
          className={cn(
            'w-12 h-12 -mt-6 -ml-6 flex items-center justify-center rounded text-white font-bold shadow-md cursor-pointer pointer-events-auto transition-transform hover:scale-110 text-xs',
            getGateColor(gate.type)
          )}
          onClick={(e) => {
            e.stopPropagation();
            removeGate(index);
          }}
          title="Click to remove"
        >
          {displayLabel(gate)}
        </div>
      </div>
    );
  };

  return (
    <div
      id="circuit-canvas-export"
      className="flex-1 overflow-auto bg-gray-50 dark:bg-gray-950 p-8 relative min-h-[400px]"
    >
      <div
        className="relative"
        style={{ width: `${numSteps * 64 + 200}px`, height: `${circuit.num_qubits * 64 + 64}px` }}
      >
        {Array.from({ length: circuit.num_qubits }).map((_, qIdx) => (
          <div
            key={`wire-${qIdx}`}
            className="absolute w-full h-16 flex items-center"
            style={{ top: qIdx * 64 }}
          >
            <div className="w-16 font-mono font-bold text-gray-500 dark:text-gray-400">
              q_{qIdx} |0⟩
            </div>
            <div className="flex-1 h-0.5 bg-gray-300 dark:bg-gray-700 ml-4 relative">
              {Array.from({ length: numSteps }).map((_, stepIdx) => (
                <div
                  key={`drop-${qIdx}-${stepIdx}`}
                  className="absolute w-12 h-12 -top-6 rounded border-2 border-dashed border-transparent hover:border-indigo-400 dark:hover:border-indigo-500 z-0"
                  style={{ left: stepIdx * 64 + 4 }}
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={(e) => handleDrop(e, qIdx, stepIdx)}
                  onClick={() => handleClickCell(qIdx, stepIdx)}
                />
              ))}
            </div>
          </div>
        ))}

        {circuit.gates.map((gate, i) => renderGate(gate, i))}
      </div>

      {circuit.gates.length === 0 && (
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-600 font-medium pointer-events-none">
          Drag and drop gates here to build a circuit
        </div>
      )}
    </div>
  );
}

import { create } from 'zustand';
import { CircuitJSON, Gate } from '../types';

interface CircuitState {
  circuit: CircuitJSON;
  selectedTool: string | null;
  isDirty: boolean;
  setCircuit: (circuit: CircuitJSON) => void;
  addGate: (gate: Gate) => void;
  removeGate: (gateIndex: number) => void;
  updateGate: (gateIndex: number, gate: Gate) => void;
  clearCircuit: () => void;
  setNumQubits: (num: number) => void;
  setSelectedTool: (tool: string | null) => void;
}

const initialCircuit: CircuitJSON = { num_qubits: 2, gates: [] };

export const useCircuitStore = create<CircuitState>((set) => ({
  circuit: initialCircuit,
  selectedTool: null,
  isDirty: false,
  setCircuit: (circuit) => set({ circuit, isDirty: false }),
  addGate: (gate) => set((state) => ({ 
    circuit: { ...state.circuit, gates: [...state.circuit.gates, gate] }, 
    isDirty: true 
  })),
  removeGate: (index) => set((state) => ({
    circuit: { ...state.circuit, gates: state.circuit.gates.filter((_, i) => i !== index) },
    isDirty: true
  })),
  updateGate: (index, gate) => set((state) => {
    const newGates = [...state.circuit.gates];
    newGates[index] = gate;
    return { circuit: { ...state.circuit, gates: newGates }, isDirty: true };
  }),
  clearCircuit: () => set((state) => ({ circuit: { ...state.circuit, gates: [] }, isDirty: true })),
  setNumQubits: (num) => set((state) => ({ circuit: { ...state.circuit, num_qubits: num }, isDirty: true })),
  setSelectedTool: (tool) => set({ selectedTool: tool }),
}));

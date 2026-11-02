import { getGateColor, cn } from '../../lib/utils';
import { MousePointer2, GripHorizontal } from 'lucide-react';

const availableGates = [
  { type: 'H', name: 'Hadamard', description: 'Creates superposition' },
  { type: 'X', name: 'Pauli-X (NOT)', description: 'Bit flip' },
  { type: 'Y', name: 'Pauli-Y', description: 'Bit and phase flip' },
  { type: 'Z', name: 'Pauli-Z', description: 'Phase flip' },
  { type: 'S', name: 'S Gate', description: 'π/2 phase shift' },
  { type: 'T', name: 'T Gate', description: 'π/4 phase shift' },
  { type: 'CNOT', name: 'CNOT', description: 'Controlled NOT (needs 2 qubits)' },
  { type: 'Toffoli', name: 'Toffoli (CCNOT)', description: 'Needs 3 qubits — click target (controls = neighbors)' },
  { type: 'SWAP', name: 'SWAP', description: 'Swaps two qubits (uses neighbor as pair)' },
  { type: 'M', name: 'Measurement', description: 'Measures qubit state' },
];

interface GatePaletteProps {
  selectedTool: string | null;
  onSelectTool: (tool: string | null) => void;
}

export default function GatePalette({ selectedTool, onSelectTool }: GatePaletteProps) {
  const handleDragStart = (e: React.DragEvent, gateType: string) => {
    e.dataTransfer.setData('gateType', gateType);
  };

  return (
    <div className="w-64 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 flex flex-col h-full">
      <div className="p-4 border-b border-gray-200 dark:border-gray-800">
        <h3 className="font-bold text-gray-900 dark:text-white flex items-center">
          <GripHorizontal className="w-5 h-5 mr-2 text-gray-500" />
          Gates Palette
        </h3>
        <p className="text-xs text-gray-500 mt-1">Drag gates to the circuit or select a tool.</p>
      </div>
      
      <div className="p-4 flex-1 overflow-y-auto space-y-4">
        {/* Pointer Tool */}
        <button
          onClick={() => onSelectTool(null)}
          className={cn(
            "w-full flex items-center p-2 rounded-lg border transition-colors",
            selectedTool === null 
              ? "bg-indigo-50 border-indigo-200 text-indigo-700 dark:bg-indigo-900/30 dark:border-indigo-800 dark:text-indigo-400" 
              : "bg-white border-gray-200 text-gray-700 hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-700"
          )}
        >
          <MousePointer2 className="w-4 h-4 mr-2" />
          <span className="text-sm font-medium">Select / Move</span>
        </button>

        <div className="space-y-2">
          {availableGates.map(gate => (
            <div
              key={gate.type}
              draggable
              onDragStart={(e) => handleDragStart(e, gate.type)}
              onClick={() => onSelectTool(gate.type)}
              className={cn(
                "group flex items-center p-2 rounded-lg border cursor-grab active:cursor-grabbing transition-all",
                selectedTool === gate.type 
                  ? "ring-2 ring-indigo-500 border-transparent bg-indigo-50 dark:bg-indigo-900/20" 
                  : "border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-indigo-300 dark:hover:border-indigo-700"
              )}
              title={gate.description}
            >
              <div className={cn(
                "w-8 h-8 rounded flex items-center justify-center text-white font-bold text-sm shadow-sm",
                getGateColor(gate.type)
              )}>
                {gate.type.substring(0, 3)}
              </div>
              <div className="ml-3">
                <span className="block text-sm font-medium text-gray-900 dark:text-white">{gate.type}</span>
                <span className="block text-xs text-gray-500 dark:text-gray-400 truncate w-32">{gate.name}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

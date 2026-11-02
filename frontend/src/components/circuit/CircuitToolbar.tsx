import { useRef, useState } from 'react';
import { Play, Save, Download, Trash2, Plus, Minus } from 'lucide-react';
import { useCircuitStore } from '../../stores/circuitStore';
import { circuits } from '../../lib/api';
import { downloadTextFile, generateQiskitCode } from '../../lib/utils';

interface CircuitToolbarProps {
  onRun: (backend: string, shots: number) => void;
  isLoading: boolean;
}

export default function CircuitToolbar({ onRun, isLoading }: CircuitToolbarProps) {
  const { circuit, setNumQubits, clearCircuit } = useCircuitStore();
  const [backend, setBackend] = useState('qiskit_aer');
  const [shots, setShots] = useState(1024);
  const [saving, setSaving] = useState(false);
  const [statusMsg, setStatusMsg] = useState<string | null>(null);
  const exportMenuRef = useRef<HTMLDivElement>(null);
  const [exportOpen, setExportOpen] = useState(false);

  const showStatus = (msg: string) => {
    setStatusMsg(msg);
    setTimeout(() => setStatusMsg(null), 3000);
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const title = `Circuit ${new Date().toLocaleString()}`;
      await circuits.saveCircuit({
        title,
        circuit_json: JSON.stringify(circuit),
      });
      showStatus('Circuit saved');
    } catch (err: any) {
      showStatus(err.response?.data?.detail || 'Save failed');
    } finally {
      setSaving(false);
    }
  };

  const exportJSON = () => {
    downloadTextFile(
      'circuit.json',
      JSON.stringify(circuit, null, 2),
      'application/json'
    );
    setExportOpen(false);
    showStatus('Exported JSON');
  };

  const exportCode = () => {
    downloadTextFile('circuit.py', generateQiskitCode(circuit), 'text/x-python');
    setExportOpen(false);
    showStatus('Exported Qiskit code');
  };

  const exportPNG = async () => {
    setExportOpen(false);
    const el = document.getElementById('circuit-canvas-export');
    if (!el) {
      showStatus('Canvas not found');
      return;
    }
    try {
      const html2canvas = (await import('html2canvas')).default;
      const canvas = await html2canvas(el, { backgroundColor: '#f9fafb', scale: 2 });
      const a = document.createElement('a');
      a.download = 'circuit.png';
      a.href = canvas.toDataURL('image/png');
      a.click();
      showStatus('Exported PNG');
    } catch {
      showStatus('PNG export failed — try JSON or code');
    }
  };

  return (
    <div className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 p-3 flex flex-wrap items-center justify-between gap-4">
      <div className="flex items-center space-x-2">
        <span className="text-sm font-medium text-gray-700 dark:text-gray-300 mr-2">Qubits:</span>
        <button
          onClick={() => setNumQubits(Math.max(1, circuit.num_qubits - 1))}
          className="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-800"
        >
          <Minus className="w-4 h-4 text-gray-600 dark:text-gray-400" />
        </button>
        <span className="font-mono text-gray-900 dark:text-white w-4 text-center">
          {circuit.num_qubits}
        </span>
        <button
          onClick={() => setNumQubits(Math.min(5, circuit.num_qubits + 1))}
          className="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-800"
        >
          <Plus className="w-4 h-4 text-gray-600 dark:text-gray-400" />
        </button>

        <div className="w-px h-6 bg-gray-300 dark:bg-gray-700 mx-2" />

        <button
          onClick={clearCircuit}
          className="flex items-center text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 px-2 py-1 rounded transition-colors"
        >
          <Trash2 className="w-4 h-4 mr-1" /> Clear
        </button>

        <button
          onClick={handleSave}
          disabled={saving || circuit.gates.length === 0}
          className="flex items-center text-sm text-indigo-600 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 px-2 py-1 rounded transition-colors disabled:opacity-50"
        >
          <Save className="w-4 h-4 mr-1" /> {saving ? 'Saving…' : 'Save'}
        </button>

        <div className="relative" ref={exportMenuRef}>
          <button
            onClick={() => setExportOpen((o) => !o)}
            disabled={circuit.gates.length === 0}
            className="flex items-center text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 px-2 py-1 rounded transition-colors disabled:opacity-50"
          >
            <Download className="w-4 h-4 mr-1" /> Export
          </button>
          {exportOpen && (
            <div className="absolute left-0 mt-1 w-44 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-50 py-1">
              <button
                onClick={exportJSON}
                className="w-full text-left px-3 py-2 text-sm hover:bg-gray-50 dark:hover:bg-gray-700"
              >
                JSON
              </button>
              <button
                onClick={exportCode}
                className="w-full text-left px-3 py-2 text-sm hover:bg-gray-50 dark:hover:bg-gray-700"
              >
                Qiskit code (.py)
              </button>
              <button
                onClick={exportPNG}
                className="w-full text-left px-3 py-2 text-sm hover:bg-gray-50 dark:hover:bg-gray-700"
              >
                PNG image
              </button>
            </div>
          )}
        </div>

        {statusMsg && (
          <span className="text-xs text-green-600 dark:text-green-400 ml-2">{statusMsg}</span>
        )}
      </div>

      <div className="flex items-center space-x-4">
        <select
          value={backend}
          onChange={(e) => setBackend(e.target.value)}
          className="text-sm border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-1.5 px-3"
        >
          <option value="qiskit_aer">Aer Simulator (Local)</option>
          <option value="ibmq" disabled>
            IBMQ (Coming soon)
          </option>
        </select>

        <select
          value={shots}
          onChange={(e) => setShots(Number(e.target.value))}
          className="text-sm border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-1.5 px-3"
        >
          <option value={1024}>1024 shots</option>
          <option value={100}>100 shots</option>
          <option value={4096}>4096 shots</option>
        </select>

        <button
          onClick={() => onRun(backend, shots)}
          disabled={isLoading || circuit.gates.length === 0}
          className="flex items-center px-4 py-1.5 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 transition-colors shadow-sm"
        >
          <Play className="w-4 h-4 mr-2" />
          {isLoading ? 'Running...' : 'Run Simulation'}
        </button>
      </div>
    </div>
  );
}

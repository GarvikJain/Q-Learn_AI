import { useState } from 'react';
import { Link } from 'react-router-dom';
import CodeEditor from '../components/editor/CodeEditor';
import ProbabilityHistogram from '../components/visualization/ProbabilityHistogram';
import ExecutionInfo from '../components/visualization/ExecutionInfo';
import { useSimulation } from '../hooks/useSimulation';
import { CircuitJSON } from '../types';
import { Play, CircuitBoard } from 'lucide-react';
import { generateQiskitCode } from '../lib/utils';

/** Preset Bell-state circuit for the code simulation page */
const bellCircuit: CircuitJSON = {
  num_qubits: 2,
  gates: [
    { type: 'H', targets: [0], step: 0 },
    { type: 'CNOT', targets: [1], control: 0, step: 1 },
    { type: 'M', targets: [0], step: 2 },
    { type: 'M', targets: [1], step: 2 },
  ],
};

const defaultCode = generateQiskitCode(bellCircuit);

export default function SimulationPage() {
  const [code, setCode] = useState(defaultCode);
  const { runSimulation, result, isLoading, errorMessage } = useSimulation();

  const handleRun = () => {
    // API accepts circuit JSON — run the Bell preset that matches the template code
    runSimulation({ circuit: bellCircuit, backend: 'qiskit_aer', shots: 1024 });
  };

  return (
    <div className="flex flex-col lg:flex-row gap-6 h-[calc(100vh-8rem)]">
      <div className="flex-1 flex flex-col h-full bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm p-4">
        <div className="flex justify-between items-center mb-2">
          <h2 className="text-lg font-bold text-gray-900 dark:text-white">Qiskit Code Editor</h2>
          <button
            onClick={handleRun}
            disabled={isLoading}
            className="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 transition-colors"
          >
            <Play className="w-4 h-4 mr-2" />
            {isLoading ? 'Running...' : 'Run Bell State Demo'}
          </button>
        </div>
        <p className="text-xs text-gray-500 dark:text-gray-400 mb-3">
          Monaco editor shows Qiskit code. Run executes the matching Bell-state circuit via the
          simulation API. For custom circuits, use the{' '}
          <Link to="/circuit" className="text-indigo-600 hover:underline inline-flex items-center">
            <CircuitBoard className="w-3 h-3 mr-1" /> Circuit Builder
          </Link>
          .
        </p>
        <div className="flex-1">
          <CodeEditor code={code} onChange={setCode} onRun={handleRun} />
        </div>
      </div>

      <div className="w-full lg:w-96 flex flex-col h-full bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm overflow-hidden">
        <div className="p-4 border-b border-gray-200 dark:border-gray-800">
          <h2 className="text-lg font-bold text-gray-900 dark:text-white">Results</h2>
        </div>
        <div className="p-4 flex-1 overflow-y-auto">
          {errorMessage && (
            <div className="p-4 bg-red-50 text-red-600 rounded-lg text-sm">{errorMessage}</div>
          )}
          {!result && !isLoading && !errorMessage && (
            <div className="text-center text-gray-500 mt-10">
              Run the Bell-state demo to see results
            </div>
          )}
          {isLoading && (
            <div className="text-center text-indigo-500 mt-10 animate-pulse">Simulating...</div>
          )}
          {result && !isLoading && (
            <div className="space-y-6">
              <ProbabilityHistogram probabilities={result.probabilities} />
              <ExecutionInfo result={result} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useCircuitStore } from '../stores/circuitStore';
import { useSimulation } from '../hooks/useSimulation';
import { circuits } from '../lib/api';
import GatePalette from '../components/circuit/GatePalette';
import CircuitCanvas from '../components/circuit/CircuitCanvas';
import CircuitToolbar from '../components/circuit/CircuitToolbar';
import ProbabilityHistogram from '../components/visualization/ProbabilityHistogram';
import StatevectorTable from '../components/visualization/StatevectorTable';
import BlochSphere from '../components/visualization/BlochSphere';
import ExecutionInfo from '../components/visualization/ExecutionInfo';
import CodeEditor from '../components/editor/CodeEditor';
import { generateQiskitCode } from '../lib/utils';
import { CircuitJSON } from '../types';

export default function CircuitBuilderPage() {
  const { id } = useParams<{ id: string }>();
  const { circuit, selectedTool, setSelectedTool, setCircuit } = useCircuitStore();
  const { runSimulation, result, isLoading, error } = useSimulation();
  const [activeTab, setActiveTab] = useState<'results' | 'code'>('results');
  const [loadError, setLoadError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    const load = async () => {
      try {
        const res = await circuits.getCircuit(id);
        const raw = res.data.circuit_json;
        const parsed: CircuitJSON = typeof raw === 'string' ? JSON.parse(raw) : raw;
        setCircuit(parsed);
      } catch (err: any) {
        setLoadError(err.response?.data?.detail || 'Failed to load circuit');
      }
    };
    load();
  }, [id, setCircuit]);

  const handleRun = (backend: string, shots: number) => {
    runSimulation({ circuit, backend, shots });
    setActiveTab('results');
  };

  return (
    <div className="flex h-[calc(100vh-6rem)] -m-4 lg:-m-8">
      <GatePalette selectedTool={selectedTool} onSelectTool={setSelectedTool} />

      <div className="flex-1 flex flex-col border-r border-gray-200 dark:border-gray-800 overflow-hidden">
        <CircuitToolbar onRun={handleRun} isLoading={isLoading} />
        {loadError && (
          <div className="px-4 py-2 bg-red-50 text-red-600 text-sm">{loadError}</div>
        )}
        <CircuitCanvas />
      </div>

      <div className="w-96 bg-white dark:bg-gray-900 flex flex-col h-full overflow-hidden shrink-0">
        <div className="flex border-b border-gray-200 dark:border-gray-800">
          <button
            className={`flex-1 py-3 text-sm font-medium border-b-2 ${activeTab === 'results' ? 'border-indigo-500 text-indigo-600 dark:text-indigo-400' : 'border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'}`}
            onClick={() => setActiveTab('results')}
          >
            Simulation Results
          </button>
          <button
            className={`flex-1 py-3 text-sm font-medium border-b-2 ${activeTab === 'code' ? 'border-indigo-500 text-indigo-600 dark:text-indigo-400' : 'border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'}`}
            onClick={() => setActiveTab('code')}
          >
            Code View
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-4">
          {activeTab === 'results' && (
            <div className="space-y-6">
              {error && (
                <div className="text-red-500 p-4 bg-red-50 dark:bg-red-900/20 rounded-lg text-sm">
                  {error.message}
                </div>
              )}
              {!result && !isLoading && !error && (
                <div className="text-center text-gray-500 dark:text-gray-400 mt-10">
                  Run the simulation to see results here.
                </div>
              )}
              {isLoading && (
                <div className="text-center text-indigo-500 mt-10 animate-pulse">
                  Running simulation...
                </div>
              )}
              {result && !isLoading && (
                <>
                  <ProbabilityHistogram probabilities={result.probabilities} />
                  {result.statevector && (
                    <StatevectorTable
                      statevector={result.statevector}
                      numQubits={result.num_qubits}
                    />
                  )}
                  <ExecutionInfo result={result} />
                  {result.num_qubits === 1 && result.statevector && (
                    <BlochSphere
                      alpha={{
                        real: result.statevector[0][0],
                        imag: result.statevector[0][1],
                      }}
                      beta={{
                        real: result.statevector[1][0],
                        imag: result.statevector[1][1],
                      }}
                      numQubits={1}
                    />
                  )}
                </>
              )}
            </div>
          )}

          {activeTab === 'code' && (
            <div className="h-full min-h-[400px]">
              <CodeEditor code={generateQiskitCode(circuit)} readOnly />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

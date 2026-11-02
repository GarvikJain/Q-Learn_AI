import { Cpu, Clock, Layers, Calendar } from 'lucide-react';
import { SimulationResult } from '../../types';

export default function ExecutionInfo({ result }: { result: SimulationResult }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
      <div className="bg-white dark:bg-gray-900 p-4 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm flex items-center space-x-3">
        <div className="p-2 bg-indigo-100 dark:bg-indigo-900/30 rounded-lg">
          <Cpu className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
        </div>
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400">Backend</p>
          <p className="font-semibold text-gray-900 dark:text-white text-sm">{result.backend_used}</p>
        </div>
      </div>
      
      <div className="bg-white dark:bg-gray-900 p-4 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm flex items-center space-x-3">
        <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
          <Clock className="w-5 h-5 text-blue-600 dark:text-blue-400" />
        </div>
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400">Time</p>
          <p className="font-semibold text-gray-900 dark:text-white text-sm">{result.execution_time_ms.toFixed(2)} ms</p>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-900 p-4 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm flex items-center space-x-3">
        <div className="p-2 bg-purple-100 dark:bg-purple-900/30 rounded-lg">
          <Layers className="w-5 h-5 text-purple-600 dark:text-purple-400" />
        </div>
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400">Qubits</p>
          <p className="font-semibold text-gray-900 dark:text-white text-sm">{result.num_qubits}</p>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-900 p-4 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm flex items-center space-x-3">
        <div className="p-2 bg-green-100 dark:bg-green-900/30 rounded-lg">
          <Calendar className="w-5 h-5 text-green-600 dark:text-green-400" />
        </div>
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400">Executed</p>
          <p className="font-semibold text-gray-900 dark:text-white text-sm">Just now</p>
        </div>
      </div>
    </div>
  );
}

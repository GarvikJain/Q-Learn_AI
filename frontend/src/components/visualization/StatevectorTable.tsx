import { getBasisStates } from '../../lib/utils';
import { cn } from '../../lib/utils';

interface StatevectorTableProps {
  statevector: number[][]; // Array of [real, imag]
  numQubits: number;
}

export default function StatevectorTable({ statevector, numQubits }: StatevectorTableProps) {
  const basisStates = getBasisStates(numQubits);
  
  const data = statevector.map((val, idx) => {
    const real = val[0];
    const imag = val[1];
    const amplitude = Math.sqrt(real*real + imag*imag);
    const prob = amplitude * amplitude;
    return {
      state: basisStates[idx],
      real,
      imag,
      amplitude,
      prob
    };
  }).sort((a, b) => b.prob - a.prob); // Sort by probability descending

  return (
    <div className="w-full overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-800 mt-4">
      <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-800 dark:text-gray-400">
          <tr>
            <th scope="col" className="px-6 py-3">Basis State</th>
            <th scope="col" className="px-6 py-3">Amplitude (α)</th>
            <th scope="col" className="px-6 py-3">Probability (|α|²)</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i} className="bg-white border-b dark:bg-gray-900 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50">
              <td className="px-6 py-4 font-mono text-gray-900 dark:text-white font-medium">
                {row.state}
              </td>
              <td className="px-6 py-4 font-mono text-xs">
                {row.real.toFixed(3)} {row.imag >= 0 ? '+' : '-'} {Math.abs(row.imag).toFixed(3)}i
              </td>
              <td className="px-6 py-4">
                <div className="flex items-center">
                  <span className="w-12 inline-block">{(row.prob * 100).toFixed(1)}%</span>
                  <div className="w-24 bg-gray-200 dark:bg-gray-700 rounded-full h-1.5 ml-2">
                    <div 
                      className="bg-indigo-600 h-1.5 rounded-full" 
                      style={{ width: `${row.prob * 100}%` }}
                    ></div>
                  </div>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

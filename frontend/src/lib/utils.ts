import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(dateString: string) {
  return new Intl.DateTimeFormat('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(dateString))
}

export function formatDuration(minutes: number) {
  const h = Math.floor(minutes / 60)
  const m = minutes % 60
  if (h > 0) return `${h}h ${m}m`
  return `${m}m`
}

export function getBasisStates(n_qubits: number) {
  const states = []
  const max = Math.pow(2, n_qubits)
  for (let i = 0; i < max; i++) {
    states.push(`|${i.toString(2).padStart(n_qubits, '0')}⟩`)
  }
  return states
}

export function probabilityToPercent(prob: number) {
  return `${(prob * 100).toFixed(1)}%`
}

export function getGateColor(gateType: string) {
  const colors: Record<string, string> = {
    H: 'bg-blue-500',
    X: 'bg-red-500',
    Y: 'bg-orange-500',
    Z: 'bg-green-500',
    S: 'bg-purple-500',
    T: 'bg-pink-500',
    CNOT: 'bg-yellow-500',
    Toffoli: 'bg-teal-500',
    SWAP: 'bg-gray-500',
    M: 'bg-slate-800 dark:bg-slate-700',
    Measure: 'bg-slate-800 dark:bg-slate-700',
  }
  return colors[gateType] || 'bg-gray-400'
}

/** Normalize UI gate types to backend simulator names */
export function toBackendGateType(type: string): string {
  if (type === 'Measure') return 'M'
  return type
}

export function downloadTextFile(filename: string, content: string, mime = 'text/plain') {
  const blob = new Blob([content], { type: mime })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

export function generateQiskitCode(circuit: { num_qubits: number; gates: Array<{ type: string; targets: number[]; control?: number; controls?: number[]; step: number }> }) {
  let code = `from qiskit import QuantumCircuit\nfrom qiskit_aer import AerSimulator\n\n`
  code += `qc = QuantumCircuit(${circuit.num_qubits}, ${circuit.num_qubits})\n\n`
  const sortedGates = [...circuit.gates].sort((a, b) => a.step - b.step)
  for (const gate of sortedGates) {
    const g = toBackendGateType(gate.type).toUpperCase()
    if (g === 'CNOT' || g === 'CX') {
      code += `qc.cx(${gate.control}, ${gate.targets[0]})\n`
    } else if (g === 'M') {
      code += `qc.measure(${gate.targets[0]}, ${gate.targets[0]})\n`
    } else if (g === 'SWAP') {
      const a = gate.targets[0]
      const b = gate.targets[1] ?? gate.control
      code += `qc.swap(${a}, ${b})\n`
    } else if (g === 'TOFFOLI' || g === 'CCX') {
      const c = gate.controls ?? []
      code += `qc.ccx(${c[0]}, ${c[1]}, ${gate.targets[0]})\n`
    } else {
      code += `qc.${g.toLowerCase()}(${gate.targets[0]})\n`
    }
  }
  code += `\nsimulator = AerSimulator()\n`
  code += `job = simulator.run(qc, shots=1024)\n`
  code += `result = job.result()\n`
  code += `print(result.get_counts(qc))\n`
  return code
}

import { useMutation } from '@tanstack/react-query';
import { simulate } from '../lib/api';
import { CircuitJSON, SimulationResult, Gate } from '../types';
import { toBackendGateType } from '../lib/utils';

function normalizeCircuit(circuit: CircuitJSON): CircuitJSON {
  return {
    ...circuit,
    gates: circuit.gates.map((g: Gate) => ({
      ...g,
      type: toBackendGateType(g.type),
    })),
  };
}

function extractErrorMessage(err: any): string {
  const detail = err?.response?.data?.detail;
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) {
    return detail.map((d) => d.msg || JSON.stringify(d)).join('; ');
  }
  return err?.message || 'Simulation failed';
}

export function useSimulation() {
  const mutation = useMutation({
    mutationFn: async (data: { circuit: CircuitJSON; backend: string; shots: number }) => {
      const payload = {
        circuit: normalizeCircuit(data.circuit),
        backend: data.backend,
        shots: data.shots,
      };
      const res = await simulate.runSimulation(payload);
      return res.data as SimulationResult;
    },
  });

  const errorMessage = mutation.error ? extractErrorMessage(mutation.error) : null;

  return {
    runSimulation: mutation.mutate,
    result: mutation.data,
    isLoading: mutation.isPending,
    error: mutation.error
      ? Object.assign(new Error(errorMessage || 'Simulation failed'), { message: errorMessage })
      : null,
    errorMessage,
    reset: mutation.reset,
  };
}

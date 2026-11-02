import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { useThemeStore } from '../../stores/themeStore';

interface ProbabilityHistogramProps {
  probabilities: Record<string, number>;
}

export default function ProbabilityHistogram({ probabilities }: ProbabilityHistogramProps) {
  const { theme } = useThemeStore();
  
  const data = Object.entries(probabilities)
    .map(([state, prob]) => ({
      state: `|${state}⟩`,
      probability: prob,
      probPercent: (prob * 100).toFixed(1)
    }))
    .sort((a, b) => a.state.localeCompare(b.state)); // Sort by basis state

  const maxProb = Math.max(...data.map(d => d.probability));

  return (
    <div className="w-full h-[300px] mt-4">
      <h3 className="text-center text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">Measurement Probabilities</h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
          <XAxis 
            dataKey="state" 
            stroke={theme === 'dark' ? '#9CA3AF' : '#4B5563'} 
            tick={{ fill: theme === 'dark' ? '#9CA3AF' : '#4B5563', fontFamily: 'monospace' }}
          />
          <YAxis 
            domain={[0, Math.max(1, maxProb * 1.2)]}
            tickFormatter={(val) => `${(val * 100).toFixed(0)}%`}
            stroke={theme === 'dark' ? '#9CA3AF' : '#4B5563'}
          />
          <Tooltip 
            cursor={{ fill: theme === 'dark' ? '#374151' : '#F3F4F6' }}
            contentStyle={{ 
              backgroundColor: theme === 'dark' ? '#1F2937' : '#FFFFFF',
              borderColor: theme === 'dark' ? '#374151' : '#E5E7EB',
              color: theme === 'dark' ? '#F9FAFB' : '#111827',
              borderRadius: '0.5rem',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'
            }}
            formatter={(value: number) => [`${(value * 100).toFixed(2)}%`, 'Probability']}
          />
          <Bar dataKey="probability" radius={[4, 4, 0, 0]} animationDuration={1000}>
            {data.map((entry, index) => {
              // Color gradient based on probability
              const hue = 260; // Indigo
              const saturation = 50 + (entry.probability * 50); // 50% to 100%
              const lightness = 60 - (entry.probability * 20); // 60% to 40%
              return <Cell key={`cell-${index}`} fill={`hsl(${hue}, ${saturation}%, ${lightness}%)`} />;
            })}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

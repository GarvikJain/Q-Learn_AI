import ProgressDashboard from '../components/progress/ProgressDashboard';

export default function ProgressPage() {
  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Your Progress</h1>
        <p className="text-gray-500 dark:text-gray-400 mt-2">Track your learning journey through the quantum realm.</p>
      </div>
      <ProgressDashboard />
    </div>
  );
}

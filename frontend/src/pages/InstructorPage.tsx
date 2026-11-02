import InstructorDashboard from '../components/instructor/InstructorDashboard';

export default function InstructorPage() {
  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Instructor Dashboard</h1>
        <p className="text-gray-500 dark:text-gray-400 mt-2">Monitor learner progress and engagement.</p>
      </div>
      <InstructorDashboard />
    </div>
  );
}

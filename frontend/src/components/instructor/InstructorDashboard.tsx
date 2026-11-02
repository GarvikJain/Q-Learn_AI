import { useEffect, useState } from 'react';
import { progress } from '../../lib/api';
import { Users, BookOpen, AlertCircle } from 'lucide-react';

interface Learner {
  user_id: string;
  username: string;
  email: string;
  completed_modules: number;
  in_progress_modules: number;
  avg_quiz_score: number | null;
  completion_pct: number;
}

interface InstructorData {
  total_learners: number;
  avg_completion_pct: number;
  struggling_learners: number;
  learners: Learner[];
}

export default function InstructorDashboard() {
  const [data, setData] = useState<InstructorData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await progress.getInstructorLearners();
        setData(res.data);
      } catch (err: any) {
        setError(
          err.response?.data?.detail ||
            'Unable to load instructor analytics. Instructor or admin role required.'
        );
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) {
    return <div className="h-48 bg-gray-200 dark:bg-gray-800 animate-pulse rounded-xl" />;
  }

  if (error) {
    return (
      <div className="p-6 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-xl text-yellow-800 dark:text-yellow-200">
        {error}
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm flex items-center">
          <div className="p-4 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 rounded-full mr-4">
            <Users className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Learners</p>
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
              {data.total_learners}
            </h3>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm flex items-center">
          <div className="p-4 bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 rounded-full mr-4">
            <BookOpen className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
              Avg Completion Rate
            </p>
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
              {data.avg_completion_pct}%
            </h3>
          </div>
        </div>
        <div className="bg-white dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm flex items-center">
          <div className="p-4 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-600 dark:text-yellow-400 rounded-full mr-4">
            <AlertCircle className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
              Struggling Learners
            </p>
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
              {data.struggling_learners}
            </h3>
          </div>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-gray-200 dark:border-gray-800">
          <h2 className="text-lg font-bold text-gray-900 dark:text-white">Learner Performance</h2>
        </div>
        {data.learners.length === 0 ? (
          <div className="p-8 text-center text-gray-500 dark:text-gray-400">
            No student accounts yet. Registered students will appear here.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-gray-500 dark:text-gray-400 uppercase bg-gray-50 dark:bg-gray-800">
                <tr>
                  <th className="px-6 py-3">Learner</th>
                  <th className="px-6 py-3">Email</th>
                  <th className="px-6 py-3">Completed</th>
                  <th className="px-6 py-3">In Progress</th>
                  <th className="px-6 py-3">Avg Score</th>
                  <th className="px-6 py-3">Completion</th>
                </tr>
              </thead>
              <tbody>
                {data.learners.map((l) => (
                  <tr
                    key={l.user_id}
                    className="bg-white dark:bg-gray-900 border-b dark:border-gray-800"
                  >
                    <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">
                      {l.username}
                    </td>
                    <td className="px-6 py-4 text-gray-500">{l.email}</td>
                    <td className="px-6 py-4">{l.completed_modules}</td>
                    <td className="px-6 py-4">{l.in_progress_modules}</td>
                    <td className="px-6 py-4">
                      {l.avg_quiz_score !== null ? `${l.avg_quiz_score} pts` : '—'}
                    </td>
                    <td className="px-6 py-4">{l.completion_pct}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

import { useEffect, useState } from 'react';
import { progress, modules } from '../../lib/api';
import { Progress, Module } from '../../types';
import { Trophy, Clock, BookOpen, Target } from 'lucide-react';
import { formatDuration } from '../../lib/utils';
import { Link } from 'react-router-dom';

interface ProgressRow extends Progress {
  title?: string;
  slug?: string;
}

interface Summary {
  total_modules: number;
  completed: number;
  in_progress: number;
  avg_quiz_score: number;
  total_time_minutes: number;
}

export default function ProgressDashboard() {
  const [rows, setRows] = useState<ProgressRow[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const [progressRes, summaryRes, modulesRes] = await Promise.all([
          progress.getProgress(),
          progress.getProgressSummary(),
          modules.getModules(),
        ]);
        const modList: Module[] = modulesRes.data;
        const modMap = new Map(modList.map((m) => [m.id, m]));

        const progressList: Progress[] = progressRes.data;
        const enriched: ProgressRow[] = progressList.map((p) => {
          const mod = modMap.get(p.module_id);
          return {
            ...p,
            title: mod?.title || 'Module',
            slug: mod?.slug,
          };
        });

        // Include not-started modules so the table looks complete
        const trackedIds = new Set(progressList.map((p) => p.module_id));
        for (const mod of modList) {
          if (!trackedIds.has(mod.id)) {
            enriched.push({
              module_id: mod.id,
              status: 'not_started',
              quiz_attempts: 0,
              time_spent_minutes: 0,
              title: mod.title,
              slug: mod.slug,
            });
          }
        }

        enriched.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
        setRows(enriched);
        setSummary(summaryRes.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to load progress');
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
      <div className="p-4 bg-red-50 dark:bg-red-900/20 text-red-600 rounded-lg">{error}</div>
    );
  }

  const completed = summary?.completed ?? 0;
  const avgScore = summary?.avg_quiz_score ?? 0;
  const totalTime = summary?.total_time_minutes ?? 0;
  const inProgress = summary?.in_progress ?? 0;

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm flex items-center">
          <div className="p-3 bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 rounded-lg mr-4">
            <Trophy className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Completed</p>
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
              {completed} / {summary?.total_modules ?? 0}
            </h3>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm flex items-center">
          <div className="p-3 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 rounded-lg mr-4">
            <Target className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Avg Quiz Score</p>
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
              {avgScore > 0 ? avgScore.toFixed(1) : '—'} pts
            </h3>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm flex items-center">
          <div className="p-3 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-lg mr-4">
            <Clock className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Time Spent</p>
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
              {formatDuration(totalTime)}
            </h3>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm flex items-center">
          <div className="p-3 bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 rounded-lg mr-4">
            <BookOpen className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500 dark:text-gray-400">In Progress</p>
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white">{inProgress}</h3>
          </div>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-gray-200 dark:border-gray-800">
          <h2 className="text-lg font-bold text-gray-900 dark:text-white">Module Progress</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-gray-500 dark:text-gray-400 uppercase bg-gray-50 dark:bg-gray-800">
              <tr>
                <th className="px-6 py-3">Module</th>
                <th className="px-6 py-3">Status</th>
                <th className="px-6 py-3">Score</th>
                <th className="px-6 py-3">Time Spent</th>
                <th className="px-6 py-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((p) => (
                <tr
                  key={p.module_id}
                  className="bg-white dark:bg-gray-900 border-b dark:border-gray-800"
                >
                  <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">
                    {p.title}
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        p.status === 'completed'
                          ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                          : p.status === 'in_progress'
                            ? 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900/30 dark:text-indigo-400'
                            : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-400'
                      }`}
                    >
                      {p.status.replace('_', ' ').toUpperCase()}
                    </span>
                  </td>
                  <td className="px-6 py-4 font-semibold">
                    {p.quiz_score !== undefined && p.quiz_score !== null
                      ? `${p.quiz_score} pts`
                      : '—'}
                  </td>
                  <td className="px-6 py-4 text-gray-500">
                    {formatDuration(p.time_spent_minutes || 0)}
                  </td>
                  <td className="px-6 py-4 text-right">
                    {p.slug ? (
                      <Link
                        to={`/learn/${p.slug}`}
                        className="text-indigo-600 dark:text-indigo-400 hover:underline"
                      >
                        {p.status === 'completed' ? 'Review' : 'Continue'}
                      </Link>
                    ) : (
                      '—'
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

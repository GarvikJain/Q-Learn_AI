import { useEffect, useState } from 'react';
import { useAuthStore } from '../stores/authStore';
import { modules } from '../lib/api';
import ModuleCard from '../components/learning/ModuleCard';
import { Module } from '../types';
import { PlayCircle, MessageSquare, CircuitBoard } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function DashboardPage() {
  const { user } = useAuthStore();
  const [mods, setMods] = useState<Module[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchModules = async () => {
      try {
        const res = await modules.getModules();
        setMods(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchModules();
  }, []);

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl p-8 text-white shadow-lg relative overflow-hidden">
        <div className="relative z-10">
          <h1 className="text-3xl font-bold mb-2">Welcome back, {user?.username}!</h1>
          <p className="text-indigo-100 max-w-xl">
            You're making great progress. Ready to dive back into the quantum realm?
          </p>
          <div className="mt-6 flex flex-wrap gap-4">
            <Link
              to={`/learn/${mods[0]?.slug || 'qubit-basics'}`}
              className="bg-white text-indigo-600 hover:bg-indigo-50 px-5 py-2.5 rounded-lg font-medium transition-colors flex items-center"
            >
              <PlayCircle className="w-5 h-5 mr-2" /> Continue Learning
            </Link>
          </div>
        </div>
        {/* Decorative elements */}
        <div className="absolute right-0 top-0 w-64 h-64 bg-white opacity-10 rounded-full transform translate-x-1/3 -translate-y-1/2"></div>
        <div className="absolute right-20 bottom-0 w-40 h-40 bg-purple-400 opacity-20 rounded-full transform translate-y-1/3"></div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Link to="/circuit" className="bg-white dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 flex items-center hover:shadow-md transition-shadow">
          <div className="bg-indigo-100 dark:bg-indigo-900/50 p-4 rounded-full mr-4">
            <CircuitBoard className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
          </div>
          <div>
            <h3 className="font-bold text-gray-900 dark:text-white">Circuit Builder</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">Design and simulate quantum circuits</p>
          </div>
        </Link>
        <Link to="/ai-tutor" className="bg-white dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 flex items-center hover:shadow-md transition-shadow">
          <div className="bg-purple-100 dark:bg-purple-900/50 p-4 rounded-full mr-4">
            <MessageSquare className="w-6 h-6 text-purple-600 dark:text-purple-400" />
          </div>
          <div>
            <h3 className="font-bold text-gray-900 dark:text-white">Ask AI Tutor</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">Get help with concepts and debugging</p>
          </div>
        </Link>
      </div>

      {/* Modules */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Learning Path</h2>
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1,2,3].map(i => <div key={i} className="h-48 bg-gray-200 dark:bg-gray-800 rounded-xl animate-pulse"></div>)}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mods.map(mod => (
              <ModuleCard key={mod.id} module={mod} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

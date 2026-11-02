import { Link } from 'react-router-dom';
import { Atom } from 'lucide-react';

export default function NotFoundPage() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex flex-col items-center justify-center text-center px-4">
      <div className="text-indigo-600 dark:text-indigo-400 mb-6 relative">
        <Atom className="w-32 h-32 animate-spin-slow" style={{ animationDuration: '10s' }} />
        <div className="absolute inset-0 quantum-glow rounded-full mix-blend-multiply opacity-50 blur-xl"></div>
      </div>
      <h1 className="text-6xl font-extrabold text-gray-900 dark:text-white mb-4">404</h1>
      <p className="text-xl text-gray-600 dark:text-gray-400 mb-8 max-w-md">
        State |ψ⟩ not found. The page you're looking for might have decohered or collapsed into another reality.
      </p>
      <Link 
        to="/dashboard" 
        className="px-6 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors shadow-sm"
      >
        Return to Dashboard
      </Link>
    </div>
  );
}

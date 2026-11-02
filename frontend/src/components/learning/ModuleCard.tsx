import { Link } from 'react-router-dom';
import { Module, Progress } from '../../types';
import { CheckCircle, PlayCircle, Lock } from 'lucide-react';
import { cn } from '../../lib/utils';

interface ModuleCardProps {
  module: Module;
  progress?: Progress;
}

export default function ModuleCard({ module, progress }: ModuleCardProps) {
  const isCompleted = progress?.status === 'completed';
  const isInProgress = progress?.status === 'in_progress';
  
  return (
    <Link to={`/learn/${module.slug}`} className="group block">
      <div className={cn(
        "bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-6 h-full transition-all duration-300 hover:shadow-lg hover:-translate-y-1",
        isCompleted && "border-green-200 dark:border-green-900/50",
        isInProgress && "border-indigo-200 dark:border-indigo-900/50"
      )}>
        <div className="flex justify-between items-start mb-4">
          <div className="flex items-center space-x-2">
            <span className="text-xs font-bold uppercase tracking-wider text-gray-500 dark:text-gray-400">
              Module {module.order_index}
            </span>
            {isCompleted && <span className="bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 text-xs px-2 py-0.5 rounded-full font-medium">Completed</span>}
            {isInProgress && <span className="bg-indigo-100 text-indigo-800 dark:bg-indigo-900/30 dark:text-indigo-400 text-xs px-2 py-0.5 rounded-full font-medium">In Progress</span>}
          </div>
          {isCompleted ? (
            <CheckCircle className="h-5 w-5 text-green-500" />
          ) : (
            <PlayCircle className={cn("h-5 w-5 transition-colors group-hover:text-indigo-500", isInProgress ? "text-indigo-500" : "text-gray-300 dark:text-gray-700")} />
          )}
        </div>
        
        <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
          {module.title}
        </h3>
        <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-3 mb-4">
          {module.description}
        </p>
        
        {progress?.quiz_score !== undefined && (
          <div className="mt-auto pt-4 border-t border-gray-100 dark:border-gray-800">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-500 dark:text-gray-400">Quiz Score</span>
              <span className="font-semibold text-gray-900 dark:text-white">{progress.quiz_score}%</span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5 mt-2">
              <div 
                className="bg-indigo-600 h-1.5 rounded-full" 
                style={{ width: `${progress.quiz_score}%` }}
              ></div>
            </div>
          </div>
        )}
      </div>
    </Link>
  );
}

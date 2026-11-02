import { Link, useLocation } from 'react-router-dom';
import {
  BookOpen,
  CircuitBoard,
  Cpu,
  MessageSquare,
  BarChart,
  Settings,
  GraduationCap,
} from 'lucide-react';
import { cn } from '../../lib/utils';
import { useAuthStore } from '../../stores/authStore';

export default function Sidebar() {
  const location = useLocation();
  const { user } = useAuthStore();
  const isInstructor = user?.role === 'instructor' || user?.role === 'admin';

  const links = [
    { name: 'Dashboard', href: '/dashboard', icon: BookOpen },
    { name: 'Circuit Builder', href: '/circuit', icon: CircuitBoard },
    { name: 'Simulation', href: '/simulate', icon: Cpu },
    { name: 'AI Tutor', href: '/ai-tutor', icon: MessageSquare },
    { name: 'Progress', href: '/progress', icon: BarChart },
    ...(isInstructor
      ? [{ name: 'Instructor', href: '/instructor', icon: GraduationCap }]
      : []),
  ];

  return (
    <div className="w-64 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 hidden lg:flex flex-col h-[calc(100vh-4rem)] sticky top-16">
      <div className="p-4 flex-1 overflow-y-auto">
        <div className="space-y-1">
          {links.map((link) => {
            const Icon = link.icon;
            const isActive = location.pathname.startsWith(link.href);
            return (
              <Link
                key={link.name}
                to={link.href}
                className={cn(
                  'flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-colors',
                  isActive
                    ? 'bg-indigo-50 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white'
                )}
              >
                <Icon
                  className={cn(
                    'mr-3 h-5 w-5',
                    isActive
                      ? 'text-indigo-600 dark:text-indigo-400'
                      : 'text-gray-400 dark:text-gray-500'
                  )}
                />
                {link.name}
              </Link>
            );
          })}
        </div>
      </div>
      <div className="p-4 border-t border-gray-200 dark:border-gray-800">
        <Link
          to="/profile"
          className="flex items-center px-3 py-2 text-sm font-medium rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
        >
          <Settings className="mr-3 h-5 w-5 text-gray-400 dark:text-gray-500" />
          Settings
        </Link>
      </div>
    </div>
  );
}

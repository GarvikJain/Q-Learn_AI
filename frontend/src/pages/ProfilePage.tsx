import { useAuthStore } from '../stores/authStore';
import { User, Mail, Shield, Calendar } from 'lucide-react';

export default function ProfilePage() {
  const { user } = useAuthStore();

  if (!user) return null;

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden">
        <div className="h-32 bg-gradient-to-r from-indigo-500 to-purple-600"></div>
        <div className="px-8 pb-8 relative">
          <div className="absolute -top-12 w-24 h-24 bg-white dark:bg-gray-800 rounded-full border-4 border-white dark:border-gray-900 flex items-center justify-center text-3xl font-bold text-indigo-600 dark:text-indigo-400 shadow-md">
            {user.username.charAt(0).toUpperCase()}
          </div>
          
          <div className="pt-16">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">{user.username}</h1>
            <div className="flex items-center space-x-4 mt-2">
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800 dark:bg-indigo-900/30 dark:text-indigo-400 uppercase">
                {user.role}
              </span>
              {user.is_active && (
                <span className="inline-flex items-center text-xs font-medium text-green-600 dark:text-green-400">
                  <span className="w-2 h-2 mr-1.5 bg-green-500 rounded-full"></span>
                  Active Account
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-800 p-8">
        <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-6">Account Information</h3>
        
        <div className="space-y-4">
          <div className="flex items-center py-3 border-b border-gray-100 dark:border-gray-800">
            <User className="w-5 h-5 text-gray-400 mr-4" />
            <div>
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Username</p>
              <p className="text-gray-900 dark:text-white">{user.username}</p>
            </div>
          </div>
          
          <div className="flex items-center py-3 border-b border-gray-100 dark:border-gray-800">
            <Mail className="w-5 h-5 text-gray-400 mr-4" />
            <div>
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Email Address</p>
              <p className="text-gray-900 dark:text-white">{user.email}</p>
            </div>
          </div>

          <div className="flex items-center py-3 border-b border-gray-100 dark:border-gray-800">
            <Shield className="w-5 h-5 text-gray-400 mr-4" />
            <div>
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Role</p>
              <p className="text-gray-900 dark:text-white capitalize">{user.role}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

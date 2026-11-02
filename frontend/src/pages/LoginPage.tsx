import LoginForm from '../components/auth/LoginForm';
import { Atom } from 'lucide-react';

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-gray-900 flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 z-0">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
        <div className="absolute top-1/3 right-1/4 w-96 h-96 bg-purple-600 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse" style={{ animationDelay: '2s' }}></div>
      </div>

      <div className="sm:mx-auto sm:w-full sm:max-w-md relative z-10">
        <div className="flex justify-center text-indigo-400 mb-4 quantum-glow rounded-full w-16 h-16 mx-auto items-center">
          <Atom size={40} />
        </div>
        <h2 className="mt-2 text-center text-3xl font-extrabold text-white">
          Welcome to QLearnAI
        </h2>
        <p className="mt-2 text-center text-sm text-gray-400">
          Interactive quantum computing education powered by AI
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md relative z-10">
        <LoginForm />
      </div>
    </div>
  );
}

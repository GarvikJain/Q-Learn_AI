import ChatPanel from '../components/ai-tutor/ChatPanel';
import { Lightbulb, BookOpen, Bug, Code } from 'lucide-react';

export default function AITutorPage() {
  return (
    <div className="flex gap-6 max-w-7xl mx-auto h-[calc(100vh-8rem)]">
      {/* Main Chat Area */}
      <div className="flex-1 min-w-0">
        <ChatPanel />
      </div>

      {/* Sidebar Info */}
      <div className="hidden lg:flex flex-col w-80 space-y-6">
        <div className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl p-6 text-white shadow-md">
          <Lightbulb className="w-8 h-8 mb-4 opacity-80" />
          <h3 className="font-bold text-lg mb-2">How to use the AI Tutor</h3>
          <p className="text-indigo-100 text-sm leading-relaxed">
            I can help you understand quantum concepts, debug your circuits, or generate Qiskit code. Try asking for explanations at different difficulty levels.
          </p>
        </div>

        <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-6 shadow-sm flex-1">
          <h3 className="font-bold text-gray-900 dark:text-white mb-4">Capabilities</h3>
          <ul className="space-y-4">
            <li className="flex items-start">
              <BookOpen className="w-5 h-5 mr-3 text-indigo-500 flex-shrink-0 mt-0.5" />
              <div>
                <span className="font-medium text-gray-900 dark:text-gray-100 block text-sm">Explain Concepts</span>
                <span className="text-xs text-gray-500 dark:text-gray-400">Clear explanations of superposition, entanglement, etc.</span>
              </div>
            </li>
            <li className="flex items-start">
              <Bug className="w-5 h-5 mr-3 text-red-500 flex-shrink-0 mt-0.5" />
              <div>
                <span className="font-medium text-gray-900 dark:text-gray-100 block text-sm">Debug Circuits</span>
                <span className="text-xs text-gray-500 dark:text-gray-400">Help finding logical errors in your quantum circuits.</span>
              </div>
            </li>
            <li className="flex items-start">
              <Code className="w-5 h-5 mr-3 text-green-500 flex-shrink-0 mt-0.5" />
              <div>
                <span className="font-medium text-gray-900 dark:text-gray-100 block text-sm">Generate Code</span>
                <span className="text-xs text-gray-500 dark:text-gray-400">Convert ideas into working Qiskit Python code.</span>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}

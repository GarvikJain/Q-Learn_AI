import { useState, useRef, useEffect } from 'react';
import { useAITutor, AIMode } from '../../hooks/useAITutor';
import { Send, Atom, Trash2, Loader2 } from 'lucide-react';
import { cn } from '../../lib/utils';

export default function ChatPanel() {
  const [input, setInput] = useState('');
  const [difficulty, setDifficulty] = useState('Beginner');
  const [taskMode, setTaskMode] = useState<AIMode>('explain');
  const { ask, messages, isLoading, error, clearMessages } = useAITutor();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    ask(input, 'General quantum computing concepts', difficulty, taskMode);
    setInput('');
  };

  const handleSuggest = (question: string, mode: AIMode = 'explain') => {
    if (isLoading) return;
    setTaskMode(mode);
    ask(question, 'General quantum computing concepts', difficulty, mode);
  };

  const suggestions = [
    { q: 'What is superposition?', mode: 'explain' as AIMode },
    { q: 'Explain entanglement', mode: 'explain' as AIMode },
    { q: 'Why does my circuit need a measurement?', mode: 'debug' as AIMode },
    { q: 'Generate a Bell state circuit in Qiskit', mode: 'generate' as AIMode },
  ];

  const placeholder =
    taskMode === 'generate'
      ? 'Describe the circuit or algorithm to generate…'
      : taskMode === 'debug'
        ? 'Describe the circuit error or paste the error message…'
        : 'Ask a question about quantum computing…';

  return (
    <div className="flex flex-col h-[calc(100vh-10rem)] bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm overflow-hidden">
      <div className="p-4 border-b border-gray-200 dark:border-gray-800 flex flex-wrap items-center justify-between gap-3 bg-gray-50 dark:bg-gray-900/50">
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 bg-indigo-100 dark:bg-indigo-900/50 rounded-full flex items-center justify-center">
            <Atom className="h-6 w-6 text-indigo-600 dark:text-indigo-400" />
          </div>
          <div>
            <h2 className="font-bold text-gray-900 dark:text-white">AI Tutor</h2>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Gemini + mock fallback
            </p>
          </div>
        </div>
        <div className="flex items-center flex-wrap gap-2">
          <select
            value={taskMode}
            onChange={(e) => setTaskMode(e.target.value as AIMode)}
            className="text-sm bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-md px-2 py-1 text-gray-700 dark:text-gray-200"
          >
            <option value="explain">Explain</option>
            <option value="debug">Debug</option>
            <option value="generate">Generate code</option>
          </select>
          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            className="text-sm bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-md px-2 py-1 text-gray-700 dark:text-gray-200"
            disabled={taskMode !== 'explain'}
          >
            <option>Beginner</option>
            <option>Intermediate</option>
            <option>Advanced</option>
          </select>
          <button
            onClick={clearMessages}
            className="text-gray-400 hover:text-red-500 transition-colors p-2"
            title="Clear Chat"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center space-y-6">
            <div className="h-20 w-20 bg-indigo-50 dark:bg-indigo-900/20 rounded-full flex items-center justify-center mb-4">
              <Atom className="h-10 w-10 text-indigo-500 quantum-glow" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                How can I help you learn today?
              </h3>
              <p className="text-gray-500 dark:text-gray-400 max-w-md">
                Explain concepts, debug circuits, or generate Qiskit code.
              </p>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-lg mt-8">
              {suggestions.map(({ q, mode }) => (
                <button
                  key={q}
                  onClick={() => handleSuggest(q, mode)}
                  className="px-4 py-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-sm text-gray-700 dark:text-gray-300 hover:bg-indigo-50 dark:hover:bg-gray-700 hover:border-indigo-200 dark:hover:border-gray-600 transition-colors text-left"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div
              key={idx}
              className={cn('flex', msg.role === 'user' ? 'justify-end' : 'justify-start')}
            >
              <div
                className={cn(
                  'max-w-[80%] rounded-2xl px-5 py-4 flex items-start space-x-3 shadow-sm',
                  msg.role === 'user'
                    ? 'bg-indigo-600 text-white rounded-tr-none'
                    : 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 rounded-tl-none'
                )}
              >
                {msg.role === 'assistant' && (
                  <Atom className="h-5 w-5 mt-0.5 flex-shrink-0 text-indigo-500" />
                )}
                <div className="prose dark:prose-invert prose-sm max-w-none whitespace-pre-wrap">
                  {msg.content.split('\n').map((line, i) => (
                    <p key={i} className={i > 0 ? 'mt-2' : ''}>
                      {line}
                    </p>
                  ))}
                </div>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 dark:bg-gray-800 rounded-2xl rounded-tl-none px-5 py-4 flex items-center space-x-2 shadow-sm">
              <Atom className="h-5 w-5 text-indigo-500 animate-spin" />
              <div className="flex space-x-1">
                <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce" />
                <div
                  className="h-2 w-2 bg-gray-400 rounded-full animate-bounce"
                  style={{ animationDelay: '0.2s' }}
                />
                <div
                  className="h-2 w-2 bg-gray-400 rounded-full animate-bounce"
                  style={{ animationDelay: '0.4s' }}
                />
              </div>
            </div>
          </div>
        )}
        {error && (
          <p className="text-center text-xs text-red-500">{error}</p>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
        <form onSubmit={handleSubmit} className="relative flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={placeholder}
            className="w-full bg-gray-100 dark:bg-gray-800 border-transparent focus:border-indigo-500 focus:bg-white dark:focus:bg-gray-900 focus:ring-0 rounded-full pl-6 pr-12 py-3 text-sm text-gray-900 dark:text-white transition-all shadow-sm"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="absolute right-2 p-2 bg-indigo-600 text-white rounded-full hover:bg-indigo-700 disabled:opacity-50 disabled:hover:bg-indigo-600 transition-colors"
          >
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </button>
        </form>
        <p className="text-center text-xs text-gray-400 mt-2">
          Mode: {taskMode}. AI responses are educational — verify with course materials.
        </p>
      </div>
    </div>
  );
}

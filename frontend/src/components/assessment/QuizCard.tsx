import { useState } from 'react';
import { Quiz } from '../../types';
import { CheckCircle, XCircle } from 'lucide-react';
import { cn } from '../../lib/utils';

interface QuizCardProps {
  quiz: Quiz;
  onSubmit: (answers: Record<string, string>) => void;
}

export default function QuizCard({ quiz, onSubmit }: QuizCardProps) {
  const [answers, setAnswers] = useState<Record<string, string>>({});

  const handleSelect = (questionId: string, option: string) => {
    setAnswers(prev => ({ ...prev, [questionId]: option }));
  };

  const isComplete = Object.keys(answers).length === quiz.questions.length;

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <div className="bg-white dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 text-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">{quiz.title}</h2>
        <p className="text-gray-500 dark:text-gray-400 mt-2">Answer all questions to complete the module.</p>
      </div>

      {quiz.questions.map((q, idx) => (
        <div key={q.id} className="bg-white dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm">
          <div className="flex items-center space-x-3 mb-4">
            <span className="flex items-center justify-center w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-900/50 text-indigo-700 dark:text-indigo-400 font-bold text-sm">
              {idx + 1}
            </span>
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">{q.question_text}</h3>
          </div>
          
          <div className="space-y-3 mt-6">
            {q.options?.map((opt, oIdx) => (
              <label 
                key={oIdx}
                className={cn(
                  "flex items-center p-4 border rounded-lg cursor-pointer transition-all",
                  answers[q.id] === opt 
                    ? "border-indigo-600 bg-indigo-50 dark:bg-indigo-900/20 dark:border-indigo-500" 
                    : "border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800"
                )}
              >
                <input
                  type="radio"
                  name={q.id}
                  value={opt}
                  checked={answers[q.id] === opt}
                  onChange={() => handleSelect(q.id, opt)}
                  className="w-4 h-4 text-indigo-600 bg-gray-100 border-gray-300 focus:ring-indigo-500 dark:focus:ring-indigo-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                />
                <span className="ml-3 text-gray-700 dark:text-gray-300">{opt}</span>
              </label>
            ))}
          </div>
        </div>
      ))}

      <div className="flex justify-end">
        <button
          onClick={() => onSubmit(answers)}
          disabled={!isComplete}
          className="px-8 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Submit Quiz
        </button>
      </div>
    </div>
  );
}

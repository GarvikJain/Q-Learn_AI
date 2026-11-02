import { QuizResult } from '../../types';
import { CheckCircle2, XCircle, RotateCcw, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import { cn } from '../../lib/utils';

interface ScoreBoardProps {
  result: QuizResult;
  onRetry: () => void;
  nextModuleUrl?: string;
}

export default function ScoreBoard({ result, onRetry, nextModuleUrl }: ScoreBoardProps) {
  const isPassed = result.percentage >= 70;

  return (
    <div className="max-w-2xl mx-auto bg-white dark:bg-gray-900 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden">
      <div className="p-10 text-center border-b border-gray-200 dark:border-gray-800">
        <div className="relative inline-flex items-center justify-center w-32 h-32 mb-6">
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
            <path
              className="text-gray-200 dark:text-gray-700"
              strokeWidth="3"
              stroke="currentColor"
              fill="none"
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
            />
            <path
              className={isPassed ? "text-green-500" : "text-yellow-500"}
              strokeWidth="3"
              strokeDasharray={`${result.percentage}, 100`}
              strokeLinecap="round"
              stroke="currentColor"
              fill="none"
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
            />
          </svg>
          <div className="absolute flex flex-col items-center justify-center">
            <span className="text-3xl font-bold text-gray-900 dark:text-white">{result.score}</span>
            <span className="text-sm text-gray-500">out of {result.max_score}</span>
          </div>
        </div>
        
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          {isPassed ? 'Excellent Work!' : 'Keep Practicing!'}
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          You scored {result.percentage}%. {isPassed ? "You've mastered this module." : "Review the material and try again."}
        </p>
      </div>

      <div className="p-6 bg-gray-50 dark:bg-gray-900/50 space-y-4">
        <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Feedback</h3>
        {Object.entries(result.feedback).map(([questionId, raw]: [string, any], idx) => {
          const feedbackObj =
            typeof raw === 'boolean'
              ? { is_correct: raw, correct_answer: undefined, explanation: undefined }
              : raw;
          return (
            <div
              key={questionId}
              className="flex items-start p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
            >
              {feedbackObj.is_correct ? (
                <CheckCircle2 className="w-5 h-5 text-green-500 mt-0.5 mr-3 flex-shrink-0" />
              ) : (
                <XCircle className="w-5 h-5 text-red-500 mt-0.5 mr-3 flex-shrink-0" />
              )}
              <div>
                <p className="font-medium text-gray-900 dark:text-white text-sm mb-1">
                  Question {idx + 1}
                </p>
                {!feedbackObj.is_correct && feedbackObj.correct_answer && (
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Correct answer:{' '}
                    <span className="font-semibold">{feedbackObj.correct_answer}</span>
                  </p>
                )}
                {feedbackObj.explanation && (
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                    {feedbackObj.explanation}
                  </p>
                )}
              </div>
            </div>
          );
        })}
      </div>

      <div className="p-6 border-t border-gray-200 dark:border-gray-800 flex flex-col sm:flex-row gap-4 justify-center">
        <button
          onClick={onRetry}
          className="flex-1 flex items-center justify-center px-6 py-3 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-200 font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
        >
          <RotateCcw className="w-4 h-4 mr-2" /> Retry Quiz
        </button>
        {nextModuleUrl && isPassed && (
          <Link
            to={nextModuleUrl}
            className="flex-1 flex items-center justify-center px-6 py-3 bg-indigo-600 rounded-lg text-white font-medium hover:bg-indigo-700 transition-colors"
          >
            Next Module <ArrowRight className="w-4 h-4 ml-2" />
          </Link>
        )}
      </div>
    </div>
  );
}

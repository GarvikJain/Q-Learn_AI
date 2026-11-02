import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { quizzes } from '../lib/api';
import { Quiz, QuizResult } from '../types';
import QuizCard from '../components/assessment/QuizCard';
import ScoreBoard from '../components/assessment/ScoreBoard';

export default function QuizPage() {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [result, setResult] = useState<QuizResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchQuiz = async () => {
      if (!slug) return;
      try {
        const res = await quizzes.getQuiz(slug);
        setQuiz(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchQuiz();
  }, [slug]);

  const handleSubmit = async (answers: Record<string, string>) => {
    if (!slug) return;
    try {
      const res = await quizzes.submitQuiz(slug, { answers });
      setResult(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleRetry = () => {
    setResult(null);
  };

  if (loading) {
    return <div className="max-w-3xl mx-auto mt-10 h-64 bg-gray-200 dark:bg-gray-800 animate-pulse rounded-xl"></div>;
  }

  if (!quiz) {
    return <div>Quiz not found</div>;
  }

  return (
    <div className="py-8">
      {!result ? (
        <QuizCard quiz={quiz} onSubmit={handleSubmit} />
      ) : (
        <ScoreBoard 
          result={result} 
          onRetry={handleRetry} 
          nextModuleUrl="/dashboard" // Simplified for now
        />
      )}
    </div>
  );
}

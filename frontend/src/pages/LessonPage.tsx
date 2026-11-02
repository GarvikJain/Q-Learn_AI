import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { modules, progress } from '../lib/api';
import { Module } from '../types';
import LessonViewer from '../components/learning/LessonViewer';

export default function LessonPage() {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const [moduleData, setModuleData] = useState<Module | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchModule = async () => {
      if (!slug) return;
      try {
        setLoading(true);
        const res = await modules.getModule(slug);
        const data = res.data;
        // Normalize content_json if API ever returns a string
        if (typeof data.content_json === 'string') {
          data.content_json = JSON.parse(data.content_json);
        }
        setModuleData(data);

        // Start progress tracking
        await progress.updateProgress(slug, { status: 'in_progress' });
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchModule();
  }, [slug]);

  const handleComplete = async () => {
    if (!slug) return;
    try {
      await progress.updateProgress(slug, { status: 'completed' });
      navigate(`/quizzes/${slug}`);
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto space-y-4">
        <div className="h-32 bg-gray-200 dark:bg-gray-800 rounded-2xl animate-pulse"></div>
        <div className="h-64 bg-gray-200 dark:bg-gray-800 rounded-2xl animate-pulse"></div>
      </div>
    );
  }

  if (!moduleData) {
    return <div>Module not found</div>;
  }

  return (
    <div className="pb-12">
      <LessonViewer module={moduleData} onComplete={handleComplete} />
    </div>
  );
}

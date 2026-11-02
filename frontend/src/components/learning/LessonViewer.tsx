import { useState } from 'react';
import { Module } from '../../types';
import { ChevronLeft, ChevronRight, CircuitBoard, CheckCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useCircuitStore } from '../../stores/circuitStore';
import { cn } from '../../lib/utils';

interface LessonViewerProps {
  module: Module;
  onComplete: () => void;
}

export default function LessonViewer({ module, onComplete }: LessonViewerProps) {
  const [currentSection, setCurrentSection] = useState(0);
  const sections = module.content_json.sections;
  const navigate = useNavigate();
  const setCircuit = useCircuitStore(state => state.setCircuit);

  const handleNext = () => {
    if (currentSection < sections.length - 1) {
      setCurrentSection(prev => prev + 1);
      window.scrollTo(0, 0);
    }
  };

  const handlePrev = () => {
    if (currentSection > 0) {
      setCurrentSection(prev => prev - 1);
      window.scrollTo(0, 0);
    }
  };

  const openExample = () => {
    if (module.content_json.circuit_example) {
      setCircuit(module.content_json.circuit_example);
      navigate('/circuit');
    }
  };

  const renderContent = (content: string) => {
    // Basic formatting: handle paragraphs, bold, math notation naive parsing
    return content.split('\n\n').map((paragraph, i) => (
      <p key={i} className="mb-4 text-gray-700 dark:text-gray-300 leading-relaxed"
         dangerouslySetInnerHTML={{
           __html: paragraph
             .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
             .replace(/\|(.*?)⟩/g, '<span class="font-mono bg-gray-100 dark:bg-gray-800 px-1 py-0.5 rounded">|$1⟩</span>')
         }}
      />
    ));
  };

  return (
    <div className="max-w-4xl mx-auto bg-white dark:bg-gray-900 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden">
      {/* Header & Progress */}
      <div className="p-6 border-b border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900/50">
        <h1 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-4">{module.title}</h1>
        <div className="flex items-center space-x-4">
          <div className="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div 
              className="bg-indigo-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${((currentSection + 1) / sections.length) * 100}%` }}
            ></div>
          </div>
          <span className="text-sm font-medium text-gray-500 dark:text-gray-400 whitespace-nowrap">
            Section {currentSection + 1} of {sections.length}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="p-8">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
          {sections[currentSection].title}
        </h2>
        
        <div className="prose dark:prose-invert max-w-none">
          {renderContent(sections[currentSection].content)}
        </div>

        {/* Try it out banner (show on relevant section if there's an example) */}
        {module.content_json.circuit_example && currentSection === Math.floor(sections.length / 2) && (
          <div className="mt-8 bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-100 dark:border-indigo-800 rounded-xl p-6 flex flex-col sm:flex-row items-center justify-between">
            <div>
              <h4 className="font-bold text-indigo-900 dark:text-indigo-300 mb-1">Interactive Example</h4>
              <p className="text-sm text-indigo-700 dark:text-indigo-400">See this concept in action in the Circuit Builder.</p>
            </div>
            <button 
              onClick={openExample}
              className="mt-4 sm:mt-0 flex items-center px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium text-sm"
            >
              <CircuitBoard className="w-4 h-4 mr-2" />
              Try in Builder
            </button>
          </div>
        )}
      </div>

      {/* Footer Navigation */}
      <div className="p-6 border-t border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900/50 flex items-center justify-between">
        <button
          onClick={handlePrev}
          disabled={currentSection === 0}
          className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg disabled:opacity-50 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          <ChevronLeft className="w-4 h-4 mr-2" /> Previous
        </button>

        {currentSection === sections.length - 1 ? (
          <button
            onClick={onComplete}
            className="flex items-center px-6 py-2 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 transition-colors"
          >
            Mark Complete <CheckCircle className="w-4 h-4 ml-2" />
          </button>
        ) : (
          <button
            onClick={handleNext}
            className="flex items-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Next <ChevronRight className="w-4 h-4 ml-2" />
          </button>
        )}
      </div>
    </div>
  );
}

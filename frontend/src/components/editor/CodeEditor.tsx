import Editor from '@monaco-editor/react';
import { useThemeStore } from '../../stores/themeStore';
import { Play, Sparkles, Copy, Check } from 'lucide-react';
import { useState } from 'react';

interface CodeEditorProps {
  code: string;
  onChange?: (val: string) => void;
  onRun?: (code: string) => void;
  readOnly?: boolean;
}

export default function CodeEditor({ code, onChange, onRun, readOnly = false }: CodeEditorProps) {
  const { theme } = useThemeStore();
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex flex-col h-full border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden">
      <div className="bg-gray-100 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 p-2 flex justify-between items-center">
        <span className="text-sm font-mono text-gray-600 dark:text-gray-400 ml-2">circuit.py</span>
        <div className="flex space-x-2">
          <button 
            onClick={handleCopy}
            className="p-1.5 text-gray-500 hover:text-gray-900 dark:hover:text-white hover:bg-gray-200 dark:hover:bg-gray-800 rounded transition-colors"
            title="Copy Code"
          >
            {copied ? <Check className="w-4 h-4 text-green-500" /> : <Copy className="w-4 h-4" />}
          </button>
          {!readOnly && onRun && (
            <button 
              onClick={() => onRun(code)}
              className="flex items-center px-3 py-1 bg-green-600 text-white text-sm font-medium rounded hover:bg-green-700 transition-colors"
            >
              <Play className="w-3.5 h-3.5 mr-1.5" /> Run
            </button>
          )}
        </div>
      </div>
      <div className="flex-1">
        <Editor
          height="100%"
          defaultLanguage="python"
          theme={theme === 'dark' ? 'vs-dark' : 'light'}
          value={code}
          onChange={(val) => onChange?.(val || '')}
          options={{
            readOnly,
            minimap: { enabled: false },
            fontSize: 14,
            fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
            scrollBeyondLastLine: false,
          }}
        />
      </div>
    </div>
  );
}

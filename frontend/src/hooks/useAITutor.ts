import { useState } from 'react';
import { ai } from '../lib/api';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export type AIMode = 'explain' | 'debug' | 'generate';

export function useAITutor() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const ask = async (
    question: string,
    context: string,
    difficulty: string = 'Beginner',
    mode: AIMode = 'explain'
  ) => {
    setIsLoading(true);
    setError(null);
    const newMessages = [...messages, { role: 'user' as const, content: question }];
    setMessages(newMessages);

    try {
      let answer = '';
      if (mode === 'debug') {
        const res = await ai.debugCircuit({
          circuit_json: context || '{}',
          error_msg: question,
        });
        answer = res.data.answer || res.data.explanation || '';
      } else if (mode === 'generate') {
        const res = await ai.generateCode({ description: question });
        answer = res.data.code || res.data.answer || '';
      } else {
        const res = await ai.explainConcept({
          question,
          context,
          mode: difficulty,
        });
        answer = res.data.answer || res.data.explanation || '';
      }
      setMessages([...newMessages, { role: 'assistant', content: answer }]);
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      const msg = typeof detail === 'string' ? detail : 'Failed to get AI response';
      setError(msg);
      setMessages([
        ...newMessages,
        { role: 'assistant', content: `Sorry — ${msg}` },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearMessages = () => {
    setMessages([]);
    setError(null);
  };

  return { ask, messages, isLoading, error, clearMessages };
}

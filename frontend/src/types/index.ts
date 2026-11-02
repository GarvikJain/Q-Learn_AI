export interface User {
  id: string;
  email: string;
  username: string;
  role: 'student'|'instructor'|'admin';
  is_active: boolean;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface Module {
  id: string;
  slug: string;
  title: string;
  description: string;
  order_index: number;
  content_json: ModuleContent;
}

export interface ModuleContent {
  objectives: string[];
  sections: Section[];
  key_terms: string[];
  circuit_example?: CircuitJSON;
  summary: string;
}

export interface Section {
  title: string;
  content: string;
}

export interface Gate {
  type: string;
  targets: number[];
  control?: number;
  controls?: number[];
  step: number;
}

export interface CircuitJSON {
  num_qubits: number;
  gates: Gate[];
  metadata?: Record<string,any>;
}

export interface Circuit {
  id: string;
  user_id: string;
  title: string;
  circuit_json: CircuitJSON;
  created_at: string;
}

export interface SimulationResult {
  counts: Record<string,number>;
  statevector?: number[][];
  probabilities: Record<string,number>;
  execution_time_ms: number;
  backend_used: string;
  num_qubits: number;
}

export interface Progress {
  module_id: string;
  status: 'not_started'|'in_progress'|'completed';
  quiz_score?: number;
  quiz_attempts: number;
  time_spent_minutes: number;
  last_accessed?: string;
}

export interface QuizQuestion {
  id: string;
  question_text: string;
  question_type: 'mcq'|'coding';
  options?: string[];
}

export interface Quiz {
  id: string;
  module_id: string;
  title: string;
  questions: QuizQuestion[];
}

export interface QuizFeedbackItem {
  is_correct: boolean;
  correct_answer?: string;
  explanation?: string;
}

export interface QuizResult {
  score: number;
  max_score: number;
  percentage: number;
  feedback: Record<string, QuizFeedbackItem | boolean>;
}

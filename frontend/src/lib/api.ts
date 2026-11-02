import axios from 'axios';
import { useAuthStore } from '../stores/authStore';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const auth = {
  login: (data: any) => api.post('/auth/login', data),
  register: (data: any) => api.post('/auth/register', data),
  getMe: () => api.get('/auth/me'),
};

export const modules = {
  getModules: () => api.get('/modules'),
  getModule: (slug: string) => api.get(`/modules/${slug}`),
};

export const circuits = {
  saveCircuit: (data: any) => api.post('/circuits', data),
  getCircuits: () => api.get('/circuits'),
  getCircuit: (id: string) => api.get(`/circuits/${id}`),
  updateCircuit: (id: string, data: any) => api.put(`/circuits/${id}`, data),
  deleteCircuit: (id: string) => api.delete(`/circuits/${id}`),
};

export const simulate = {
  runSimulation: (data: any) => api.post('/simulate', data),
};

export const ai = {
  explainConcept: (data: any) => api.post('/ai/explain', data),
  debugCircuit: (data: any) => api.post('/ai/debug', data),
  generateCode: (data: any) => api.post('/ai/generate-code', data),
};

export const quizzes = {
  getQuiz: (module_slug: string) => api.get(`/quizzes/${module_slug}`),
  submitQuiz: (module_slug: string, answers: any) => api.post(`/quizzes/${module_slug}/submit`, answers),
};

export const progress = {
  getProgress: () => api.get('/progress'),
  updateProgress: (slug: string, data: any) => api.put(`/progress/${slug}`, data),
  getProgressSummary: () => api.get('/progress/summary'),
  getInstructorLearners: () => api.get('/progress/instructor/learners'),
};

export default api;

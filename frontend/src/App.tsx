import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './stores/authStore';
import { useThemeStore } from './stores/themeStore';

// Layout
import AppLayout from './components/layout/AppLayout';

// Pages
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import LessonPage from './pages/LessonPage';
import CircuitBuilderPage from './pages/CircuitBuilderPage';
import SimulationPage from './pages/SimulationPage';
import AITutorPage from './pages/AITutorPage';
import QuizPage from './pages/QuizPage';
import ProgressPage from './pages/ProgressPage';
import InstructorPage from './pages/InstructorPage';
import ProfilePage from './pages/ProfilePage';
import NotFoundPage from './pages/NotFoundPage';

const ProtectedRoute = ({ children, role }: { children: React.ReactNode, role?: string }) => {
  const { isAuthenticated, user } = useAuthStore();
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (role && user?.role !== role && user?.role !== 'admin') return <Navigate to="/dashboard" replace />;
  return <>{children}</>;
};

export default function App() {
  const { theme } = useThemeStore();

  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  const { isAuthenticated } = useAuthStore();

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={isAuthenticated ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        
        <Route element={<AppLayout />}>
          <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
          <Route path="/learn/:slug" element={<ProtectedRoute><LessonPage /></ProtectedRoute>} />
          <Route path="/circuit" element={<ProtectedRoute><CircuitBuilderPage /></ProtectedRoute>} />
          <Route path="/circuit/:id" element={<ProtectedRoute><CircuitBuilderPage /></ProtectedRoute>} />
          <Route path="/simulate" element={<ProtectedRoute><SimulationPage /></ProtectedRoute>} />
          <Route path="/ai-tutor" element={<ProtectedRoute><AITutorPage /></ProtectedRoute>} />
          <Route path="/quizzes/:slug" element={<ProtectedRoute><QuizPage /></ProtectedRoute>} />
          <Route path="/progress" element={<ProtectedRoute><ProgressPage /></ProtectedRoute>} />
          <Route path="/instructor" element={<ProtectedRoute role="instructor"><InstructorPage /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
        </Route>

        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}

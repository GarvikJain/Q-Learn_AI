import { useState } from 'react';
import { useAuthStore } from '../stores/authStore';
import { auth } from '../lib/api';
import { useNavigate } from 'react-router-dom';

export function useAuth() {
  const { setUser, setToken, logout: zustandLogout, isAuthenticated } = useAuthStore();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const loginWithCredentials = async (email: string, password: string) => {
    const form = new URLSearchParams();
    form.append('username', email);
    form.append('password', password);
    const res = await auth.login(form);
    setToken(res.data.access_token);
    const meRes = await auth.getMe();
    setUser(meRes.data);
    navigate('/dashboard');
  };

  const login = async (data: any) => {
    setLoading(true);
    setError(null);
    try {
      // Accept either URLSearchParams (LoginForm) or plain object
      if (data instanceof URLSearchParams) {
        const res = await auth.login(data);
        setToken(res.data.access_token);
        const meRes = await auth.getMe();
        setUser(meRes.data);
        navigate('/dashboard');
      } else {
        await loginWithCredentials(data.username || data.email, data.password);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const register = async (data: any) => {
    setLoading(true);
    setError(null);
    try {
      await auth.register(data);
      // OAuth2 password flow: username field = email
      await loginWithCredentials(data.email, data.password);
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      setError(typeof detail === 'string' ? detail : 'Registration failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    zustandLogout();
    navigate('/login');
  };

  return { login, register, logout, isAuthenticated, loading, error };
}

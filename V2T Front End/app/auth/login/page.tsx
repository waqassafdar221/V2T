'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { authAPI, LoginData } from '@/lib/api';
import styles from './Login.module.css';
import Link from 'next/link';

export default function LoginPage() {
  const router = useRouter();
  const [formData, setFormData] = useState<LoginData>({
    username_or_email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      console.log('Attempting login...');
      const response = await authAPI.login(formData);
      console.log('Login successful:', response.data);
      
      // Store token and user info in localStorage
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      
      // Also store token in cookie for middleware
      document.cookie = `token=${response.data.access_token}; path=/; max-age=86400; SameSite=Lax`;
      
      console.log('Redirecting to dashboard...');
      // Redirect to dashboard
      router.push('/dashboard');
    } catch (err: any) {
      console.error('Login error:', err);
      // Handle validation errors from FastAPI
      const detail = err.response?.data?.detail;
      if (Array.isArray(detail)) {
        const errorMessages = detail.map((e: any) => e.msg || e.message).join(', ');
        setError(errorMessages || 'Validation error occurred');
      } else if (typeof detail === 'string') {
        setError(detail);
      } else {
        setError('Login failed. Please try again.');
      }
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.formCard}>
        <h1 className={styles.title}>Welcome Back</h1>
        <p className={styles.subtitle}>Sign in to continue to V2T</p>

        {error && <div className={styles.error}>{error}</div>}

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.formGroup}>
            <label htmlFor="username_or_email">Username or Email</label>
            <input
              type="text"
              id="username_or_email"
              value={formData.username_or_email}
              onChange={(e) => setFormData({ ...formData, username_or_email: e.target.value })}
              required
              placeholder="Enter username or email"
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              required
              placeholder="Enter password"
            />
          </div>

          <button type="submit" className={styles.submitBtn} disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div className={styles.footer}>
          <p>Don't have an account? <Link href="/auth/signup">Sign up</Link></p>
        </div>
      </div>
    </div>
  );
}

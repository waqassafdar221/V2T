'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { authAPI, VerifyOTPData } from '@/lib/api';
import styles from './VerifyOTP.module.css';

function VerifyOTPContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const emailFromQuery = searchParams.get('email') || '';

  const [formData, setFormData] = useState<VerifyOTPData>({
    email: emailFromQuery,
    otp: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [resending, setResending] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      await authAPI.verifyOTP(formData);
      setSuccess('Email verified successfully! Redirecting to login...');
      
      setTimeout(() => {
        router.push('/auth/login');
      }, 2000);
    } catch (err: any) {
      // Handle validation errors from FastAPI
      const detail = err.response?.data?.detail;
      if (Array.isArray(detail)) {
        const errorMessages = detail.map((e: any) => e.msg || e.message).join(', ');
        setError(errorMessages || 'Validation error occurred');
      } else if (typeof detail === 'string') {
        setError(detail);
      } else {
        setError('OTP verification failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleResendOTP = async () => {
    setError('');
    setSuccess('');
    setResending(true);

    try {
      await authAPI.resendOTP(formData.email);
      setSuccess('OTP has been resent to your email!');
    } catch (err: any) {
      // Handle validation errors from FastAPI
      const detail = err.response?.data?.detail;
      if (Array.isArray(detail)) {
        const errorMessages = detail.map((e: any) => e.msg || e.message).join(', ');
        setError(errorMessages || 'Validation error occurred');
      } else if (typeof detail === 'string') {
        setError(detail);
      } else {
        setError('Failed to resend OTP. Please try again.');
      }
    } finally {
      setResending(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.formCard}>
        <h1 className={styles.title}>Verify Your Email</h1>
        <p className={styles.subtitle}>
          We've sent a verification code to <strong>{formData.email}</strong>
        </p>

        {error && <div className={styles.error}>{error}</div>}
        {success && <div className={styles.success}>{success}</div>}

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.formGroup}>
            <label htmlFor="otp">Enter OTP Code</label>
            <input
              type="text"
              id="otp"
              value={formData.otp}
              onChange={(e) => setFormData({ ...formData, otp: e.target.value })}
              required
              placeholder="Enter 6-digit code"
              maxLength={6}
              className={styles.otpInput}
            />
          </div>

          <button type="submit" className={styles.submitBtn} disabled={loading}>
            {loading ? 'Verifying...' : 'Verify Email'}
          </button>
        </form>

        <div className={styles.resendSection}>
          <p>Didn't receive the code?</p>
          <button 
            onClick={handleResendOTP} 
            className={styles.resendBtn}
            disabled={resending}
          >
            {resending ? 'Resending...' : 'Resend OTP'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default function VerifyOTPPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <VerifyOTPContent />
    </Suspense>
  );
}

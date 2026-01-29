'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { videoAPI, VideoStatus } from '@/lib/api';
import styles from './VideoStatus.module.css';

export default function VideoStatusPage() {
  const router = useRouter();
  const params = useParams();
  const videoId = params.videoId as string;

  const [status, setStatus] = useState<VideoStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [polling, setPolling] = useState(true);

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/auth/login');
      return;
    }

    fetchStatus();
  }, [videoId]);

  useEffect(() => {
    if (!polling) return;

    const interval = setInterval(() => {
      fetchStatus();
    }, 3000); // Poll every 3 seconds

    return () => clearInterval(interval);
  }, [polling]);

  const fetchStatus = async () => {
    try {
      const response = await videoAPI.getStatus(videoId);
      console.log('Status response:', response.data);
      console.log('Status value:', response.data.status);
      console.log('Is COMPLETED?', response.data.status === 'COMPLETED');
      setStatus(response.data);
      setLoading(false);

      // If completed, stop polling (don't fetch results here - user will click button)
      if (response.data.status === 'completed') {
        setPolling(false);
        console.log('Processing completed! Button should appear now.');
      }

      // If failed, stop polling
      if (response.data.status === 'failed') {
        setPolling(false);
      }
    } catch (err: any) {
      console.error('Status fetch error:', err);
      setError(err.response?.data?.detail || 'Failed to fetch video status');
      setLoading(false);
      setPolling(false);
    }
  };

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>Loading video status...</div>
      </div>
    );
  }

  if (error && !status) {
    return (
      <div className={styles.container}>
        <div className={styles.error}>{error}</div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.navbar}>
        <div className={styles.navContent}>
          <h1 className={styles.logo}>V2T Dashboard</h1>
          <button onClick={() => router.push('/dashboard')} className={styles.backBtn}>
            ← Back to Dashboard
          </button>
        </div>
      </div>

      <main className={styles.main}>
        <div className={styles.content}>
          <div className={styles.header}>
            <h2>Video Processing Status</h2>
            <p>Video ID: {videoId}</p>
          </div>

          {status && (
            <div className={styles.statusCard}>
              <div className={styles.statusHeader}>
                <h3>Current Status</h3>
                <span className={`${styles.statusBadge} ${styles[status.status.toLowerCase()]}`}>
                  {status.status}
                </span>
              </div>

              <div className={styles.progressSection}>
                <div className={styles.progressBar}>
                  <div 
                    className={styles.progressFill}
                    style={{ width: `${status.progress || 0}%` }}
                  />
                </div>
                <p className={styles.progressText}>{status.progress || 0}% Complete</p>
              </div>

              <p className={styles.statusMessage}>{status.message}</p>

              {status.error_message && (
                <div className={styles.errorMessage}>
                  <strong>Error:</strong> {status.error_message}
                </div>
              )}

              {console.log('Checking button condition - status:', status.status)}
              {status.status === 'completed' && (
                <div className={styles.successMessage}>
                  <p>✓ Processing completed!</p>
                  <button 
                    onClick={() => {
                      console.log('Check Results button clicked!');
                      router.push(`/dashboard/video/${videoId}/results`);
                    }}
                    className={styles.checkResultsBtn}
                  >
                    Check Results
                  </button>
                </div>
              )}
            </div>
          )}

          {error && <div className={styles.error}>{error}</div>}
        </div>
      </main>
    </div>
  );
}

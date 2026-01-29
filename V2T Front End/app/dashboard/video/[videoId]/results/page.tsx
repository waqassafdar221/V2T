'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { videoAPI, VideoResults } from '@/lib/api';
import styles from './Results.module.css';

export default function VideoResultsPage() {
  const router = useRouter();
  const params = useParams();
  const videoId = params.videoId as string;

  const [results, setResults] = useState<VideoResults | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [exporting, setExporting] = useState(false);

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/auth/login');
      return;
    }

    fetchResults();
  }, [videoId]);

  const fetchResults = async () => {
    try {
      const response = await videoAPI.getResults(videoId);
      console.log('Fetched results:', response.data);
      setResults(response.data);
      setLoading(false);
    } catch (err: any) {
      console.error('Failed to fetch results:', err);
      setError(err.response?.data?.detail || 'Failed to load results');
      setLoading(false);
    }
  };

  const handleExport = async (format: 'txt' | 'pdf') => {
    setExporting(true);
    try {
      const response = await videoAPI.exportResults(videoId, format);
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `video_${videoId}_results.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      console.error('Export error:', err);
      setError(`Failed to export results as ${format.toUpperCase()}`);
    } finally {
      setExporting(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this video and all its data?')) {
      return;
    }

    try {
      await videoAPI.delete(videoId);
      router.push('/dashboard');
    } catch (err: any) {
      setError('Failed to delete video');
    }
  };

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>Loading results...</div>
      </div>
    );
  }

  if (error && !results) {
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
          <div className={styles.error}>{error}</div>
        </main>
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
            <h2>Video Processing Results</h2>
            <p className={styles.videoId}>Video ID: {videoId}</p>
          </div>

          {results && (
            <>
              {/* Summary Card */}
              <div className={styles.summaryCard}>
                <h3>Processing Summary</h3>
                <div className={styles.summaryGrid}>
                  <div className={styles.summaryItem}>
                    <span className={styles.summaryLabel}>Filename</span>
                    <span className={styles.summaryValue}>{results.filename}</span>
                  </div>
                  <div className={styles.summaryItem}>
                    <span className={styles.summaryLabel}>Total Frames</span>
                    <span className={styles.summaryValue}>{results.total_frames}</span>
                  </div>
                  <div className={styles.summaryItem}>
                    <span className={styles.summaryLabel}>Objects Detected</span>
                    <span className={styles.summaryValue}>{results.detected_objects.length}</span>
                  </div>
                  <div className={styles.summaryItem}>
                    <span className={styles.summaryLabel}>Texts Extracted</span>
                    <span className={styles.summaryValue}>{results.extracted_texts.length}</span>
                  </div>
                  {results.fps && (
                    <div className={styles.summaryItem}>
                      <span className={styles.summaryLabel}>FPS</span>
                      <span className={styles.summaryValue}>{results.fps.toFixed(2)}</span>
                    </div>
                  )}
                  {results.duration && (
                    <div className={styles.summaryItem}>
                      <span className={styles.summaryLabel}>Duration</span>
                      <span className={styles.summaryValue}>{results.duration.toFixed(2)}s</span>
                    </div>
                  )}
                </div>
              </div>

              {/* Results Section */}
              <div className={styles.resultsSection}>
                <div className={styles.resultsCard}>
                  <h3>Detected Objects ({results.detected_objects.length})</h3>
                  <div className={styles.resultsList}>
                    {results.detected_objects.length > 0 ? (
                      results.detected_objects.slice(0, 10).map((obj, idx) => (
                        <div key={idx} className={styles.resultItem}>
                          <span className={styles.resultLabel}>
                            Frame {obj.frame_number} ({obj.timestamp.toFixed(2)}s)
                          </span>
                          <span className={styles.resultValue}>
                            {obj.object_class} - {(obj.confidence * 100).toFixed(1)}%
                          </span>
                        </div>
                      ))
                    ) : (
                      <p className={styles.noData}>No objects detected</p>
                    )}
                    {results.detected_objects.length > 10 && (
                      <p className={styles.moreText}>
                        + {results.detected_objects.length - 10} more objects...
                      </p>
                    )}
                  </div>
                </div>

                <div className={styles.resultsCard}>
                  <h3>Extracted Texts ({results.extracted_texts.length})</h3>
                  <div className={styles.resultsList}>
                    {results.extracted_texts.length > 0 ? (
                      results.extracted_texts.slice(0, 10).map((text, idx) => (
                        <div key={idx} className={styles.resultItem}>
                          <span className={styles.resultLabel}>
                            Frame {text.frame_number} ({text.timestamp.toFixed(2)}s)
                          </span>
                          <span className={styles.resultValue}>
                            "{text.text}" - {(text.confidence * 100).toFixed(1)}%
                          </span>
                        </div>
                      ))
                    ) : (
                      <p className={styles.noData}>No text extracted</p>
                    )}
                    {results.extracted_texts.length > 10 && (
                      <p className={styles.moreText}>
                        + {results.extracted_texts.length - 10} more texts...
                      </p>
                    )}
                  </div>
                </div>
              </div>

              {/* Export Actions */}
              <div className={styles.actions}>
                <h3>Export Results</h3>
                <div className={styles.actionButtons}>
                  <button 
                    onClick={() => handleExport('txt')} 
                    className={styles.exportBtn}
                    disabled={exporting}
                  >
                    📄 Export as Text
                  </button>
                  <button 
                    onClick={() => handleExport('pdf')} 
                    className={styles.exportBtn}
                    disabled={exporting}
                  >
                    📕 Export as PDF
                  </button>
                  <button 
                    onClick={handleDelete} 
                    className={styles.deleteBtn}
                    disabled={exporting}
                  >
                    🗑️ Delete Video
                  </button>
                </div>
              </div>
            </>
          )}

          {error && <div className={styles.error}>{error}</div>}
        </div>
      </main>
    </div>
  );
}

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { videoAPI, VideoUploadResponse } from '@/lib/api';
import styles from './Dashboard.module.css';

interface User {
  name: string;
  email: string;
  username: string;
  role: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadedVideo, setUploadedVideo] = useState<VideoUploadResponse | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');

    if (!token || !userData) {
      router.push('/auth/login');
      return;
    }

    setUser(JSON.parse(userData));
  }, [router]);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file type
      const allowedTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/mkv', 'video/flv', 'video/wmv'];
      if (!allowedTypes.includes(file.type) && !file.name.match(/\.(mp4|avi|mov|mkv|flv|wmv)$/i)) {
        setError('Invalid file type. Please upload a video file.');
        return;
      }

      // Validate file size (500MB max)
      const maxSize = 500 * 1024 * 1024;
      if (file.size > maxSize) {
        setError('File size exceeds 500MB limit.');
        return;
      }

      setSelectedFile(file);
      setError('');
      setUploadedVideo(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setError('');
    setUploadProgress(0);

    try {
      const response = await videoAPI.upload(selectedFile);
      setUploadedVideo(response.data);
      setUploadProgress(100);
      
      // Redirect to video status page after 2 seconds
      setTimeout(() => {
        router.push(`/dashboard/video/${response.data.video_id}`);
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.');
      setUploadProgress(0);
    } finally {
      setUploading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    router.push('/');
  };

  if (!user) {
    return <div className={styles.loading}>Loading...</div>;
  }

  return (
    <div className={styles.container}>
      <nav className={styles.navbar}>
        <div className={styles.navContent}>
          <h1 className={styles.logo}>V2T Dashboard</h1>
          <div className={styles.navRight}>
            <span className={styles.userName}>Welcome, {user.name}</span>
            <button onClick={handleLogout} className={styles.logoutBtn}>
              Logout
            </button>
          </div>
        </div>
      </nav>

      <main className={styles.main}>
        <div className={styles.content}>
          <div className={styles.header}>
            <h2>Upload Video for Processing</h2>
            <p>Upload a video file to extract text and detect objects using AI</p>
          </div>

          <div className={styles.uploadSection}>
            <div className={styles.uploadCard}>
              <div className={styles.uploadArea}>
                <input
                  type="file"
                  id="video-upload"
                  accept="video/*"
                  onChange={handleFileSelect}
                  className={styles.fileInput}
                />
                <label htmlFor="video-upload" className={styles.fileLabel}>
                  <svg className={styles.uploadIcon} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                  <span className={styles.uploadText}>
                    {selectedFile ? selectedFile.name : 'Click to select video file'}
                  </span>
                  <span className={styles.uploadHint}>
                    Supported: MP4, AVI, MOV, MKV, FLV, WMV (Max 500MB)
                  </span>
                </label>
              </div>

              {selectedFile && (
                <div className={styles.fileInfo}>
                  <p><strong>File:</strong> {selectedFile.name}</p>
                  <p><strong>Size:</strong> {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB</p>
                </div>
              )}

              {error && <div className={styles.error}>{error}</div>}

              {uploadedVideo && (
                <div className={styles.success}>
                  <p>✓ Video uploaded successfully!</p>
                  <p>Video ID: {uploadedVideo.video_id}</p>
                  <p>Redirecting to processing status...</p>
                </div>
              )}

              {uploadProgress > 0 && uploadProgress < 100 && (
                <div className={styles.progressBar}>
                  <div 
                    className={styles.progressFill} 
                    style={{ width: `${uploadProgress}%` }}
                  />
                </div>
              )}

              <button
                onClick={handleUpload}
                disabled={!selectedFile || uploading}
                className={styles.uploadBtn}
              >
                {uploading ? 'Uploading...' : 'Upload and Process Video'}
              </button>
            </div>

            <div className={styles.infoCard}>
              <h3>How it works</h3>
              <ol className={styles.stepsList}>
                <li>Select and upload your video file</li>
                <li>Our AI will process the video in the background</li>
                <li>Extract frames and detect objects using YOLO</li>
                <li>Perform OCR text extraction from frames</li>
                <li>View and export the results</li>
              </ol>

              <div className={styles.features}>
                <h4>Features</h4>
                <ul>
                  <li>✓ Object detection with bounding boxes</li>
                  <li>✓ Text extraction with confidence scores</li>
                  <li>✓ Frame-by-frame analysis</li>
                  <li>✓ Export results in multiple formats</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

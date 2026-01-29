import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/auth/login';
    }
    return Promise.reject(error);
  }
);

// Types
export interface SignupData {
  name: string;
  username: string;
  email: string;
  password: string;
  role: 'Student' | 'Teacher' | 'Others';
}

export interface LoginData {
  username_or_email: string;
  password: string;
}

export interface VerifyOTPData {
  email: string;
  otp: string;
}

export interface User {
  id: number;
  name: string;
  username: string;
  email: string;
  role: string;
  is_verified: boolean;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface VideoUploadResponse {
  video_id: string;
  filename: string;
  file_size: number;
  status: string;
  message: string;
}

export interface VideoStatus {
  video_id: string;
  status: string;
  progress: number;
  message: string;
  error_message?: string;
}

export interface DetectedObject {
  frame_number: number;
  timestamp: number;
  object_class: string;
  confidence: number;
  bbox: {
    x1: number;
    y1: number;
    x2: number;
    y2: number;
  };
}

export interface ExtractedText {
  frame_number: number;
  timestamp: number;
  text: string;
  confidence: number;
}

export interface VideoResults {
  video_id: string;
  filename: string;
  status: string;
  duration?: number;
  fps?: number;
  total_frames: number;
  detected_objects: DetectedObject[];
  extracted_texts: ExtractedText[];
  error_message?: string;
  created_at: string;
  completed_at?: string;
}

// Auth API
export const authAPI = {
  signup: (data: SignupData) => api.post('/auth/signup', data),
  
  verifyOTP: (data: VerifyOTPData) => api.post('/auth/verify-otp', data),
  
  login: (data: LoginData) => api.post<AuthResponse>('/auth/login', data),
  
  resendOTP: (email: string) => api.post('/auth/resend-otp', null, { params: { email } }),
};

// Video API
export const videoAPI = {
  upload: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post<VideoUploadResponse>('/video/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  getStatus: (videoId: string) => api.get<VideoStatus>(`/video/status/${videoId}`),
  
  getResults: (videoId: string) => api.get<VideoResults>(`/video/results/${videoId}`),
  
  delete: (videoId: string) => api.delete(`/video/delete/${videoId}`),
  
  exportResults: (videoId: string, format: 'txt' | 'json' | 'csv' | 'pdf') => 
    api.get(`/video/export/${videoId}/${format}`, {
      responseType: 'blob',
    }),
  
  listVideos: () => api.get('/video/list'),
};

export default api;

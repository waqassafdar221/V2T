import { ReactNode } from 'react';

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large';
  message?: string;
}

export default function LoadingSpinner({ size = 'medium', message }: LoadingSpinnerProps) {
  const sizeClasses = {
    small: 'w-6 h-6 border-2',
    medium: 'w-12 h-12 border-3',
    large: 'w-16 h-16 border-4',
  };

  return (
    <div style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center', 
      justifyContent: 'center',
      gap: '16px'
    }}>
      <div style={{
        width: size === 'small' ? '24px' : size === 'medium' ? '48px' : '64px',
        height: size === 'small' ? '24px' : size === 'medium' ? '48px' : '64px',
        border: `${size === 'small' ? '2px' : size === 'medium' ? '3px' : '4px'} solid #f3f3f3`,
        borderTop: `${size === 'small' ? '2px' : size === 'medium' ? '3px' : '4px'} solid #667eea`,
        borderRadius: '50%',
        animation: 'spin 1s linear infinite',
      }} />
      {message && (
        <p style={{ 
          fontSize: '14px', 
          color: '#666',
          margin: 0
        }}>
          {message}
        </p>
      )}
      <style jsx>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

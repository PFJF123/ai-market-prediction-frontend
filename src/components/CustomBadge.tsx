'use client';

interface CustomBadgeProps {
  children: React.ReactNode;
  color?: 'gray' | 'red' | 'yellow' | 'green' | 'blue' | 'indigo';
  size?: 'xs' | 'sm' | 'md' | 'lg';
  className?: string;
}

export default function CustomBadge({ 
  children, 
  color = 'gray', 
  size = 'md',
  className = '' 
}: CustomBadgeProps) {
  const colorClasses = {
    gray: 'bg-gray-100 text-gray-700',
    red: 'bg-red-100 text-red-700',
    yellow: 'bg-yellow-100 text-yellow-700',
    green: 'bg-green-100 text-green-700',
    blue: 'bg-blue-100 text-blue-700',
    indigo: 'bg-indigo-100 text-indigo-700'
  };

  const sizeClasses = {
    xs: 'px-2 py-0.5 text-xs',
    sm: 'px-2.5 py-0.5 text-sm',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-1.5 text-base'
  };

  return (
    <span className={`inline-flex items-center rounded-full font-medium ${colorClasses[color]} ${sizeClasses[size]} ${className}`}>
      {children}
    </span>
  );
}

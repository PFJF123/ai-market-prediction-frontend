import { useState, useEffect } from 'react';

export function useFallbackData<T>(data: T | undefined, fallback: T): T {
  const [fallbackData, setFallbackData] = useState<T>(fallback);

  useEffect(() => {
    if (data !== undefined) {
      setFallbackData(data);
    }
  }, [data]);

  return data ?? fallbackData;
}
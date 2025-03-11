import { useState, useEffect } from 'react';
import axios, { AxiosResponse, AxiosError } from 'axios';

// Get API URL from environment variables with fallback
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://ai-market-prediction-production.up.railway.app';

// Response interface for API calls
export interface ApiResponse<T> {
  data: T | null;
  error: Error | null;
  response: AxiosResponse<T> | null;
  status: number | null;
}

// State interface for components using API data
export interface ApiState<T> {
  data: T | null;
  isLoading: boolean;
  error: Error | null;
  errorMessage: string | null;
  status: number | null;
}

/**
 * Hook for making GET requests to the API
 * @param endpoint API endpoint path (e.g., '/api/v1/health')
 * @param params Optional query parameters
 * @returns ApiResponse object with data, error, and response
 */
export function useApiGet<T>(endpoint: string, params?: Record<string, any>): ApiResponse<T> {
  const [response, setResponse] = useState<ApiResponse<T>>({
    data: null,
    error: null,
    response: null,
    status: null
  });

  useEffect(() => {
    let isMounted = true;
    
    const fetchData = async () => {
      try {
        const result = await axios.get<T>(`${API_URL}${endpoint}`, { 
          params,
          timeout: 10000 // 10 second timeout
        });
        
        if (isMounted) {
          setResponse({
            data: result.data,
            error: null,
            response: result,
            status: result.status
          });
        }
      } catch (error) {
        if (isMounted) {
          const axiosError = error as AxiosError;
          setResponse({
            data: null,
            error: new Error(axiosError.message || 'An unknown error occurred'),
            response: null,
            status: axiosError.response?.status || null
          });
        }
      }
    };

    fetchData();
    
    // Cleanup function to prevent state updates on unmounted component
    return () => {
      isMounted = false;
    };
  }, [endpoint, JSON.stringify(params)]);

  return response;
}

/**
 * Helper hook to extract API state from API response
 * @param apiResponse Response from useApiGet
 * @returns Structured state for components
 */
export function useApiState<T>(apiResponse: ApiResponse<T>): ApiState<T> {
  return {
    data: apiResponse.data,
    isLoading: !apiResponse.data && !apiResponse.error,
    error: apiResponse.error,
    errorMessage: apiResponse.error?.message || null,
    status: apiResponse.status
  };
}

'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Card, Title, Text, Badge } from '@tremor/react';
To https://github.com/PFJF123/ai-market-prediction.git
   f7e9d98..3484cff  main -> main
import { useApiGet, useApiState } from '@/hooks/useApi';
import { useFallbackData } from '@/hooks/useFallbackData';
import { Trend } from '@/types/api';
import LoadingSpinner from './LoadingSpinner';
import ErrorAlert from './ErrorAlert';
import CustomBadge from './CustomBadge';

interface TrendingTopicsProps {
  className?: string;
  limit?: number;
}

export default function TrendingTopics({ className = '', limit = 5 }: TrendingTopicsProps) {
  const [isClient, setIsClient] = useState(false);
  
  // Fetch trending topics
  const trendsResponse = useApiGet<Trend[]>('/api/trends', { 
    is_active: true,
    limit: limit
  });
  
  const { data: apiTrends, isLoading, error, errorMessage } = useApiState(trendsResponse);
  
  // Use fallback data if API fails
  const { data: trends, isFallback, fallbackReason } = useFallbackData<Trend[]>(
    apiTrends, 
    isLoading, 
    error ? error : null, 
    'trends', 
    limit
  );

  // Function to get badge color based on sentiment
  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'bullish':
        return 'green';
      case 'bearish':
        return 'red';
      default:
        return 'gray';
    }
  };

  const getSentimentText = (sentiment: string) => {
    switch (sentiment) {
      case 'bullish':
        return 'Bullish';
      case 'bearish':
        return 'Bearish';
      default:
        return 'Neutral';
    }
  };
  
  // Handle hydration issues by only rendering on client
  useEffect(() => {
    setIsClient(true);
  }, []);
  
  if (!isClient) {
    return null;
  }

  return (
    <Card>
      <div className="flex justify-between items-center mb-4">
        <div>
          <Title>Trending Topics</Title>
          <Text>Most active market trends</Text>
        </div>
        <Link 
          href="/trends" 
          className="text-sm text-primary-600 hover:text-primary-800 font-medium"
        >
          View All →
        </Link>
      </div>
      
      {isLoading ? (
        <div className="flex justify-center items-center py-12">
          <LoadingSpinner size="lg" />
        </div>
      ) : error && !isFallback ? (
        <ErrorAlert message={errorMessage || "Failed to load trending topics"} />
      ) : (
        <>
          {isFallback && (
            <div className="mb-4 p-2 bg-yellow-50 border border-yellow-200 rounded-md">
              <Text className="text-sm text-yellow-700">
                <span className="font-medium">Using cached data:</span> {fallbackReason}
              </Text>
            </div>
          )}
          
          {trends && trends.length > 0 ? (
            <div className="space-y-4">
              {trends.map((topic) => (
                <div key={topic.id}>
                  <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center w-full">
                    <div className="flex flex-col">
                      <Link 
                        href={`/trends/${topic.id}`}
                        className="font-medium hover:text-primary-600"
                      >
                        {topic.name}
                      </Link>
                      <div className="flex flex-wrap gap-2 mt-1">
                        {topic.keywords.map((keyword, index) => (
                          <CustomBadge key={index} color="blue" size="sm">
                            {keyword}
                          </CustomBadge>
                        ))}
                      </div>
                      <div className="flex items-center mt-1 space-x-2">
                        {topic.sentiment_history.length > 0 && (
                          <>
                            <CustomBadge 
                              color={getSentimentColor(topic.sentiment_history[topic.sentiment_history.length - 1].sentiment)}
                              size="sm"
                            >
                              {getSentimentText(topic.sentiment_history[topic.sentiment_history.length - 1].sentiment)}
                            </CustomBadge>
                            <Text className="text-xs text-gray-500">
                              Score: {topic.sentiment_history[topic.sentiment_history.length - 1].score > 0 ? '+' : ''}
                              {topic.sentiment_history[topic.sentiment_history.length - 1].score.toFixed(2)}
                            </Text>
                          </>
                        )}
                      </div>
                    </div>
                    
                    <div className="mt-2 sm:mt-0 flex flex-wrap gap-1">
                      {topic.related_sectors.slice(0, 2).map((sector) => (
                        <CustomBadge key={sector} color="blue" size="xs">
                          {sector}
                        </CustomBadge>
                      ))}
                      {topic.related_stocks.slice(0, 3).map((stock) => (
                        <CustomBadge key={stock} color="indigo" size="xs">
                          {stock}
                        </CustomBadge>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="py-8 text-center">
              <Text>No trending topics found</Text>
              <Link 
                href="/trends/create" 
                className="inline-block mt-2 text-sm text-primary-600 hover:text-primary-800 font-medium"
              >
                Create a new trend
              </Link>
            </div>
          )}
        </>
      )}
    </Card>
  );
} 
'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Card, Title, Text, Badge } from '@tremor/react';
import { useApiGet, useApiState, ApiResponse } from '@/hooks/useApi';
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
  const apiResponse = useApiGet<Trend[]>('/api/v1/trends');
  const { data: trends, isLoading, error, errorMessage } = useApiState(apiResponse);
  
  // Use fallback data if API fails
  const fallbackTrends: Trend[] = [];
  const displayTrends = useFallbackData<Trend[]>(trends || undefined, fallbackTrends);

  useEffect(() => {
    setIsClient(true);
  }, []);

  if (!isClient) {
    return null;
  }

  if (isLoading) {
    return (
      <Card className={className}>
        <div className="flex items-center justify-center p-4">
          <LoadingSpinner size="lg" />
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className={className}>
        <ErrorAlert
          title="Error Loading Trends"
          message={errorMessage || "Unable to load market trends. Please try again later."}
        />
      </Card>
    );
  }

  const renderTopic = (topic: Trend) => {
    const sentimentColor = topic.sentiment > 0 ? 'green' : topic.sentiment < 0 ? 'red' : 'gray';
    const confidenceLevel = topic.confidence >= 0.7 ? 'high' : topic.confidence >= 0.4 ? 'medium' : 'low';

    return (
      <div key={topic.topic} className="mb-4 last:mb-0">
        <div className="flex items-center justify-between mb-2">
          <Title className="text-lg font-semibold">{topic.topic}</Title>
          <CustomBadge color={sentimentColor} size="sm">
            {(topic.sentiment * 100).toFixed(1)}%
          </CustomBadge>
        </div>
        
        <div className="flex flex-wrap gap-2 mb-2">
          {topic.keywords.map((keyword: string, index: number) => (
            <Badge key={`${keyword}-${index}`} color="blue" size="sm">
              {keyword}
            </Badge>
          ))}
        </div>

        <div className="flex flex-wrap gap-2">
          <div className="flex flex-wrap gap-1">
            <Text className="text-sm text-gray-600">Sectors:</Text>
            {topic.sectors.map((sector: string) => (
              <Link key={sector} href={`/sectors/${sector.toLowerCase()}`} className="text-sm text-blue-600 hover:underline">
                {sector}
              </Link>
            ))}
          </div>
          <div className="flex flex-wrap gap-1">
            <Text className="text-sm text-gray-600">Stocks:</Text>
            {topic.stocks.map((stock: string) => (
              <Link key={stock} href={`/stocks/${stock.toLowerCase()}`} className="text-sm text-blue-600 hover:underline">
                {stock}
              </Link>
            ))}
          </div>
        </div>
      </div>
    );
  };

  return (
    <Card className={className}>
      <div className="flex items-center justify-between mb-4">
        <Title>Market Trends</Title>
        <CustomBadge color={!error ? 'green' : 'red'} size="sm">
          {!error ? 'Connected' : 'Disconnected'}
        </CustomBadge>
      </div>
      <div className="divide-y">
        {displayTrends.slice(0, limit).map(renderTopic)}
      </div>
    </Card>
  );
}
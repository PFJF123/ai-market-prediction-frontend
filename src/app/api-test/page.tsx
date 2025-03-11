'use client';

import { useState, useEffect } from 'react';
import { Card, Title, Text, Grid, Badge, Flex, Metric } from '@tremor/react';
import { useApiGet, useApiState } from '@/hooks/useApi';
import LoadingSpinner from '@/components/LoadingSpinner';
import ErrorAlert from '@/components/ErrorAlert';

interface HealthStatus {
  status: string;
  timestamp: string;
  version: string;
  environment?: string;
  database: {
    mongodb: string | boolean;
    status?: {
      connected: boolean;
      last_attempt: string | null;
      attempts: number;
      max_attempts: number;
    };
  };
  trace_id?: string;
}

export default function ApiTestPage() {
  const [isClient, setIsClient] = useState(false);

  // Fetch API health status
  const healthResponse = useApiGet<HealthStatus>('/api/v1/health');
  const { data: health, isLoading, error, errorMessage } = useApiState(healthResponse);

  // Function to get badge color based on status
  const getStatusColor = (status: string | boolean) => {
    if (typeof status === 'boolean') {
      return status ? 'green' : 'red';
    }
    
    switch (String(status).toLowerCase()) {
      case 'healthy':
      case 'connected':
        return 'green';
      case 'degraded':
        return 'yellow';
      default:
        return 'red';
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
    <main className="p-4 md:p-10 mx-auto max-w-7xl">
      <Title>API Health Monitor</Title>
      <Text>Check the status of the AI Market Prediction API</Text>

      {isLoading ? (
        <div className="flex justify-center items-center py-12">
          <LoadingSpinner size="lg" />
        </div>
      ) : error ? (
        <ErrorAlert 
          title="API Health Check Failed"
          message={errorMessage || "Failed to check API health. Please try again later."} 
          className="mt-4"
        />
      ) : health ? (
        <Grid numItems={1} numItemsSm={2} numItemsLg={3} className="gap-6 mt-6">
          <Card>
            <Title>API Status</Title>
            <Flex className="mt-4">
              <Badge color={getStatusColor(health.status)}>
                {health.status}
              </Badge>
              {health.environment && (
                <Text>{health.environment}</Text>
              )}
            </Flex>
            <Text className="mt-2">Version: {health.version}</Text>
            {health.trace_id && (
              <Text className="mt-2 text-xs text-gray-500">Trace ID: {health.trace_id}</Text>
            )}
          </Card>

          <Card>
            <Title>Database Status</Title>
            <Flex className="mt-4">
              <Badge color={getStatusColor(health.database.mongodb)}>
                {typeof health.database.mongodb === 'boolean' 
                  ? (health.database.mongodb ? 'Connected' : 'Disconnected')
                  : health.database.mongodb}
              </Badge>
            </Flex>
            {health.database.status && (
              <>
                {health.database.status.last_attempt && (
                  <Text className="mt-2">
                    Last attempt: {new Date(health.database.status.last_attempt).toLocaleString()}
                  </Text>
                )}
                <Text className="mt-2">
                  Connection attempts: {health.database.status.attempts} / {health.database.status.max_attempts}
                </Text>
              </>
            )}
          </Card>

          <Card>
            <Title>Last Updated</Title>
            <Metric className="mt-4">
              {new Date(health.timestamp).toLocaleTimeString()}
            </Metric>
            <Text className="text-xs text-gray-500">
              {new Date(health.timestamp).toLocaleDateString()}
            </Text>
          </Card>
        </Grid>
      ) : null}
    </main>
  );
}
'use client';

import { useState, useEffect } from 'react';
import { Card, Title, Text, Grid } from '@tremor/react';
import { useApiGet, useApiState } from '@/hooks/useApi';
import LoadingSpinner from '@/components/LoadingSpinner';
import ErrorAlert from '@/components/ErrorAlert';

export default function DebugPage() {
  const [isClient, setIsClient] = useState(false);

  // Handle hydration issues by only rendering on client
  useEffect(() => {
    setIsClient(true);
  }, []);

  if (!isClient) {
    return null;
  }

  return (
    <main className="p-4 md:p-10 mx-auto max-w-7xl">
      <Title>Debug Page</Title>
      <Text>This page is for debugging purposes</Text>
      
      <Grid numItems={1} className="gap-6 mt-6">
        <Card>
          <Title>Environment Variables</Title>
          <Text className="mt-4">
            API URL: {process.env.NEXT_PUBLIC_API_URL || 'https://ai-market-prediction-production.up.railway.app'}
          </Text>
        </Card>
      </Grid>
    </main>
  );
}
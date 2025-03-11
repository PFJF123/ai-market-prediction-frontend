'use client';

import { useState, useEffect } from 'react';
import { Container, Typography, Grid, CircularProgress, Box } from '@mui/material';
import axios from 'axios';

interface MarketTrend {
  topic: string;
  sentiment: number;
  volume: number;
  timestamp: string;
  sources: string[];
}

export default function TrendsPage() {
  const [trends, setTrends] = useState<MarketTrend[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://ai-market-prediction-production.up.railway.app';

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`${apiUrl}/api/v1/trends`);
        setTrends(response.data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch market trends');
        setTrends([]);
      } finally {
        setLoading(false);
      }
    };

    fetchTrends();
    const interval = setInterval(fetchTrends, 60000); // Refresh every minute

    return () => clearInterval(interval);
  }, [apiUrl]);

  if (loading) {
    return (
      <Container maxWidth="lg" className="py-8">
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" className="py-8">
        <Typography color="error" gutterBottom>
          Error: {error}
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" className="py-8">
      <Typography variant="h4" component="h1" gutterBottom>
        Market Trends
      </Typography>

      <Grid container spacing={3}>
        {trends.map((trend, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <div className="trend-card">
              <Typography variant="h6" className="trend-title">
                {trend.topic}
              </Typography>
              <div className="flex justify-between items-center mb-2">
                <Typography variant="body2" color="textSecondary">
                  Sentiment: {(trend.sentiment * 100).toFixed(1)}%
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Volume: {trend.volume}
                </Typography>
              </div>
              <Typography variant="caption" className="trend-description">
                Last updated: {new Date(trend.timestamp).toLocaleString()}
              </Typography>
              <Typography variant="caption" display="block" className="mt-2 text-gray-500">
                Sources: {trend.sources.join(', ')}
              </Typography>
            </div>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}
'use client';

import { Box, Container, Typography, Button } from '@mui/material';
import Link from 'next/link';

export default function HomePage() {
  return (
    <Container maxWidth="lg" className="py-8">
      <Box className="text-center">
        <Typography variant="h2" component="h1" gutterBottom>
          AI Market Prediction
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom className="text-gray-600 dark:text-gray-300">
          Discover market trends through AI-powered news analysis
        </Typography>

        <Box className="mt-8 space-y-4">
          <Link href="/trends" passHref>
            <Button variant="contained" color="primary" size="large" className="w-full sm:w-auto">
              View Market Trends
            </Button>
          </Link>

          <Link href="/api-test" passHref>
            <Button variant="outlined" color="primary" size="large" className="w-full sm:w-auto ml-0 sm:ml-4">
              Check API Status
            </Button>
          </Link>
        </Box>
      </Box>
    </Container>
  );
}
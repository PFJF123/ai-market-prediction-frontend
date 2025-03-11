# AI Market Prediction Frontend

Next.js frontend application for visualizing market trends and predictions based on AI analysis of financial news.

## Production Deployment

The application is deployed on Vercel at:
https://frontend-c0gyw24lh-justoms-projects.vercel.app

## Features

- Real-time market trend visualization
- News-based market sentiment analysis
- API health monitoring dashboard
- Fallback data handling for API outages
- Responsive design for all devices

## Backend Integration

The application integrates with our FastAPI backend deployed on Railway:
https://ai-market-prediction-production.up.railway.app

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Run development server:
```bash
npm run dev
```

3. Build for production:
```bash
npm run build
```

## Environment Variables

Required environment variables in `.env` or Vercel:

- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_APP_ENV`: Environment (development/production)
- `NEXT_PUBLIC_LOG_LEVEL`: Logging level

## Project Structure

```
src/
├── app/                # Next.js pages
│   ├── api-test/      # API monitoring page
│   ├── debug/         # Debug utilities
│   └── trends/        # Market trends visualization
├── components/        # React components
├── context/          # React context providers
├── hooks/            # Custom React hooks
└── utils/           # Utility functions
```

## Testing

```bash
npm run test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License
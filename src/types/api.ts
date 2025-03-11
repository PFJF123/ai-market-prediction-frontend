export interface Trend {
  topic: string;
  sentiment: number;
  confidence: number;
  keywords: string[];
  sectors: string[];
  stocks: string[];
  timestamp: string;
}

export interface ApiResponse<T> {
  data: T;
  status: string;
  timestamp: string;
}

export interface HealthCheck {
  status: string;
  version: string;
  database: {
    mongodb: string;
  };
  trace_id: string;
  timestamp: string;
}

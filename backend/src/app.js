import express from 'express';
import cors from 'cors';
import config from './config/index.js';
import health from './routes/health.js';
import { notFound, errorHandler } from './middleware/errors.js';

const app = express();

app.use(cors({ origin: config.corsOrigin }));
app.use(express.json({ limit: '1mb' }));

app.use('/api/v1/health', health);

app.use(notFound);
app.use(errorHandler);

export default app;

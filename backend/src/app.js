const express = require('express');
const cors = require('cors');
const config = require('./config');
const health = require('./routes/health');
const { notFound, errorHandler } = require('./middleware/errors');

const app = express();

app.use(cors({ origin: config.corsOrigin }));
app.use(express.json({ limit: '1mb' }));

app.use('/api/v1/health', health);

app.use(notFound);
app.use(errorHandler);

module.exports = app;

import mongoose from 'mongoose';
import app from './app.js';
import config from './config/index.js';

await mongoose.connect(config.mongodbUri);
app.listen(config.port, () => {
  console.log(`Canopia API in ascolto sulla porta ${config.port}`);
});

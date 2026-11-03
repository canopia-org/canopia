// Processo separato per i job pianificati (D3, C-07). I job vengono aggiunti con T-04.
import mongoose from 'mongoose';
import config from './config/index.js';

await mongoose.connect(config.mongodbUri);
console.log('Canopia worker avviato');

// Processo separato per i job pianificati (D3, C-07). I job vengono aggiunti con T-04.
const mongoose = require('mongoose');
const config = require('./config');

async function main() {
  await mongoose.connect(config.mongodbUri);
  console.log('Canopia worker avviato');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

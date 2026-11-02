const mongoose = require('mongoose');
const app = require('./app');
const config = require('./config');

async function main() {
  await mongoose.connect(config.mongodbUri);
  app.listen(config.port, () => {
    console.log(`Canopia API in ascolto sulla porta ${config.port}`);
  });
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

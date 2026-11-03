import express from 'express';
import { readFileSync } from 'node:fs';

const { version } = JSON.parse(readFileSync(new URL('../../package.json', import.meta.url)));
const router = express.Router();

router.get('/', (req, res) => {
  res.json({ stato: 'ok', versione: version });
});

export default router;

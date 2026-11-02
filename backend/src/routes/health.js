const express = require('express');
const { version } = require('../../package.json');

const router = express.Router();

router.get('/', (req, res) => {
  res.json({ stato: 'ok', versione: version });
});

module.exports = router;

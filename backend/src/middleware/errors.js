export function notFound(req, res) {
  res.status(404).json({ codice: 'NON_TROVATO', messaggio: 'Risorsa non trovata' });
}

// Express 5 inoltra qui anche gli errori delle funzioni async, senza try/catch nelle rotte.
// eslint-disable-next-line no-unused-vars
export function errorHandler(err, req, res, next) {
  const status = err.status || 500;
  if (status >= 500) console.error(err);
  res.status(status).json({
    codice: err.codice || 'ERRORE_INTERNO',
    messaggio: status >= 500 ? 'Errore interno' : err.message,
  });
}

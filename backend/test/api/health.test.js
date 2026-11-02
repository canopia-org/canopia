const request = require('supertest');
const app = require('../../src/app');

describe('GET /api/v1/health', () => {
  test('risponde 200 con lo stato del servizio', async () => {
    const res = await request(app).get('/api/v1/health');
    expect(res.status).toBe(200);
    expect(res.body.stato).toBe('ok');
  });

  test('una rotta inesistente risponde 404 nel formato di errore comune', async () => {
    const res = await request(app).get('/api/v1/inesistente');
    expect(res.status).toBe(404);
    expect(res.body.codice).toBe('NON_TROVATO');
  });
});

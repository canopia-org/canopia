import { http, HttpResponse } from 'msw';

const API = import.meta.env.VITE_API_URL || 'http://localhost:3000/api/v1';

// Risposte simulate dell'API, conformi a api/openapi.yaml. Usate dai test e da `npm run dev:mock`.
export const handlers = [
  http.get(`${API}/health`, () => HttpResponse.json({ stato: 'ok', versione: '0.1.0' })),
];

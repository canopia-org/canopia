const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api/v1';

export async function get(path) {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) throw new Error(`Errore ${res.status}`);
  return res.json();
}

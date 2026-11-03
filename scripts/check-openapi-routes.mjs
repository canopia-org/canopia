/**
 * Confronto statico tra le rotte Express del backend e api/openapi.yaml.
 *
 * Legge come testo backend/src/app.js e backend/src/routes/*.js:
 * - in app.js, `app.use('/api/v1/<prefisso>', <router>)` con il router importato da ./routes/<file>.js;
 * - in ogni file di rotte, `router.<metodo>('<percorso>', ...)`.
 * Ricostruisce le coppie `METODO /percorso` (con `:param` convertito in `{param}`) e le confronta
 * con i percorsi e i metodi dichiarati nella specifica.
 *
 * Uso: `npm run openapi:routes`. Esce con codice 1 se una rotta implementata non è nella specifica.
 * Gli endpoint della specifica non ancora implementati sono solo elencati: vengono realizzati sprint dopo sprint.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = join(ROOT, 'backend', 'src');
const SPEC = join(ROOT, 'api', 'openapi.yaml');
const BASE = '/api/v1';
const METODI = ['get', 'post', 'put', 'patch', 'delete'];

function normalizza(percorso) {
  const p = percorso.replace(/\/+/g, '/').replace(/(.)\/$/, '$1');
  return p.replace(/:([A-Za-z0-9_]+)/g, '{$1}');
}

function rotteImplementate() {
  const app = readFileSync(join(SRC, 'app.js'), 'utf8');
  const importati = new Map();
  for (const m of app.matchAll(/import\s+(\w+)\s+from\s+'\.\/routes\/([\w-]+)\.js'/g)) {
    importati.set(m[1], m[2]);
  }
  const montaggi = new Map();
  for (const m of app.matchAll(/app\.use\(\s*'([^']+)'\s*,\s*(\w+)\s*\)/g)) {
    const file = importati.get(m[2]);
    if (file) montaggi.set(file, m[1]);
  }
  const rotte = new Set();
  for (const nome of readdirSync(join(SRC, 'routes'))) {
    if (!nome.endsWith('.js')) continue;
    const file = nome.replace(/\.js$/, '');
    const prefisso = montaggi.get(file);
    if (!prefisso) continue;
    const testo = readFileSync(join(SRC, 'routes', nome), 'utf8');
    for (const m of testo.matchAll(/router\.(get|post|put|patch|delete)\(\s*'([^']*)'/g)) {
      const completo = normalizza(`${prefisso}/${m[2]}`);
      rotte.add(`${m[1].toUpperCase()} ${completo.slice(BASE.length) || '/'}`);
    }
  }
  return rotte;
}

function rotteSpecifica() {
  const righe = readFileSync(SPEC, 'utf8').split('\n');
  const rotte = new Set();
  let inPaths = false;
  let percorso = null;
  for (const riga of righe) {
    if (/^paths:/.test(riga)) inPaths = true;
    else if (/^\S/.test(riga)) inPaths = false;
    if (!inPaths) continue;
    const p = riga.match(/^ {2}(\/\S*):\s*$/);
    if (p) percorso = p[1];
    const m = riga.match(/^ {4}(\w+):/);
    if (percorso && m && METODI.includes(m[1])) rotte.add(`${m[1].toUpperCase()} ${percorso}`);
  }
  return rotte;
}

const implementate = rotteImplementate();
const specifica = rotteSpecifica();
const nonDocumentate = [...implementate].filter((r) => !specifica.has(r));
const daImplementare = [...specifica].filter((r) => !implementate.has(r));

console.log(`Rotte implementate: ${implementate.size} · nella specifica: ${specifica.size}`);
console.log(`Ancora da implementare: ${daImplementare.length}`);
if (nonDocumentate.length) {
  console.error('Rotte implementate ma assenti da api/openapi.yaml:');
  for (const r of nonDocumentate) console.error(`  ${r}`);
  process.exit(1);
}
console.log('Ogni rotta implementata è documentata in api/openapi.yaml.');

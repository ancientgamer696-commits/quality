import { test } from 'node:test';
import assert from 'node:assert/strict';
import worker from '../src/index.mjs';

const env = { DEPLOYMENT_STAGE: 'development', ALLOWED_ORIGINS: 'https://quality-glass-shop.pages.dev,https://quality-glass-manager.pages.dev' };
const req = (path, opts = {}) => new Request(`https://example.workers.dev${path}`, opts);

test('read-only health check exposes no secret or customer data', async () => {
  const res = await worker.fetch(req('/health'), env);
  assert.equal(res.status, 200);
  assert.deepEqual(await res.json(), { ok: true, service: 'quality-glass-api', stage: 'development', dbConfigured: false });
});

test('catalog refuses traffic until a real D1 database is configured', async () => {
  const res = await worker.fetch(req('/api/v1/products'), env);
  assert.equal(res.status, 503);
  assert.equal((await res.json()).code, 'DB_NOT_CONFIGURED');
});

test('write and admin attempts are not available', async () => {
  const res = await worker.fetch(req('/api/v1/orders', { method: 'POST' }), env);
  assert.equal(res.status, 405);
  assert.equal((await worker.fetch(req('/api/v1/admin/orders'), env)).status, 404);
});

test('CORS is explicit per owner-provided Pages origin', async () => {
  const good = await worker.fetch(req('/health', { headers: { Origin: 'https://quality-glass-shop.pages.dev' } }), env);
  assert.equal(good.headers.get('Access-Control-Allow-Origin'), 'https://quality-glass-shop.pages.dev');
  const bad = await worker.fetch(req('/health', { headers: { Origin: 'https://other.example' } }), env);
  assert.equal(bad.headers.get('Access-Control-Allow-Origin'), null);
  const preflight = await worker.fetch(req('/api/v1/products', { method: 'OPTIONS', headers: { Origin: 'https://other.example' } }), env);
  assert.equal(preflight.status, 403);
});

test('category parameter uses validation and SQL binding', async () => {
  const capture = [];
  const db = { prepare(sql) { capture.push(sql); return { bind(category) { capture.push(category); return this; }, async all() { return { results: [] }; } }; } };
  assert.equal((await worker.fetch(req('/api/v1/products?category=bad%27--'), { ...env, DB: db })).status, 400);
  const res = await worker.fetch(req('/api/v1/products?category=landscapes'), { ...env, DB: db });
  assert.equal(res.status, 200);
  assert.deepEqual(capture.slice(-1), ['landscapes']);
});

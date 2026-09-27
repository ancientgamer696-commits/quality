// Safe read-only foundation. No authentication, payment, uploads, or admin routes.
// DO NOT add writes without production auth/RBAC, server validation, idempotency
// and private file storage. Customer/shop HTML demos do not call this Worker yet.
const json = (value, status = 200, headers = {}) => new Response(JSON.stringify(value), {
  status,
  headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...headers },
});

function corsHeaders(request, env) {
  const origin = request.headers.get('Origin');
  const list = (env.ALLOWED_ORIGINS || '').split(',').map((o) => o.trim()).filter(Boolean);
  // No wildcard: origins of the two Pages sites will be added explicitly AFTER
  // Cloudflare assigns their actual pages.dev hostnames.
  return origin && list.includes(origin) ? {
    'Access-Control-Allow-Origin': origin,
    'Vary': 'Origin',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '600',
  } : {};
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const cors = corsHeaders(request, env);
    const origin = request.headers.get('Origin');
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: origin && cors['Access-Control-Allow-Origin'] ? 204 : 403, headers: cors });
    }
    if (request.method !== 'GET') return json({ error: 'Method not allowed', code: 'METHOD_NOT_ALLOWED' }, 405, cors);
    if (url.pathname === '/health') {
      return json({ ok: true, service: 'quality-glass-api', stage: env.DEPLOYMENT_STAGE || 'unknown', dbConfigured: !!env.DB }, 200, cors);
    }
    if (!['/api/v1/categories', '/api/v1/products'].includes(url.pathname)) {
      return json({ error: 'Not found', code: 'NOT_FOUND' }, 404, cors);
    }
    if (!env.DB) return json({ error: 'Development database not connected yet', code: 'DB_NOT_CONFIGURED' }, 503, cors);
    try {
      if (url.pathname === '/api/v1/categories') {
        const { results } = await env.DB.prepare('SELECT slug, name, description FROM categories WHERE is_published = 1 ORDER BY sort_order, name LIMIT 50').all();
        return json({ data: results }, 200, cors);
      }
      let sql = 'SELECT p.slug, p.name, p.summary, p.price_paise, p.category_slug, p.featured FROM products p WHERE p.is_published = 1';
      const category = url.searchParams.get('category');
      if (category && !/^[a-z0-9-]{1,50}$/.test(category)) return json({ error: 'Invalid category', code: 'INVALID_CATEGORY' }, 400, cors);
      if (category) sql += ' AND p.category_slug = ?';
      sql += ' ORDER BY p.featured DESC, p.sort_order, p.name LIMIT 48';
      const stmt = env.DB.prepare(sql);
      const { results } = await (category ? stmt.bind(category) : stmt).all();
      return json({ data: results }, 200, cors);
    } catch (_) {
      // Never echo SQL or infrastructure errors to public clients.
      return json({ error: 'Service temporarily unavailable', code: 'DATA_UNAVAILABLE' }, 503, cors);
    }
  },
};

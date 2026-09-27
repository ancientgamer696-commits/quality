-- Development schema only. Real order/payment schemas require auth and private media.
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS categories (
  slug TEXT PRIMARY KEY CHECK(length(slug) BETWEEN 1 AND 50),
  name TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  sort_order INTEGER NOT NULL DEFAULT 0,
  is_published INTEGER NOT NULL DEFAULT 0 CHECK(is_published IN (0, 1))
);
CREATE TABLE IF NOT EXISTS products (
  id TEXT PRIMARY KEY,
  slug TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  summary TEXT NOT NULL DEFAULT '',
  category_slug TEXT NOT NULL REFERENCES categories(slug),
  price_paise INTEGER NOT NULL CHECK(price_paise >= 0),
  featured INTEGER NOT NULL DEFAULT 0 CHECK(featured IN (0, 1)),
  sort_order INTEGER NOT NULL DEFAULT 0,
  is_published INTEGER NOT NULL DEFAULT 0 CHECK(is_published IN (0, 1))
);
CREATE INDEX IF NOT EXISTS idx_products_public ON products(is_published, category_slug, featured, sort_order);
-- No seed products: the old website's displayed prices and art are not assumed
-- to be accurate/owned. Publish only after the owner supplies validated SKUs.

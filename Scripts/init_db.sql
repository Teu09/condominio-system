
-- init_db.sql - cria tabelas básicas para demo

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  full_name TEXT,
  role TEXT DEFAULT 'resident',
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS units (
  id SERIAL PRIMARY KEY,
  block TEXT,
  number TEXT,
  owner_id INTEGER REFERENCES users(id),
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS visitors (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  document TEXT NOT NULL,
  unit_id INTEGER REFERENCES units(id),
  visit_date TIMESTAMP NOT NULL,
  expected_duration INTEGER DEFAULT 120,
  purpose TEXT NOT NULL,
  contact_phone TEXT,
  status TEXT DEFAULT 'scheduled',
  check_in TIMESTAMP,
  check_out TIMESTAMP,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS reservations (
  id SERIAL PRIMARY KEY,
  unit_id INTEGER REFERENCES units(id),
  area TEXT,
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS maintenance_orders (
  id SERIAL PRIMARY KEY,
  unit_id INTEGER REFERENCES units(id),
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  priority TEXT DEFAULT 'medium',
  category TEXT NOT NULL,
  requested_by INTEGER REFERENCES users(id),
  status TEXT DEFAULT 'open',
  expected_date TIMESTAMP,
  assigned_to TEXT,
  completed_date TIMESTAMP,
  created_at TIMESTAMP DEFAULT now()
);

-- seed admin user (email: admin@condo.local / password: admin)
INSERT INTO users (email, password, full_name, role)
VALUES ('admin@condo.local', 'admin', 'Administrador do Condomínio', 'admin')
ON CONFLICT (email) DO NOTHING;

-- seed some sample data for testing
INSERT INTO units (block, number, owner_id) VALUES
('A', '101', 1),
('A', '102', NULL),
('B', '201', NULL),
('B', '202', NULL)
ON CONFLICT DO NOTHING;

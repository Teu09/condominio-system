
-- init_db.sql - cria tabelas básicas para demo

-- Tabela de condomínios (tenants)
CREATE TABLE IF NOT EXISTS tenants (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  cnpj TEXT UNIQUE NOT NULL,
  address TEXT NOT NULL,
  phone TEXT NOT NULL,
  email TEXT NOT NULL,
  theme_config JSONB,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT now()
);

-- Tabela de usuários com tenant_id
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  tenant_id INTEGER REFERENCES tenants(id),
  email TEXT NOT NULL,
  password TEXT NOT NULL,
  full_name TEXT,
  role TEXT DEFAULT 'resident',
  permissions JSONB DEFAULT '[]',
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT now(),
  UNIQUE(tenant_id, email)
);

CREATE TABLE IF NOT EXISTS units (
  id SERIAL PRIMARY KEY,
  tenant_id INTEGER REFERENCES tenants(id),
  block TEXT,
  number TEXT,
  owner_id INTEGER REFERENCES users(id),
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS visitors (
  id SERIAL PRIMARY KEY,
  tenant_id INTEGER REFERENCES tenants(id),
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
  tenant_id INTEGER REFERENCES tenants(id),
  unit_id INTEGER REFERENCES units(id),
  area TEXT,
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS maintenance_orders (
  id SERIAL PRIMARY KEY,
  tenant_id INTEGER REFERENCES tenants(id),
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

-- seed sample tenants
INSERT INTO tenants (name, cnpj, address, phone, email, theme_config) VALUES
('Condomínio Alphaline', '12.345.678/0001-90', 'Rua das Flores, 123', '(11) 99999-9999', 'contato@alphaline.com', '{"primary_color": "#1976d2", "secondary_color": "#dc004e", "background_color": "#f5f5f5", "text_color": "#333333"}'),
('Condomínio das Araras', '98.765.432/0001-10', 'Av. dos Pássaros, 456', '(11) 88888-8888', 'contato@araras.com', '{"primary_color": "#2e7d32", "secondary_color": "#ff6f00", "background_color": "#f1f8e9", "text_color": "#1b5e20"}')
ON CONFLICT (cnpj) DO NOTHING;

-- seed super admin (sem tenant_id = NULL para acesso global)
INSERT INTO users (tenant_id, email, password, full_name, role, permissions) VALUES
(NULL, 'superadmin@condosys.com', 'superadmin123', 'Super Administrador CondoSys', 'super_admin', '["all", "manage_tenants", "global_access"]')
ON CONFLICT (email) DO NOTHING;

-- seed admin users for each tenant
INSERT INTO users (tenant_id, email, password, full_name, role, permissions) VALUES
(1, 'admin@alphaline.com', 'admin', 'Administrador Alphaline', 'admin', '["all"]'),
(2, 'admin@araras.com', 'admin', 'Administrador das Araras', 'admin', '["all"]')
ON CONFLICT (tenant_id, email) DO NOTHING;

-- seed some sample data for testing
INSERT INTO units (tenant_id, block, number, owner_id) VALUES
(1, 'A', '101', 1),
(1, 'A', '102', NULL),
(1, 'B', '201', NULL),
(1, 'B', '202', NULL),
(2, 'A', '101', 2),
(2, 'A', '102', NULL),
(2, 'B', '201', NULL),
(2, 'B', '202', NULL)
ON CONFLICT DO NOTHING;

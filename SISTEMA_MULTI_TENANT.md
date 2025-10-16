# Sistema de Condomínios Multi-Tenant

## Visão Geral

Este sistema foi desenvolvido para ser vendido para múltiplos condomínios, onde cada condomínio tem sua própria identidade visual e configurações personalizadas.

## Características Principais

### 1. Multi-Tenancy
- Cada condomínio é um "tenant" isolado
- Dados completamente separados entre condomínios
- Sistema de permissões baseado em roles

### 2. Temas Personalizáveis
- Cada condomínio pode ter suas próprias cores
- Configuração de tema no cadastro do condomínio
- Aplicação automática do tema no login

### 3. Sistema de Permissões
- **Admin**: Acesso total ao sistema
- **Síndico**: Acesso a relatórios e gestão
- **Morador**: Acesso limitado às suas próprias informações

### 4. Cadastro de Condomínios
- Interface para cadastrar novos condomínios
- Criação automática do usuário administrador
- Configuração de tema personalizado

## Estrutura do Sistema

### Backend Services

1. **tenant_service** (Porta 8008)
   - Gerenciamento de condomínios
   - Configurações de tema
   - Cadastro de novos tenants

2. **auth_service** (Porta 8001)
   - Autenticação multi-tenant
   - JWT com informações do tenant
   - Validação de permissões

3. **user_service** (Porta 8002)
   - Gestão de usuários por tenant
   - Sistema de permissões

4. **unit_service** (Porta 8003)
   - Gestão de unidades por tenant

5. **reservation_service** (Porta 8004)
   - Reservas de áreas comuns por tenant

6. **visitor_service** (Porta 8005)
   - Controle de visitantes por tenant

7. **maintenance_service** (Porta 8006)
   - Ordens de manutenção por tenant

8. **reporting_service** (Porta 8007)
   - Relatórios por tenant

### Frontend
- Interface responsiva com temas dinâmicos
- Seleção de condomínio no login
- Cadastro de novos condomínios
- Aplicação automática de temas

## Como Usar

### 1. Cadastrar Novo Condomínio

1. Acesse a tela de login
2. Clique em "Cadastrar Novo Condomínio"
3. Preencha os dados do condomínio:
   - Nome do condomínio
   - CNPJ
   - Endereço
   - Telefone
   - Email
4. Configure o tema:
   - Cor primária
   - Cor secundária
5. Preencha os dados do administrador:
   - Nome completo
   - Email
   - Senha
6. Clique em "Cadastrar Condomínio"

### 2. Fazer Login

1. Selecione o condomínio na lista
2. Digite seu email e senha
3. O sistema aplicará automaticamente o tema do condomínio

### 3. Gerenciar Usuários

- Cada usuário pertence a um condomínio específico
- Permissões são definidas por role (admin, sindico, morador)
- Usuários só podem ver dados do seu próprio condomínio

## Configuração de Tema

Cada condomínio pode personalizar:
- **Cor Primária**: Usada em botões e elementos principais
- **Cor Secundária**: Usada em elementos de destaque
- **Cor de Fundo**: Cor de fundo da interface
- **Cor do Texto**: Cor principal do texto

## Exemplos de Condomínios

### Condomínio Alphaline
- Cor Primária: #1976d2 (Azul)
- Cor Secundária: #dc004e (Vermelho)
- Tema: Moderno e corporativo

### Condomínio das Araras
- Cor Primária: #2e7d32 (Verde)
- Cor Secundária: #ff6f00 (Laranja)
- Tema: Natural e acolhedor

## Segurança

- Isolamento completo de dados entre condomínios
- Autenticação JWT com informações do tenant
- Validação de permissões em todas as operações
- Senhas dos administradores são armazenadas de forma segura

## Desenvolvimento

### Adicionando Novos Serviços

1. Crie o serviço no diretório `Backend/`
2. Adicione `tenant_id` em todas as tabelas
3. Implemente validação de tenant nas operações
4. Adicione o serviço no `docker-compose.yml`
5. Configure o proxy no `nginx.conf`

### Modificando Temas

1. Edite as variáveis CSS no `index.html`
2. Atualize a função `applyTenantTheme()` no `app.js`
3. Modifique o schema `TenantThemeConfig` se necessário

## Deploy

1. Execute `docker-compose up -d`
2. Acesse `http://localhost:8080`
3. Cadastre o primeiro condomínio
4. Configure os usuários conforme necessário

## Suporte

Para dúvidas ou problemas, consulte a documentação técnica ou entre em contato com a equipe de desenvolvimento.

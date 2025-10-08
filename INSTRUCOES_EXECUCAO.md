# 🏢 Sistema de Condomínio - Instruções de Execução

## 📋 Pré-requisitos

Antes de executar o sistema, certifique-se de ter instalado:

1. **Docker Desktop** (versão 20.10 ou superior)
   - Download: https://www.docker.com/products/docker-desktop/
   - Certifique-se de que o Docker está rodando

2. **Docker Compose** (geralmente vem com o Docker Desktop)
   - Verifique com: `docker-compose --version`

## 🚀 Como Executar o Sistema

### 1. Navegue até o diretório do projeto
```bash
cd "condominio_system_fixed (1)"
```

### 2. Execute o sistema completo
```bash
docker-compose up --build
```

**O que este comando faz:**
- Constrói todas as imagens Docker dos serviços
- Inicia o banco de dados PostgreSQL
- Inicia todos os microserviços (7 serviços)
- Inicia o frontend com Nginx
- Configura automaticamente as dependências entre serviços

### 3. Aguarde a inicialização
O sistema levará alguns minutos para inicializar completamente. Você verá logs de todos os serviços no terminal.

**Indicadores de que está pronto:**
- Banco de dados: "database system is ready to accept connections"
- Serviços: "Application startup complete"
- Frontend: "nginx: [notice] ready for connections"

## 🌐 Acessando o Sistema

### Frontend (Interface Web)
- **URL:** http://localhost:8080
- **Login padrão:**
  - Email: `admin@condo.local`
  - Senha: `admin`

### APIs dos Serviços
- **Auth Service:** http://localhost:8001
- **User Service:** http://localhost:8002
- **Unit Service:** http://localhost:8003
- **Reservation Service:** http://localhost:8004
- **Visitor Service:** http://localhost:8005
- **Maintenance Service:** http://localhost:8006
- **Reporting Service:** http://localhost:8007

### Banco de Dados
- **Host:** localhost
- **Porta:** 5432
- **Database:** condominio
- **Usuário:** condo
- **Senha:** condopass

## 🔧 Comandos Úteis

### Parar o sistema
```bash
docker-compose down
```

### Parar e remover volumes (limpar dados)
```bash
docker-compose down -v
```

### Ver logs de um serviço específico
```bash
docker-compose logs auth_service
docker-compose logs user_service
# etc...
```

### Reconstruir apenas um serviço
```bash
docker-compose up --build auth_service
```

### Ver status dos containers
```bash
docker-compose ps
```

## 🏗️ Arquitetura do Sistema

O sistema é composto por:

1. **Frontend** (Nginx + HTML/JS)
   - Interface web responsiva
   - Comunicação com APIs via proxy

2. **Microserviços Backend:**
   - **Auth Service:** Autenticação e autorização
   - **User Service:** Gerenciamento de usuários/moradores
   - **Unit Service:** Gerenciamento de unidades
   - **Reservation Service:** Sistema de reservas
   - **Visitor Service:** Controle de visitantes
   - **Maintenance Service:** Ordens de manutenção
   - **Reporting Service:** Geração de relatórios

3. **Banco de Dados:**
   - PostgreSQL 15
   - Tabelas pré-configuradas
   - Usuário admin pré-cadastrado

## 🐛 Solução de Problemas

### Erro de porta em uso
Se alguma porta estiver em uso, pare outros serviços ou modifique as portas no `docker-compose.yml`.

### Erro de permissão no Windows
Execute o PowerShell como administrador.

### Serviços não iniciam
```bash
# Verifique os logs
docker-compose logs

# Reconstrua as imagens
docker-compose build --no-cache
docker-compose up
```

### Banco de dados não conecta
```bash
# Verifique se o PostgreSQL está rodando
docker-compose logs db

# Reinicie apenas o banco
docker-compose restart db
```

## 📊 Monitoramento

### Health Checks
Todos os serviços têm endpoints de health check:
- http://localhost:8001/health
- http://localhost:8002/health
- etc...

### Status dos Containers
```bash
docker-compose ps
```

## 🔒 Segurança

⚠️ **IMPORTANTE:** Este é um sistema de demonstração. Para produção:
- Altere todas as senhas padrão
- Configure HTTPS
- Implemente autenticação JWT adequada
- Configure firewall adequadamente

## 📝 Funcionalidades Disponíveis

### ✅ Implementadas
- Login/autenticação
- CRUD de usuários
- CRUD de unidades
- Sistema de reservas
- Interface web responsiva

### 🚧 Em Desenvolvimento
- Controle de visitantes
- Sistema de manutenção
- Geração de relatórios

## 🆘 Suporte

Se encontrar problemas:
1. Verifique os logs: `docker-compose logs`
2. Confirme que o Docker está rodando
3. Verifique se as portas não estão em uso
4. Tente reconstruir: `docker-compose up --build`

---

**Sistema pronto para uso! 🎉**

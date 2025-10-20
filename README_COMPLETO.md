# 🏢 Sistema de Condomínio Completo

Sistema completo de gerenciamento de condomínios com arquitetura de microserviços, incluindo todos os módulos solicitados.

## 🚀 Funcionalidades Implementadas

### ✅ **Sistemas Principais**
1. **Sistema de Orçamentos** - Orçamentos de compra e serviço com históricos
2. **Sistema de Eventos** - Cadastro de datas e eventos importantes
3. **Sistema de Reuniões** - Reuniões com históricos, emissão e envio por email
4. **Sistema de Atas** - Atas com históricos, emissão e envio por email
5. **Sistema de Funcionários** - Cadastro de funcionários com históricos
6. **Sistema de Documentos** - Cadastro de documentos por tipo
7. **Sistema de Patrimônio** - Cadastro de patrimônio com históricos
8. **Sistema de Avisos** - Avisos com históricos e quadro de avisos
9. **Sistema de Auditoria** - Logs de ações e auditoria
10. **Sistema de Prestadores de Serviço** - Cadastro de prestadores com históricos
11. **Sistema de Membros da Família** - Cadastro de membros da família
12. **Sistema de Notificações** - Notificações por email

### ✅ **Sistemas Existentes**
- Sistema de Autenticação
- Sistema de Usuários
- Sistema de Unidades
- Sistema de Reservas
- Sistema de Visitantes
- Sistema de Manutenção
- Sistema de Relatórios
- Sistema de Tenants

## 🏗️ Arquitetura

### **Microserviços (Backend)**
- **auth_service** (Porta 8001) - Autenticação e autorização
- **user_service** (Porta 8002) - Gerenciamento de usuários
- **unit_service** (Porta 8003) - Gerenciamento de unidades
- **reservation_service** (Porta 8004) - Reservas de áreas comuns
- **visitor_service** (Porta 8005) - Controle de visitantes
- **maintenance_service** (Porta 8006) - Ordens de manutenção
- **reporting_service** (Porta 8007) - Relatórios
- **tenant_service** (Porta 8008) - Gerenciamento de condomínios
- **budget_service** (Porta 8009) - Orçamentos
- **events_service** (Porta 8010) - Eventos
- **meetings_service** (Porta 8011) - Reuniões
- **minutes_service** (Porta 8012) - Atas
- **employees_service** (Porta 8013) - Funcionários
- **documents_service** (Porta 8014) - Documentos
- **assets_service** (Porta 8015) - Patrimônio
- **notices_service** (Porta 8016) - Avisos
- **audit_service** (Porta 8017) - Auditoria
- **service_providers_service** (Porta 8018) - Prestadores de serviço
- **family_members_service** (Porta 8019) - Membros da família
- **notifications_service** (Porta 8020) - Notificações

### **Frontend**
- **Frontend** (Porta 8080) - Interface web com Nginx

### **Banco de Dados**
- **PostgreSQL** (Porta 5432) - Banco principal

## 🛠️ Tecnologias Utilizadas

### **Backend**
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validação de dados
- **PostgreSQL** - Banco de dados relacional
- **Docker** - Containerização

### **Frontend**
- **HTML5/CSS3/JavaScript** - Interface web
- **Chart.js** - Gráficos e visualizações
- **Nginx** - Servidor web

## 📋 Pré-requisitos

- Docker
- Docker Compose
- Git

## 🚀 Como Executar

### 1. **Clone o Repositório**
```bash
git clone <url-do-repositorio>
cd condominio_system_fixed
```

### 2. **Configure as Variáveis de Ambiente**
```bash
# Copie o arquivo de exemplo
cp config.env.example .env

# Edite o arquivo .env com suas configurações
# Especialmente as configurações de SMTP para notificações
```

### 3. **Execute o Sistema**
```bash
# Inicie todos os serviços
docker-compose up -d

# Ou use o script de inicialização (se disponível)
./iniciar_sistema.bat
```

### 4. **Acesse o Sistema**
- **Frontend**: http://localhost:8080
- **Super Admin**: http://localhost:8080/super-admin.html
- **Demo**: http://localhost:8080/demo.html

## 🔧 Configuração de Email

Para usar o sistema de notificações, configure as variáveis de SMTP no arquivo `.env`:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=seu_email@gmail.com
SMTP_PASSWORD=sua_senha_app
SMTP_USE_TLS=true
```

## 📊 Funcionalidades por Sistema

### **Sistema de Orçamentos**
- Criação de orçamentos de compra e serviço
- Controle de itens e categorias
- Histórico de alterações
- Relatórios e estatísticas

### **Sistema de Eventos**
- Cadastro de eventos importantes
- Categorização por tipo e prioridade
- Controle de status e visibilidade
- Histórico de alterações

### **Sistema de Reuniões**
- Agendamento de reuniões
- Controle de participantes
- Emissão e envio de convites por email
- Histórico de reuniões

### **Sistema de Atas**
- Criação de atas de reuniões
- Controle de versões
- Emissão e envio por email
- Histórico de alterações

### **Sistema de Funcionários**
- Cadastro completo de funcionários
- Controle de dados pessoais e profissionais
- Histórico de movimentações
- Relatórios de funcionários

### **Sistema de Documentos**
- Cadastro por tipo de documento
- Controle de vencimento
- Categorização e organização
- Histórico de alterações

### **Sistema de Patrimônio**
- Cadastro de bens patrimoniais
- Controle de localização e status
- Histórico de movimentações
- Relatórios de patrimônio

### **Sistema de Avisos**
- Criação de avisos
- Quadro de avisos digital
- Controle de prioridade e visibilidade
- Sistema de visualizações

### **Sistema de Auditoria**
- Logs de todas as ações
- Rastreamento de atividades
- Relatórios de auditoria
- Controle de segurança

### **Sistema de Prestadores de Serviço**
- Cadastro de prestadores
- Controle de contratos e licenças
- Sistema de avaliações
- Categorização por tipo

### **Sistema de Membros da Família**
- Cadastro de familiares
- Controle de relacionamentos
- Documentos e autorizações
- Árvore genealógica

### **Sistema de Notificações**
- Envio de emails automáticos
- Templates personalizáveis
- Fila de processamento
- Controle de status

## 🔐 Acesso ao Sistema

### **Super Administrador**
- **Email**: superadmin@condosys.com
- **Senha**: superadmin123
- **Acesso**: http://localhost:8080/super-admin.html

### **Administradores de Condomínio**
- **Alphaline**: admin@alphaline.com / admin
- **Araras**: admin@araras.com / admin

## 📈 Monitoramento

### **Health Checks**
Todos os serviços possuem health checks configurados:
- **Banco**: http://localhost:5432
- **Serviços**: http://localhost:800X/health

### **Logs**
```bash
# Ver logs de todos os serviços
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f auth_service
```

## 🛠️ Desenvolvimento

### **Estrutura de um Microserviço**
```
service_name/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── db.py
│   ├── models/
│   │   └── entity.py
│   ├── schemas/
│   │   └── entity.py
│   ├── repositories/
│   │   └── entity_repository.py
│   ├── services/
│   │   └── entity_service.py
│   └── routers/
│       └── entity.py
├── main.py
├── requirements.txt
└── Dockerfile
```

### **Adicionando Novos Serviços**
1. Crie a estrutura do serviço
2. Adicione ao `docker-compose.yml`
3. Configure as variáveis de ambiente
4. Teste o serviço

## 🐛 Troubleshooting

### **Problemas Comuns**

1. **Serviço não inicia**
   - Verifique se a porta está disponível
   - Verifique os logs: `docker-compose logs service_name`

2. **Erro de conexão com banco**
   - Aguarde o banco inicializar completamente
   - Verifique as variáveis de ambiente

3. **Email não funciona**
   - Configure as variáveis SMTP no `.env`
   - Use senha de app do Gmail

### **Comandos Úteis**
```bash
# Parar todos os serviços
docker-compose down

# Reconstruir e iniciar
docker-compose up --build -d

# Ver status dos serviços
docker-compose ps

# Limpar volumes (CUIDADO: apaga dados)
docker-compose down -v
```

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE.txt` para mais detalhes.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para suporte ou dúvidas, entre em contato através dos issues do repositório.

---

**Sistema Completo de Gerenciamento de Condomínios** 🏢✨


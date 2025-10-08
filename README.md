
# Sistema de Condomínio - Projeto (Entregável)
Este repositório contém um sistema de exemplo para um condomínio com arquitetura de microserviços.
Linguagem: Python (FastAPI), banco Postgres, frontend estático (HTML/JS).

## Serviços incluídos
- auth_service (8001) - login e tokens simples
- user_service (8002) - CRUD de moradores/usuários
- unit_service (8003) - unidades (skeleton)
- reservation_service (8004) - reservas (skeleton)
- visitor_service (8005) - controle de visitantes (skeleton)
- maintenance_service (8006) - ordens de serviço (skeleton)
- reporting_service (8007) - relatórios (skeleton)
- frontend (8080) - interface web simples

## Como rodar (requer Docker e docker-compose)
1. `docker-compose up --build`
2. Acesse frontend: http://localhost:8080
3. APIs estão nas portas 8001..8007

## Usuário admin (seed)
- email: admin@condo.local
- password: admin

> Nota: sistema de autenticação é simplificado para fins didáticos. Não usar em produção sem melhorias de segurança.

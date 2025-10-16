# CondoSys - Frontend

## Visão Geral

Interface moderna e responsiva para o sistema de gestão condominial multi-tenant CondoSys. O frontend foi desenvolvido com foco em usabilidade, design moderno e personalização por condomínio.

## Características

### 🎨 Design Moderno
- Interface limpa e profissional
- Animações suaves e transições elegantes
- Design responsivo para todos os dispositivos
- Tema personalizável por condomínio

### 🏢 Multi-Tenancy
- Seleção de condomínio no login
- Cadastro de novos condomínios
- Aplicação automática de temas
- Isolamento visual por tenant

### 📱 Responsividade
- Otimizado para desktop, tablet e mobile
- Layout adaptativo
- Navegação intuitiva em todos os tamanhos de tela

### ⚡ Performance
- Carregamento rápido
- Animações otimizadas
- Interface fluida e responsiva

## Estrutura de Arquivos

```
Frontend/
├── index.html          # Página principal
├── demo.html           # Página de demonstração
├── app.js             # JavaScript principal
├── config.json        # Configuração das APIs
├── nginx.conf         # Configuração do Nginx
└── README.md          # Este arquivo
```

## Funcionalidades

### 🔐 Autenticação
- Login com seleção de condomínio
- Cadastro de novos condomínios
- Aplicação automática de temas
- Informações do tenant no header

### 📊 Dashboard
- Cards de estatísticas animados
- Métricas em tempo real
- Design responsivo
- Efeitos visuais modernos

### 👥 Gestão de Usuários
- Listagem de usuários por tenant
- Criação de novos usuários
- Sistema de permissões
- Interface intuitiva

### 🏠 Gestão de Unidades
- Cadastro e listagem de unidades
- Associação com proprietários
- Interface organizada

### 📅 Reservas
- Calendário interativo
- Criação de reservas
- Filtros por área
- Visualização em grid

### 👥 Visitantes
- Controle de entrada e saída
- Check-in/Check-out
- Histórico de visitas
- Status em tempo real

### 🔧 Manutenção
- Ordens de serviço
- Categorização por tipo
- Sistema de prioridades
- Acompanhamento de status

### 📈 Relatórios
- Geração de relatórios
- Exportação de dados
- Filtros por período
- Visualização de estatísticas

## Personalização de Temas

### Cores Personalizáveis
- **Cor Primária**: Usada em botões e elementos principais
- **Cor Secundária**: Usada em elementos de destaque
- **Cor de Fundo**: Cor de fundo da interface
- **Cor do Texto**: Cor principal do texto

### Aplicação de Temas
Os temas são aplicados automaticamente através de variáveis CSS:
```css
:root {
  --primary-color: #1976d2;
  --secondary-color: #dc004e;
  --background-color: #f5f5f5;
  --text-color: #333333;
}
```

## Tecnologias Utilizadas

- **HTML5**: Estrutura semântica
- **CSS3**: Estilos modernos com variáveis CSS
- **JavaScript ES6+**: Funcionalidades interativas
- **Font Awesome**: Ícones
- **Google Fonts**: Tipografia (Inter)
- **Nginx**: Servidor web e proxy reverso

## Recursos Visuais

### Animações
- Transições suaves em todos os elementos
- Efeitos de hover interativos
- Animações de entrada (fade-in, slide-in)
- Loading states animados

### Efeitos Especiais
- Backdrop blur nos cards
- Gradientes dinâmicos
- Sombras e elevações
- Efeitos de partículas no fundo

### Responsividade
- Breakpoints para mobile, tablet e desktop
- Layout flexível e adaptativo
- Navegação otimizada para touch
- Tipografia escalável

## Como Usar

### 1. Acesso ao Sistema
1. Abra `http://localhost:8080` no navegador
2. Selecione um condomínio na lista
3. Digite suas credenciais
4. O sistema aplicará automaticamente o tema do condomínio

### 2. Cadastro de Condomínio
1. Clique em "Cadastrar Novo Condomínio"
2. Preencha os dados do condomínio
3. Configure as cores do tema
4. Crie o usuário administrador
5. O sistema criará automaticamente o condomínio

### 3. Navegação
- Use o menu superior para navegar entre as seções
- O menu se adapta às permissões do usuário
- Informações do condomínio são exibidas no header

## Demonstração

Acesse `demo.html` para ver uma demonstração dos temas disponíveis e funcionalidades do sistema.

## Compatibilidade

### Navegadores Suportados
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Dispositivos
- Desktop (1920x1080+)
- Tablet (768x1024)
- Mobile (375x667+)

## Desenvolvimento

### Estrutura CSS
- Variáveis CSS para temas
- Classes utilitárias
- Componentes modulares
- Media queries responsivas

### JavaScript
- Funções modulares
- Async/await para APIs
- Gerenciamento de estado local
- Aplicação dinâmica de temas

## Suporte

Para dúvidas ou problemas com o frontend, consulte a documentação técnica ou entre em contato com a equipe de desenvolvimento.

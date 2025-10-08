// Load configuration and bootstrap app
+(async function init() {
  let cfg;
  try {
    const res = await fetch('config.json', { cache: 'no-store' });
    cfg = await res.json();
  } catch (e) {
    console.error('Failed to load config.json, using defaults', e);
    cfg = { 
      api_auth: '/api/auth', 
      api_users: '/api/users', 
      api_units: '/api/units', 
      api_reservations: '/api/reservations',
      api_visitors: '/api/visitors',
      api_maintenance: '/api/maintenance',
      api_reports: '/api/reports'
    };
  }

  const API_AUTH = cfg.api_auth || '/api/auth';
  const API_USER = cfg.api_users || '/api/users';
  const API_UNIT = cfg.api_units || '/api/units';
  const API_RES = cfg.api_reservations || '/api/reservations';
  const API_VISITORS = cfg.api_visitors || '/api/visitors';
  const API_MAINTENANCE = cfg.api_maintenance || '/api/maintenance';
  const API_REPORTS = cfg.api_reports || '/api/reports';

  function showNav(show){ document.getElementById('main-nav').style.display = show? 'block':'none' }

  function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i> ${message}`;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
      alertDiv.remove();
    }, 5000);
  }

  function setLoading(button, loading) {
    if (loading) {
      button.disabled = true;
      button.innerHTML = '<span class="loading"></span> Carregando...';
    } else {
      button.disabled = false;
      button.innerHTML = button.getAttribute('data-original-text') || button.innerHTML;
    }
  }

  async function login(){
    const company = document.getElementById('company').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    if (!email || !password) {
      showAlert('Por favor, preencha email e senha', 'error');
      return;
    }

    const btn = document.getElementById('btn-login');
    setLoading(btn, true);
    
    try {
      const res = await fetch(API_AUTH + '/login', {
        method:'POST', 
        headers:{'content-type':'application/json'}, 
        body: JSON.stringify({company,email,password})
      });
      const data = await res.json();
      
      if (!res.ok){ 
        showAlert(data.detail || 'Erro no login', 'error');
        return; 
      }
      
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('role', data.user.role);
      localStorage.setItem('user', JSON.stringify(data.user));
      
      document.getElementById('login').classList.add('hidden');
      showNav(true);
      navigateTo('dashboard');
      showAlert('Login realizado com sucesso!', 'success');
    } catch (error) {
      showAlert('Erro de conexão. Tente novamente.', 'error');
    } finally {
      setLoading(btn, false);
    }
  }

  document.getElementById('btn-login').onclick = login;
  document.getElementById('logout').onclick = ()=>{ 
    localStorage.clear(); 
    location.reload(); 
  }

  document.querySelectorAll('#main-nav a[data-view]').forEach(a=> a.onclick = (e)=>{ 
    e.preventDefault(); 
    navigateTo(a.dataset.view); 
  });

  function hideAll(){ 
    ['dashboard','users','units','reservations','visitors','maintenance','reports'].forEach(v => 
      document.getElementById('view-'+v).classList.add('hidden')
    ) 
  }

  function navigateTo(view){
    hideAll(); 
    document.getElementById('view-'+view).classList.remove('hidden');
    
    if(view==='dashboard') loadDashboard();
    if(view==='users') loadUsers();
    if(view==='units') loadUnits();
    if(view==='reservations') loadReservations();
    if(view==='visitors') loadVisitors();
    if(view==='maintenance') loadMaintenance();
    if(view==='reports') loadReports();
  }

  async function authFetch(url, opts={}){
    opts.headers = opts.headers || {};
    const token = localStorage.getItem('token');
    if (token) opts.headers['Authorization'] = 'Bearer ' + token;
    
    const res = await fetch(url, opts);
    if (res.status===401){ 
      showAlert('Sessão expirada, faça login novamente', 'error');
      localStorage.clear(); 
      location.reload(); 
    }
    return res;
  }

  // Dashboard
  async function loadDashboard() {
    try {
      const [usersRes, unitsRes, reservationsRes, visitorsRes] = await Promise.all([
        authFetch(API_USER + '/users'),
        authFetch(API_UNIT + '/units'),
        authFetch(API_RES + '/reservations'),
        authFetch(API_VISITORS + '/visitors')
      ]);

      const users = usersRes.ok ? await usersRes.json() : [];
      const units = unitsRes.ok ? await unitsRes.json() : [];
      const reservations = reservationsRes.ok ? await reservationsRes.json() : [];
      const visitors = visitorsRes.ok ? await visitorsRes.json() : [];

      document.getElementById('total-users').textContent = users.length;
      document.getElementById('total-units').textContent = units.length;
      document.getElementById('total-reservations').textContent = reservations.length;
      document.getElementById('total-visitors').textContent = visitors.length;
    } catch (error) {
      console.error('Error loading dashboard:', error);
    }
  }

  // Users
  async function loadUsers(){
    const res = await authFetch(API_USER + '/users');
    if (!res.ok){ showAlert('Erro ao listar usuários', 'error'); return; }
    const users = await res.json();
    const tbody = document.querySelector('#tbl-users tbody'); 
    tbody.innerHTML='';
    users.forEach(u=> tbody.insertAdjacentHTML('beforeend', 
      `<tr><td>${u.id}</td><td>${u.email}</td><td>${u.full_name||''}</td><td>${u.role}</td></tr>`));
  }
  
  document.getElementById('refresh-users').onclick = loadUsers;
  document.getElementById('btn-create-user').onclick = async ()=>{
    const email = document.getElementById('u-email').value;
    const password = document.getElementById('u-pass').value;
    const full_name = document.getElementById('u-name').value;
    const role = document.getElementById('u-role').value;
    
    if (!email || !password || !full_name) {
      showAlert('Por favor, preencha todos os campos obrigatórios', 'error');
      return;
    }

    const btn = document.getElementById('btn-create-user');
    setLoading(btn, true);
    
    try {
      const res = await authFetch(API_USER + '/users', {
        method:'POST', 
        headers:{'content-type':'application/json'}, 
        body: JSON.stringify({email,password,full_name,role})
      });
      
      if (!res.ok){ 
        const error = await res.json();
        showAlert('Erro: ' + (error.detail || 'Erro desconhecido'), 'error');
        return; 
      }
      
      showAlert('Usuário criado com sucesso!', 'success');
      loadUsers();
      
      // Clear form
      document.getElementById('u-email').value = '';
      document.getElementById('u-pass').value = '';
      document.getElementById('u-name').value = '';
    } catch (error) {
      showAlert('Erro de conexão', 'error');
    } finally {
      setLoading(btn, false);
    }
  };

  // Units
  async function loadUnits(){
    const res = await authFetch(API_UNIT + '/units');
    if (!res.ok){ showAlert('Erro ao listar unidades', 'error'); return; }
    const units = await res.json();
    const tbody = document.querySelector('#tbl-units tbody'); 
    tbody.innerHTML='';
    units.forEach(u=> tbody.insertAdjacentHTML('beforeend', 
      `<tr><td>${u.id}</td><td>${u.block}</td><td>${u.number}</td><td>${u.owner_id||''}</td></tr>`));
  }
  
  document.getElementById('refresh-units').onclick = loadUnits;
  document.getElementById('btn-create-unit').onclick = async ()=>{
    const block = document.getElementById('unit-block').value;
    const number = document.getElementById('unit-number').value;
    const owner_id = document.getElementById('unit-owner').value || null;
    
    if (!block || !number) {
      showAlert('Por favor, preencha bloco e número', 'error');
      return;
    }

    const btn = document.getElementById('btn-create-unit');
    setLoading(btn, true);
    
    try {
      const body = {block, number, owner_id: owner_id? parseInt(owner_id): null};
      const res = await authFetch(API_UNIT + '/units', {
        method:'POST', 
        headers:{'content-type':'application/json'}, 
        body: JSON.stringify(body)
      });
      
      if (!res.ok){ 
        const error = await res.json();
        showAlert('Erro criar unidade: ' + (error.detail || 'Erro desconhecido'), 'error');
        return; 
      }
      
      showAlert('Unidade criada com sucesso!', 'success');
      loadUnits();
      
      // Clear form
      document.getElementById('unit-block').value = '';
      document.getElementById('unit-number').value = '';
      document.getElementById('unit-owner').value = '';
    } catch (error) {
      showAlert('Erro de conexão', 'error');
    } finally {
      setLoading(btn, false);
    }
  };

  // Reservations
  async function loadReservations(){
    const res = await authFetch(API_RES + '/reservations');
    if (!res.ok){ showAlert('Erro ao listar reservas', 'error'); return; }
    const rows = await res.json();
    const tbody = document.querySelector('#tbl-res tbody'); 
    tbody.innerHTML='';
    rows.forEach(r => {
      const statusClass = `status-${r.status}`;
      tbody.insertAdjacentHTML('beforeend', 
        `<tr>
          <td>${r.id}</td>
          <td>${r.unit_id}</td>
          <td>${r.area}</td>
          <td>${new Date(r.start_time).toLocaleString()}</td>
          <td>${new Date(r.end_time).toLocaleString()}</td>
          <td><span class="status-badge ${statusClass}">${r.status}</span></td>
          <td>
            ${r.status !== 'cancelled' ? `<button onclick="cancelRes(${r.id})" class="btn-danger btn-sm">Cancelar</button>` : ''}
          </td>
        </tr>`);
    });
  }
  
  document.getElementById('refresh-res').onclick = loadReservations;
  window.cancelRes = async (id)=>{
    if (!confirm('Tem certeza que deseja cancelar esta reserva?')) return;
    
    const res = await authFetch(API_RES + `/reservations/${id}/cancel`, {method:'POST'});
    if (!res.ok){ 
      const error = await res.json();
      showAlert('Erro ao cancelar: ' + (error.detail || 'Erro desconhecido'), 'error');
      return; 
    }
    showAlert('Reserva cancelada com sucesso!', 'success');
    loadReservations();
  }
  
  document.getElementById('btn-create-res').onclick = async ()=>{
    const unit_id = parseInt(document.getElementById('res-unit').value);
    const area = document.getElementById('res-area').value;
    const start = document.getElementById('res-start').value.replace(' ','T') + ':00';
    const end = document.getElementById('res-end').value.replace(' ','T') + ':00';
    
    if (!unit_id || !area || !start || !end) {
      showAlert('Por favor, preencha todos os campos', 'error');
      return;
    }

    const btn = document.getElementById('btn-create-res');
    setLoading(btn, true);
    
    try {
      const body = {unit_id, area, start_time: start, end_time: end};
      const res = await authFetch(API_RES + '/reservations', {
        method:'POST', 
        headers:{'content-type':'application/json'}, 
        body: JSON.stringify(body)
      });
      
      if (!res.ok){ 
        const error = await res.json();
        showAlert('Erro criar reserva: ' + (error.detail || 'Erro desconhecido'), 'error');
        return; 
      }
      
      showAlert('Reserva criada com sucesso!', 'success');
      loadReservations();
      
      // Clear form
      document.getElementById('res-unit').value = '';
      document.getElementById('res-area').value = '';
      document.getElementById('res-start').value = '';
      document.getElementById('res-end').value = '';
    } catch (error) {
      showAlert('Erro de conexão', 'error');
    } finally {
      setLoading(btn, false);
    }
  };

  // Visitors
  async function loadVisitors(){
    const res = await authFetch(API_VISITORS + '/visitors');
    if (!res.ok){ showAlert('Erro ao listar visitantes', 'error'); return; }
    const visitors = await res.json();
    const tbody = document.querySelector('#tbl-visitors tbody'); 
    tbody.innerHTML='';
    visitors.forEach(v => {
      const statusClass = `status-${v.status}`;
      tbody.insertAdjacentHTML('beforeend', 
        `<tr>
          <td>${v.id}</td>
          <td>${v.name}</td>
          <td>${v.document}</td>
          <td>${v.unit_id}</td>
          <td>${new Date(v.visit_date).toLocaleString()}</td>
          <td><span class="status-badge ${statusClass}">${v.status}</span></td>
          <td>
            ${v.status === 'scheduled' ? `<button onclick="checkInVisitor(${v.id})" class="btn-success btn-sm">Check-in</button>` : ''}
            ${v.status === 'checked_in' ? `<button onclick="checkOutVisitor(${v.id})" class="btn-warning btn-sm">Check-out</button>` : ''}
            ${v.status !== 'checked_in' ? `<button onclick="deleteVisitor(${v.id})" class="btn-danger btn-sm">Excluir</button>` : ''}
          </td>
        </tr>`);
    });
  }
  
  document.getElementById('refresh-visitors').onclick = loadVisitors;
  
  window.checkInVisitor = async (id) => {
    const res = await authFetch(API_VISITORS + `/visitors/${id}/check-in`, {method:'POST'});
    if (!res.ok){ 
      const error = await res.json();
      showAlert('Erro no check-in: ' + (error.detail || 'Erro desconhecido'), 'error');
      return; 
    }
    showAlert('Check-in realizado com sucesso!', 'success');
    loadVisitors();
  };
  
  window.checkOutVisitor = async (id) => {
    const res = await authFetch(API_VISITORS + `/visitors/${id}/check-out`, {method:'POST'});
    if (!res.ok){ 
      const error = await res.json();
      showAlert('Erro no check-out: ' + (error.detail || 'Erro desconhecido'), 'error');
      return; 
    }
    showAlert('Check-out realizado com sucesso!', 'success');
    loadVisitors();
  };
  
  window.deleteVisitor = async (id) => {
    if (!confirm('Tem certeza que deseja excluir este visitante?')) return;
    
    const res = await authFetch(API_VISITORS + `/visitors/${id}`, {method:'DELETE'});
    if (!res.ok){ 
      const error = await res.json();
      showAlert('Erro ao excluir: ' + (error.detail || 'Erro desconhecido'), 'error');
      return; 
    }
    showAlert('Visitante excluído com sucesso!', 'success');
    loadVisitors();
  };
  
  document.getElementById('btn-create-visitor').onclick = async ()=>{
    const name = document.getElementById('vis-name').value;
    const document = document.getElementById('vis-document').value;
    const unit_id = parseInt(document.getElementById('vis-unit').value);
    const visit_date = document.getElementById('vis-date').value;
    const purpose = document.getElementById('vis-purpose').value;
    const contact_phone = document.getElementById('vis-phone').value;
    
    if (!name || !document || !unit_id || !visit_date || !purpose) {
      showAlert('Por favor, preencha todos os campos obrigatórios', 'error');
      return;
    }

    const btn = document.getElementById('btn-create-visitor');
    setLoading(btn, true);
    
    try {
      const body = {name, document, unit_id, visit_date, purpose, contact_phone};
      const res = await authFetch(API_VISITORS + '/visitors', {
        method:'POST', 
        headers:{'content-type':'application/json'}, 
        body: JSON.stringify(body)
      });
      
      if (!res.ok){ 
        const error = await res.json();
        showAlert('Erro criar visitante: ' + (error.detail || 'Erro desconhecido'), 'error');
        return; 
      }
      
      showAlert('Visitante registrado com sucesso!', 'success');
      loadVisitors();
      
      // Clear form
      document.getElementById('vis-name').value = '';
      document.getElementById('vis-document').value = '';
      document.getElementById('vis-unit').value = '';
      document.getElementById('vis-date').value = '';
      document.getElementById('vis-purpose').value = '';
      document.getElementById('vis-phone').value = '';
    } catch (error) {
      showAlert('Erro de conexão', 'error');
    } finally {
      setLoading(btn, false);
    }
  };

  // Maintenance
  async function loadMaintenance(){
    const res = await authFetch(API_MAINTENANCE + '/maintenance');
    if (!res.ok){ showAlert('Erro ao listar ordens de manutenção', 'error'); return; }
    const orders = await res.json();
    const tbody = document.querySelector('#tbl-maintenance tbody'); 
    tbody.innerHTML='';
    orders.forEach(o => {
      const statusClass = `status-${o.status}`;
      const priorityClass = `priority-${o.priority}`;
      tbody.insertAdjacentHTML('beforeend', 
        `<tr>
          <td>${o.id}</td>
          <td>${o.title}</td>
          <td>${o.category}</td>
          <td><span class="status-badge ${priorityClass}">${o.priority}</span></td>
          <td><span class="status-badge ${statusClass}">${o.status}</span></td>
          <td>${new Date(o.created_at).toLocaleDateString()}</td>
          <td>
            ${o.status === 'open' ? `<button onclick="assignMaintenance(${o.id})" class="btn-warning btn-sm">Atribuir</button>` : ''}
            ${o.status === 'assigned' ? `<button onclick="completeMaintenance(${o.id})" class="btn-success btn-sm">Concluir</button>` : ''}
            ${o.status !== 'completed' ? `<button onclick="deleteMaintenance(${o.id})" class="btn-danger btn-sm">Excluir</button>` : ''}
          </td>
        </tr>`);
    });
  }
  
  document.getElementById('refresh-maintenance').onclick = loadMaintenance;
  
  window.assignMaintenance = async (id) => {
    const assigned_to = prompt('Nome do responsável:');
    if (!assigned_to) return;
    
    const res = await authFetch(API_MAINTENANCE + `/maintenance/${id}/assign`, {
      method:'POST',
      headers:{'content-type':'application/json'},
      body: JSON.stringify({assigned_to})
    });
    if (!res.ok){ 
      const error = await res.json();
      showAlert('Erro ao atribuir: ' + (error.detail || 'Erro desconhecido'), 'error');
      return; 
    }
    showAlert('Ordem atribuída com sucesso!', 'success');
    loadMaintenance();
  };
  
  window.completeMaintenance = async (id) => {
    if (!confirm('Tem certeza que deseja marcar como concluída?')) return;
    
    const res = await authFetch(API_MAINTENANCE + `/maintenance/${id}/complete`, {method:'POST'});
    if (!res.ok){ 
      const error = await res.json();
      showAlert('Erro ao concluir: ' + (error.detail || 'Erro desconhecido'), 'error');
      return; 
    }
    showAlert('Ordem concluída com sucesso!', 'success');
    loadMaintenance();
  };
  
  window.deleteMaintenance = async (id) => {
    if (!confirm('Tem certeza que deseja excluir esta ordem?')) return;
    
    const res = await authFetch(API_MAINTENANCE + `/maintenance/${id}`, {method:'DELETE'});
    if (!res.ok){ 
      const error = await res.json();
      showAlert('Erro ao excluir: ' + (error.detail || 'Erro desconhecido'), 'error');
      return; 
    }
    showAlert('Ordem excluída com sucesso!', 'success');
    loadMaintenance();
  };
  
  document.getElementById('btn-create-maintenance').onclick = async ()=>{
    const title = document.getElementById('maint-title').value;
    const description = document.getElementById('maint-description').value;
    const unit_id = parseInt(document.getElementById('maint-unit').value);
    const category = document.getElementById('maint-category').value;
    const priority = document.getElementById('maint-priority').value;
    
    if (!title || !description || !unit_id || !category) {
      showAlert('Por favor, preencha todos os campos obrigatórios', 'error');
      return;
    }

    const btn = document.getElementById('btn-create-maintenance');
    setLoading(btn, true);
    
    try {
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      const body = {title, description, unit_id, category, priority, requested_by: user.id || 1};
      const res = await authFetch(API_MAINTENANCE + '/maintenance', {
        method:'POST', 
        headers:{'content-type':'application/json'}, 
        body: JSON.stringify(body)
      });
      
      if (!res.ok){ 
        const error = await res.json();
        showAlert('Erro criar ordem: ' + (error.detail || 'Erro desconhecido'), 'error');
        return; 
      }
      
      showAlert('Ordem de manutenção criada com sucesso!', 'success');
      loadMaintenance();
      
      // Clear form
      document.getElementById('maint-title').value = '';
      document.getElementById('maint-description').value = '';
      document.getElementById('maint-unit').value = '';
      document.getElementById('maint-category').value = 'plumbing';
      document.getElementById('maint-priority').value = 'medium';
    } catch (error) {
      showAlert('Erro de conexão', 'error');
    } finally {
      setLoading(btn, false);
    }
  };

  // Reports
  async function loadReports() {
    // Set default dates
    const today = new Date();
    const lastMonth = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
    
    document.getElementById('report-start').value = lastMonth.toISOString().split('T')[0];
    document.getElementById('report-end').value = today.toISOString().split('T')[0];
  }
  
  document.getElementById('btn-generate-report').onclick = async ()=>{
    const reportType = document.getElementById('report-type').value;
    const startDate = document.getElementById('report-start').value;
    const endDate = document.getElementById('report-end').value;
    
    if (!startDate || !endDate) {
      showAlert('Por favor, selecione as datas', 'error');
      return;
    }

    const btn = document.getElementById('btn-generate-report');
    setLoading(btn, true);
    
    try {
      const body = {
        report_type: reportType,
        start_date: startDate + 'T00:00:00',
        end_date: endDate + 'T23:59:59'
      };
      
      const res = await authFetch(API_REPORTS + '/reports/generate', {
        method:'POST', 
        headers:{'content-type':'application/json'}, 
        body: JSON.stringify(body)
      });
      
      if (!res.ok){ 
        const error = await res.json();
        showAlert('Erro gerar relatório: ' + (error.detail || 'Erro desconhecido'), 'error');
        return; 
      }
      
      const report = await res.json();
      displayReport(report);
      showAlert('Relatório gerado com sucesso!', 'success');
    } catch (error) {
      showAlert('Erro de conexão', 'error');
    } finally {
      setLoading(btn, false);
    }
  };

  function displayReport(report) {
    const resultsDiv = document.getElementById('report-results');
    const contentDiv = document.getElementById('report-content');
    
    let html = `
      <div class="alert alert-info">
        <h4><i class="fas fa-file-alt"></i> ${report.title}</h4>
        <p><strong>Gerado em:</strong> ${new Date(report.generated_at).toLocaleString()}</p>
      </div>
      
      <div class="row">
        <div class="col">
          <h5>Resumo</h5>
          <div class="stats-grid">
    `;
    
    // Summary stats
    Object.entries(report.summary).forEach(([key, value]) => {
      html += `
        <div class="stat-card">
          <h3>${value}</h3>
          <p>${key.replace(/_/g, ' ').toUpperCase()}</p>
        </div>
      `;
    });
    
    html += `
          </div>
        </div>
      </div>
      
      <div class="row">
        <div class="col">
          <h5>Detalhes</h5>
          <pre style="background: #f8f9fa; padding: 15px; border-radius: 10px; overflow-x: auto;">${JSON.stringify(report.data, null, 2)}</pre>
        </div>
      </div>
    `;
    
    contentDiv.innerHTML = html;
    resultsDiv.classList.remove('hidden');
  }

  // Store original button texts
  document.querySelectorAll('button').forEach(btn => {
    btn.setAttribute('data-original-text', btn.innerHTML);
  });

  // Auto-login if token exists
  if(localStorage.getItem('token')){ 
    document.getElementById('login').classList.add('hidden'); 
    showNav(true); 
    navigateTo('dashboard'); 
  }
})();
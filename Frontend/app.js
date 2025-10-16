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
  const API_TENANTS = cfg.api_tenants || '/api/tenants';

  function showNav(show){ document.getElementById('main-nav').style.display = show? 'block':'none' }

  // Carregar lista de tenants
  async function loadTenants() {
    try {
      const res = await fetch(API_TENANTS + '/tenants');
      if (!res.ok) return;
      const tenants = await res.json();
      const select = document.getElementById('tenant-select');
      select.innerHTML = '<option value="">Selecione um condomínio</option>';
      tenants.forEach(tenant => {
        const option = document.createElement('option');
        option.value = tenant.id;
        option.textContent = tenant.name;
        select.appendChild(option);
      });
    } catch (error) {
      console.error('Erro ao carregar tenants:', error);
    }
  }

  // Aplicar tema do tenant
  function applyTenantTheme(themeConfig) {
    if (!themeConfig) return;
    
    const root = document.documentElement;
    if (themeConfig.primary_color) {
      root.style.setProperty('--primary-color', themeConfig.primary_color);
    }
    if (themeConfig.secondary_color) {
      root.style.setProperty('--secondary-color', themeConfig.secondary_color);
    }
    if (themeConfig.background_color) {
      root.style.setProperty('--background-color', themeConfig.background_color);
    }
    if (themeConfig.text_color) {
      root.style.setProperty('--text-color', themeConfig.text_color);
    }
  }


  function adjustNavByRole(){
    const role = localStorage.getItem('role');
    const nav = document.getElementById('main-nav');
    if (!nav) return;
    
    // Show all by default
    nav.querySelectorAll('[data-view], #logout').forEach(a=> a.style.display = '');
    
    // Hide admin-only items for moradores
    if (role === 'morador'){
      const hideViews = ['users','reports','units','visitors','maintenance'];
      hideViews.forEach(v => {
        const el = nav.querySelector(`[data-view="${v}"]`);
        if (el) el.style.display = 'none';
      });
    }
  }

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
    const tenantId = document.getElementById('tenant-select').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    if (!tenantId || !email || !password) {
      showAlert('Por favor, preencha todos os campos', 'error');
      return;
    }

    const btn = document.getElementById('btn-login');
    setLoading(btn, true);
    
    try {
      const res = await fetch(API_AUTH + '/login', {
        method:'POST', 
        headers:{'content-type':'application/json'}, 
        body: JSON.stringify({tenant_id: parseInt(tenantId), email, password})
      });
      
      const data = await res.json();
      
      if (!res.ok){ 
        showAlert(data.detail || 'Erro no login', 'error');
        return; 
      }
      
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('role', data.user.role);
      localStorage.setItem('user', JSON.stringify(data.user));
      localStorage.setItem('tenant', JSON.stringify(data.tenant));
      
      // Aplicar tema do tenant
      if (data.tenant && data.tenant.theme_config) {
        applyTenantTheme(data.tenant.theme_config);
      }
      
      // Mostrar informações do tenant
      if (data.tenant) {
        document.getElementById('tenant-name').textContent = data.tenant.name;
        document.getElementById('tenant-info').style.display = 'flex';
      }
      
      document.getElementById('login').classList.add('hidden');
      showNav(true);
      adjustNavByRole();
      navigateTo('dashboard');
      showAlert('Login realizado com sucesso!', 'success');
    } catch (error) {
      showAlert('Erro de conexão. Tente novamente.', 'error');
    } finally {
      setLoading(btn, false);
    }
  }

  // Cadastro de tenant
  async function registerTenant() {
    const name = document.getElementById('tenant-name').value;
    const cnpj = document.getElementById('tenant-cnpj').value;
    const address = document.getElementById('tenant-address').value;
    const phone = document.getElementById('tenant-phone').value;
    const email = document.getElementById('tenant-email').value;
    const primaryColor = document.getElementById('theme-primary').value;
    const secondaryColor = document.getElementById('theme-secondary').value;
    const adminName = document.getElementById('admin-name').value;
    const adminEmail = document.getElementById('admin-email').value;
    const adminPassword = document.getElementById('admin-password').value;
    
    if (!name || !cnpj || !address || !phone || !email || !adminName || !adminEmail || !adminPassword) {
      showAlert('Por favor, preencha todos os campos obrigatórios', 'error');
      return;
    }

    const btn = document.getElementById('btn-register-tenant');
    setLoading(btn, true);
    
    try {
      const tenantData = {
        name,
        cnpj,
        address,
        phone,
        email,
        theme_config: {
          primary_color: primaryColor,
          secondary_color: secondaryColor,
          background_color: '#f5f5f5',
          text_color: '#333333'
        },
        admin_email: adminEmail,
        admin_password: adminPassword,
        admin_name: adminName
      };
      
      const res = await fetch(API_TENANTS + '/tenants', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(tenantData)
      });
      
      if (!res.ok) {
        const error = await res.json();
        showAlert('Erro ao cadastrar: ' + (error.detail || 'Erro desconhecido'), 'error');
        return;
      }
      
      showAlert('Condomínio cadastrado com sucesso!', 'success');
      
      // Limpar formulário
      document.getElementById('tenant-name').value = '';
      document.getElementById('tenant-cnpj').value = '';
      document.getElementById('tenant-address').value = '';
      document.getElementById('tenant-phone').value = '';
      document.getElementById('tenant-email').value = '';
      document.getElementById('admin-name').value = '';
      document.getElementById('admin-email').value = '';
      document.getElementById('admin-password').value = '';
      
      // Recarregar lista de tenants
      await loadTenants();
      
      // Voltar para login
      document.getElementById('tenant-registration').classList.add('hidden');
      document.getElementById('login').classList.remove('hidden');
      
    } catch (error) {
      showAlert('Erro de conexão', 'error');
    } finally {
      setLoading(btn, false);
    }
  }

  document.getElementById('btn-login').onclick = login;
  document.getElementById('btn-register-tenant').onclick = registerTenant;
  document.getElementById('show-tenant-registration').onclick = (e) => {
    e.preventDefault();
    document.getElementById('login').classList.add('hidden');
    document.getElementById('tenant-registration').classList.remove('hidden');
  };
  document.getElementById('back-to-login').onclick = (e) => {
    e.preventDefault();
    document.getElementById('tenant-registration').classList.add('hidden');
    document.getElementById('login').classList.remove('hidden');
  };
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
    if(view==='reservations'){ loadReservations(); initCalendar(); }
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
    const areaFilter = (document.getElementById('list-area')||{}).value || '';
    const res = await authFetch(API_RES + '/reservations');
    if (!res.ok){ showAlert('Erro ao listar reservas', 'error'); return; }
    let rows = await res.json();
    if (areaFilter) rows = rows.filter(r=> (r.area||'').toLowerCase().includes(areaFilter.toLowerCase()));
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
    const start = document.getElementById('res-start').value ? document.getElementById('res-start').value + ':00' : '';
    const end = document.getElementById('res-end').value ? document.getElementById('res-end').value + ':00' : '';
    
    if (!unit_id || !area || !start || !end) {
      showAlert('Por favor, preencha todos os campos', 'error');
      return;
    }

    const btn = document.getElementById('btn-create-res');
    setLoading(btn, true);
    
    try {
      // availability check
      const qs = new URLSearchParams({ area, start_time: start, end_time: end }).toString();
      const availabilityRes = await authFetch(API_RES + `/reservations/availability?${qs}`);
      if (availabilityRes.ok){
        const avail = await availabilityRes.json();
        if (!avail.available){
          showAlert(avail.detail || 'Horário indisponível para esta área', 'error');
          setLoading(btn, false);
          return;
        }
      }
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

  function initCalendar(){
    const monthInput = document.getElementById('cal-month');
    const btn = document.getElementById('btn-load-calendar');
    const grid = document.getElementById('calendar-grid');
    const areaInput = document.getElementById('cal-area');
    if (!monthInput || !btn || !grid) return;

    if (!monthInput.value){
      const today = new Date();
      monthInput.value = today.toISOString().slice(0,7);
    }

    btn.onclick = async ()=>{
      const [year, month] = monthInput.value.split('-').map(x=>parseInt(x,10));
      if (!year || !month) return;
      await renderCalendar(year, month, areaInput.value||'');
    };

    // Auto render on open
    const [y, m] = monthInput.value.split('-').map(x=>parseInt(x,10));
    renderCalendar(y, m, areaInput ? (areaInput.value||'') : '');
  }

  async function renderCalendar(year, month, areaFilter){
    const grid = document.getElementById('calendar-grid');
    grid.innerHTML = '';
    grid.style.display = 'grid';
    grid.style.gridTemplateColumns = 'repeat(7, 1fr)';
    grid.style.gap = '8px';

    const start = new Date(year, month-1, 1);
    const end = new Date(year, month, 0);
    const firstWeekday = (start.getDay()+6)%7; // make Monday=0
    const daysInMonth = end.getDate();

    // fetch reservations once
    const res = await authFetch(API_RES + '/reservations');
    let rows = res.ok ? await res.json() : [];
    if (areaFilter) rows = rows.filter(r=> (r.area||'').toLowerCase().includes(areaFilter.toLowerCase()));

    const user = JSON.parse(localStorage.getItem('user')||'{}');

    // Build a map date -> reservations
    const dateKey = (d)=> d.toISOString().slice(0,10);
    const map = {};
    for (const r of rows){
      const s = new Date(r.start_time);
      if (s.getFullYear()===year && (s.getMonth()+1)===month){
        const k = dateKey(s);
        (map[k] = map[k] || []).push(r);
      }
    }

    // Headers
    const weekdays = ['Seg','Ter','Qua','Qui','Sex','Sáb','Dom'];
    weekdays.forEach(w=>{
      const h = document.createElement('div');
      h.style.fontWeight = '700';
      h.style.textAlign = 'center';
      h.textContent = w;
      grid.appendChild(h);
    });

    // Leading blanks
    for (let i=0;i<firstWeekday;i++){
      const b = document.createElement('div');
      grid.appendChild(b);
    }

    for (let d=1; d<=daysInMonth; d++){
      const cell = document.createElement('div');
      cell.className = 'card';
      cell.style.padding = '10px';
      const dayDate = new Date(year, month-1, d);
      const k = dateKey(dayDate);
      const list = map[k] || [];
      const items = list.slice(0,3).map(r=>{
        const isMine = user && typeof user.id !== 'undefined' && (r.owner_id === user.id || r.user_id === user.id);
        const bulletColor = isMine ? '#20c997' : '#667eea';
        return `<div style=\"font-size:0.85rem\"><i class='fas fa-circle' style='font-size:6px;color:${bulletColor}'></i> ${r.area} ${new Date(r.start_time).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}</div>`
      }).join('');
      const more = list.length>3 ? `<div style='font-size:0.8rem;color:#666'>+${list.length-3} mais</div>`:'';
      cell.innerHTML = `<div style='font-weight:700;margin-bottom:6px'>${d}</div>${items}${more}`;
      grid.appendChild(cell);
    }
  }

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

  // Export reservations CSV
  document.getElementById('btn-export-reservations').onclick = async ()=>{
    const startDate = document.getElementById('report-start').value;
    const endDate = document.getElementById('report-end').value;
    if (!startDate || !endDate) { showAlert('Selecione as datas para exportar', 'error'); return; }
    const qs = new URLSearchParams({ start_date: startDate + 'T00:00:00', end_date: endDate + 'T23:59:59' }).toString();
    const token = localStorage.getItem('token');
    try{
      const res = await fetch(API_REPORTS + `/reports/reservations/export?${qs}`, {
        headers: token ? { 'Authorization': 'Bearer ' + token } : {}
      });
      if (!res.ok){ showAlert('Erro ao exportar CSV', 'error'); return; }
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `reservas_${startDate}_${endDate}.csv`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      showAlert('CSV gerado com sucesso!', 'success');
    }catch(e){
      showAlert('Erro de conexão ao exportar', 'error');
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


  // Inicialização
  loadTenants();
  
  // Auto-login if token exists
  if(localStorage.getItem('token')){ 
    document.getElementById('login').classList.add('hidden'); 
    showNav(true); 
    adjustNavByRole();
    
    // Aplicar tema salvo
    const tenant = JSON.parse(localStorage.getItem('tenant') || '{}');
    if (tenant.theme_config) {
      applyTenantTheme(tenant.theme_config);
    }
    
    // Mostrar informações do tenant
    if (tenant.name) {
      document.getElementById('tenant-name').textContent = tenant.name;
      document.getElementById('tenant-info').style.display = 'flex';
    }
    
    navigateTo('dashboard'); 
  }

})();
// Load configuration and bootstrap app
(async function init() {
  let cfg;
  try {
    const res = await fetch('config.json', { cache: 'no-store' });
    cfg = await res.json();
  } catch (e) {
    console.error('Failed to load config.json, using defaults', e);
    cfg = { api_auth: '/api/auth', api_users: '/api/users', api_units: '/api/units', api_reservations: '/api/reservations' };
  }

  const API_AUTH = cfg.api_auth || '/api/auth';
  const API_USER = cfg.api_users || '/api/users';
  const API_UNIT = cfg.api_units || '/api/units';
  const API_RES = cfg.api_reservations || '/api/reservations';

  function showNav(show){ document.getElementById('main-nav').style.display = show? 'block':'none' }

  async function login(){
    const company = document.getElementById('company').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const res = await fetch(API_AUTH + '/login', {
      method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({company,email,password})
    });
    const data = await res.json();
    if (!res.ok){ document.getElementById('login-msg').innerText = data.detail || JSON.stringify(data); return; }
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('role', data.user.role);
    document.getElementById('login').classList.add('hidden');
    showNav(true);
    navigateTo('users');
  }

  document.getElementById('btn-login').onclick = login;
  document.getElementById('logout').onclick = ()=>{ localStorage.clear(); location.reload(); }

  document.querySelectorAll('#main-nav a[data-view]').forEach(a=> a.onclick = (e)=>{ e.preventDefault(); navigateTo(a.dataset.view); });

  function hideAll(){ ['users','units','reservations','visitors','maintenance','reports'].forEach(v => document.getElementById('view-'+v).classList.add('hidden')) }

  function navigateTo(view){
    hideAll(); document.getElementById('view-'+view).classList.remove('hidden');
    if(view==='users') loadUsers();
    if(view==='units') loadUnits();
    if(view==='reservations') loadReservations();
  }

  async function authFetch(url, opts={}){
    opts.headers = opts.headers || {};
    const token = localStorage.getItem('token');
    if (token) opts.headers['Authorization'] = 'Bearer ' + token;
    const res = await fetch(url, opts);
    if (res.status===401){ alert('Sessão expirada, faça login novamente'); localStorage.clear(); location.reload(); }
    return res;
  }

  async function loadUsers(){
    const res = await authFetch(API_USER + '/users');
    if (!res.ok){ alert('Erro ao listar usuários'); return; }
    const users = await res.json();
    const tbody = document.querySelector('#tbl-users tbody'); tbody.innerHTML='';
    users.forEach(u=> tbody.insertAdjacentHTML('beforeend', `<tr><td>${u.id}</td><td>${u.email}</td><td>${u.full_name||''}</td><td>${u.role}</td></tr>`));
  }
  document.getElementById('refresh-users').onclick = loadUsers;
  document.getElementById('btn-create-user').onclick = async ()=>{
    const email = document.getElementById('u-email').value;
    const password = document.getElementById('u-pass').value;
    const full_name = document.getElementById('u-name').value;
    const role = document.getElementById('u-role').value;
    const res = await authFetch(API_USER + '/users', {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({email,password,full_name,role})});
    if (!res.ok){ alert('Erro: ' + JSON.stringify(await res.json())); return; }
    loadUsers();
  };

  async function loadUnits(){
    const res = await authFetch(API_UNIT + '/units');
    if (!res.ok){ alert('Erro ao listar unidades'); return; }
    const units = await res.json();
    const tbody = document.querySelector('#tbl-units tbody'); tbody.innerHTML='';
    units.forEach(u=> tbody.insertAdjacentHTML('beforeend', `<tr><td>${u.id}</td><td>${u.block}</td><td>${u.number}</td><td>${u.owner_id||''}</td></tr>`));
  }
  document.getElementById('refresh-units').onclick = loadUnits;
  document.getElementById('btn-create-unit').onclick = async ()=>{
    const block = document.getElementById('unit-block').value;
    const number = document.getElementById('unit-number').value;
    const owner_id = document.getElementById('unit-owner').value || null;
    const body = {block, number, owner_id: owner_id? parseInt(owner_id): null};
    const res = await authFetch(API_UNIT + '/units', {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify(body)});
    if (!res.ok){ alert('Erro criar unidade: ' + JSON.stringify(await res.json())); return; }
    loadUnits();
  };

  async function loadReservations(){
    const res = await authFetch(API_RES + '/reservations');
    if (!res.ok){ alert('Erro ao listar reservas'); return; }
    const rows = await res.json();
    const tbody = document.querySelector('#tbl-res tbody'); tbody.innerHTML='';
    rows.forEach(r => {
      tbody.insertAdjacentHTML('beforeend', `<tr><td>${r.id}</td><td>${r.unit_id}</td><td>${r.area}</td><td>${r.start_time}</td><td>${r.end_time}</td><td>${r.status}</td><td><button onclick="cancelRes(${r.id})">Cancelar</button></td></tr>`)
    });
  }
  document.getElementById('refresh-res').onclick = loadReservations;
  window.cancelRes = async (id)=>{
    const res = await authFetch(API_RES + `/reservations/${id}/cancel`, {method:'POST'});
    if (!res.ok){ alert('Erro ao cancelar: ' + JSON.stringify(await res.json())); return; }
    loadReservations();
  }
  document.getElementById('btn-create-res').onclick = async ()=>{
    const unit_id = parseInt(document.getElementById('res-unit').value);
    const area = document.getElementById('res-area').value;
    const start = document.getElementById('res-start').value.replace(' ','T') + ':00';
    const end = document.getElementById('res-end').value.replace(' ','T') + ':00';
    const body = {unit_id, area, start_time: start, end_time: end};
    const res = await authFetch(API_RES + '/reservations', {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify(body)});
    if (!res.ok){ alert('Erro criar reserva: ' + JSON.stringify(await res.json())); return; }
    loadReservations();
  };

  if(localStorage.getItem('token')){ document.getElementById('login').classList.add('hidden'); showNav(true); navigateTo('users'); }
})();




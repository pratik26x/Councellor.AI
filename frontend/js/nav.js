/* nav.js — shared navbar, auth-aware */
(function () {
  const path = window.location.pathname;
  const isLoginPage = path.includes('login.html');

  function esc(s) {
    return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  /* ── Read user from localStorage ── */
  let user = null;
  try { user = JSON.parse(localStorage.getItem('auth_user') || 'null'); } catch(e) {}

  /* ── Build right-side auth area ── */
  function buildAuthArea(u) {
    if (u && localStorage.getItem('auth_token')) {
      const initial = esc((u.full_name || '?').charAt(0).toUpperCase());
      const fname   = esc((u.full_name || '').split(' ')[0]);
      return `
        <div class="nav-user-area" id="nav-user-area">
          <a href="/pages/profile.html" class="nav-user-chip">
            <span class="nav-avatar">${initial}</span>
            <span class="nav-user-name">${fname}</span>
          </a>
          <button class="nav-logout-btn" onclick="navLogout()">Log Out</button>
        </div>`;
    }
    return `<a href="/pages/login.html" class="nav-login-btn" id="nav-login-btn">Log In</a>`;
  }

  /* ── Inject navbar ── */
  const html = `
  <nav class="shared-navbar" id="shared-navbar">
    <a class="nav-brand" href="/">
      <span>&#127891;</span>
      <div><strong>Counsellor.AI</strong><small>A Rising Education Initiative</small></div>
    </a>
    <button class="nav-toggle" id="nav-toggle" aria-label="Menu">&#9776;</button>
    <ul class="nav-menu" id="nav-menu">
      <li><a href="/" ${(path === '/' || path.endsWith('index.html')) ? 'class="active"' : ''}>Home</a></li>
      <li class="has-dropdown">
        <a href="/pages/dashboard.html" ${path.includes('dashboard') ? 'class="active"' : ''}>Predictors &#9660;</a>
        <ul class="dropdown">
          <li><a href="/pages/predict.html">MHT-CET</a></li>
          <li><a href="/pages/pharmacy.html">MH Pharmacy</a></li>
          <li><a href="/pages/bits.html">BITSAT</a></li>
          <li><a href="/pages/jee.html">JEE Main</a></li>
        </ul>
      </li>
      <li><a href="/pages/scholarships.html" ${path.includes('scholarships') ? 'class="active"' : ''}>Scholarships</a></li>
      <li><a href="/pages/resources.html" ${path.includes('resources') ? 'class="active"' : ''}>Study Materials</a></li>
      <li><a href="/pages/accommodation.html" ${path.includes('accommodation') ? 'class="active"' : ''}>Accommodation</a></li>
      <li><a href="/pages/mess.html" ${path.includes('mess') ? 'class="active"' : ''}>Mess &amp; Tiffin</a></li>
    </ul>
    <div id="nav-auth-slot">${buildAuthArea(user)}</div>
  </nav>`;

  document.body.insertAdjacentHTML('afterbegin', html);

  /* ── Hamburger ── */
  document.getElementById('nav-toggle').addEventListener('click', function() {
    document.getElementById('shared-navbar').classList.toggle('open');
  });

  /* ── Verify token with server (skip on login page) ── */
  const token = localStorage.getItem('auth_token');

  if (token && !isLoginPage) {
    fetch('http://127.0.0.1:5000/api/auth/me', {
      headers: { 'Authorization': 'Bearer ' + token }
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      const slot = document.getElementById('nav-auth-slot');
      if (!slot) return;
      if (data.user) {
        localStorage.setItem('auth_user', JSON.stringify(data.user));
        slot.innerHTML = buildAuthArea(data.user);
      } else {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_user');
        slot.innerHTML = buildAuthArea(null);
      }
    })
    .catch(function() { /* server unreachable — keep localStorage state */ });
  } else if (!token && user) {
    /* stale user data without token — clear it */
    localStorage.removeItem('auth_user');
    const slot = document.getElementById('nav-auth-slot');
    if (slot) slot.innerHTML = buildAuthArea(null);
  }

  /* ── Sync across tabs ── */
  window.addEventListener('storage', function(e) {
    if (e.key === 'auth_user' || e.key === 'auth_token') {
      let u = null;
      try { u = JSON.parse(localStorage.getItem('auth_user') || 'null'); } catch(err) {}
      const slot = document.getElementById('nav-auth-slot');
      if (slot) slot.innerHTML = buildAuthArea(u);
    }
  });

})();

/* ── Logout — called from navbar button ── */
function navLogout() {
  const token = localStorage.getItem('auth_token');
  if (token) {
    fetch('http://127.0.0.1:5000/api/auth/logout', {
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + token }
    }).catch(function() {});
  }
  localStorage.removeItem('auth_token');
  localStorage.removeItem('auth_user');
  /* Update navbar immediately before redirect */
  const slot = document.getElementById('nav-auth-slot');
  if (slot) slot.innerHTML = '<a href="/pages/login.html" class="nav-login-btn">Log In</a>';
  window.location.replace('/pages/login.html');
}

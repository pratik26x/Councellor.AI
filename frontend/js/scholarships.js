/* ═══════════════════════════════════════════════
   scholarships.js  –  Counsellor.AI
   Handles: fetch from API, filter, sort, modal
═══════════════════════════════════════════════ */

const API = 'http://127.0.0.1:5000/api/scholarships';

// All scholarships fetched from backend
let allScholarships = [];
// Active pill category filter
let activePillCat = '';

/* ── Fetch all scholarships on page load ── */
async function loadScholarships() {
  const grid = document.getElementById('scholarship-grid');
  grid.innerHTML = `
    <div class="spinner">
      <div class="spinner-ring"></div>
      <p>Loading scholarships...</p>
    </div>`;

  try {
    const res = await fetch(API);
    if (!res.ok) throw new Error('Server error');
    allScholarships = await res.json();
    applyFilters();
  } catch (err) {
    grid.innerHTML = `
      <div class="spinner">
        <p>⚠️ Could not load scholarships. Make sure the server is running on port 5000.</p>
        <button class="btn-clear" onclick="loadScholarships()">Retry</button>
      </div>`;
  }
}

/* ── Apply all active filters + sort ── */
function applyFilters() {
  const searchVal  = (document.getElementById('search-input')?.value || '').toLowerCase();
  const sortVal    = document.getElementById('sort-select')?.value || 'deadline';
  const deadlineF  = document.getElementById('deadline-filter')?.value || '';

  // Checked category checkboxes
  const checkedCats = [...document.querySelectorAll('#cat-filters input:checked')]
    .map(cb => cb.value);

  // Checked provider checkboxes
  const checkedProvs = [];
  if (document.getElementById('prov-govt')?.checked)  checkedProvs.push('government');
  if (document.getElementById('prov-pvt')?.checked)   checkedProvs.push('private');
  if (document.getElementById('prov-aicte')?.checked) checkedProvs.push('aicte');

  let filtered = allScholarships.filter(s => {
    // Search
    if (searchVal && !s.name.toLowerCase().includes(searchVal) &&
        !s.provider.toLowerCase().includes(searchVal) &&
        !s.description.toLowerCase().includes(searchVal)) return false;

    // Pill category
    if (activePillCat && !s.category.toLowerCase().includes(activePillCat.toLowerCase())) return false;

    // Sidebar category checkboxes (OR logic)
    if (checkedCats.length > 0) {
      const match = checkedCats.some(c => s.category.toLowerCase().includes(c.toLowerCase()));
      if (!match) return false;
    }

    // Provider checkboxes (OR logic)
    if (checkedProvs.length > 0) {
      const prov = s.provider.toLowerCase();
      const match = checkedProvs.some(p => prov.includes(p));
      if (!match) return false;
    }

    // Deadline filter
    if (deadlineF) {
      const months = parseInt(deadlineF);
      const deadlineDate = parseDeadline(s.deadline);
      if (deadlineDate) {
        const now = new Date();
        const diffMonths = (deadlineDate - now) / (1000 * 60 * 60 * 24 * 30);
        if (diffMonths > months || diffMonths < 0) return false;
      }
    }

    return true;
  });

  // Sort
  filtered = sortScholarships(filtered, sortVal);

  renderScholarships(filtered);
}

/* ── Sort helper ── */
function sortScholarships(list, by) {
  return [...list].sort((a, b) => {
    if (by === 'deadline') {
      const da = parseDeadline(a.deadline) || new Date('2099-01-01');
      const db = parseDeadline(b.deadline) || new Date('2099-01-01');
      return da - db;
    }
    if (by === 'amount') {
      return extractAmount(b.amount) - extractAmount(a.amount);
    }
    if (by === 'name') {
      return a.name.localeCompare(b.name);
    }
    return 0;
  });
}

/* ── Render cards ── */
function renderScholarships(list) {
  const grid = document.getElementById('scholarship-grid');
  const noRes = document.getElementById('no-results');
  const count = document.getElementById('result-count');

  count.textContent = `${list.length} scholarship${list.length !== 1 ? 's' : ''} found`;

  if (list.length === 0) {
    grid.innerHTML = '';
    noRes.classList.remove('hidden');
    return;
  }
  noRes.classList.add('hidden');

  grid.innerHTML = list.map(s => buildCard(s)).join('');
}

/* ── Build a single card HTML ── */
function buildCard(s) {
  const catClass  = getCatClass(s.category);
  const catLabel  = s.category || 'General';
  const deadline  = s.deadline || 'Open';
  const dlClass   = getDeadlineClass(s.deadline);
  const dlIcon    = dlClass === 'deadline-soon' ? '🔴' : dlClass === 'deadline-ok' ? '🟢' : '📅';

  return `
  <div class="sch-card" onclick="openModal(${s.id})">
    <div class="sch-card-top">
      <div>
        <span class="sch-cat-badge ${catClass}">${catLabel}</span>
      </div>
    </div>
    <h3>${escHtml(s.name)}</h3>
    <p class="sch-provider">🏛️ ${escHtml(s.provider)}</p>
    <div class="sch-amount">${escHtml(s.amount)}</div>
    <div class="sch-eligibility">✅ ${escHtml(s.eligibility)}</div>
    <div class="sch-meta">
      <span class="sch-meta-item sch-deadline ${dlClass}">${dlIcon} Deadline: ${escHtml(deadline)}</span>
    </div>
    <div class="sch-card-footer">
      <a href="${escHtml(s.apply_link || '#')}" target="_blank" class="btn-apply" onclick="event.stopPropagation()">Apply Now →</a>
      <button class="btn-details" onclick="event.stopPropagation(); openModal(${s.id})">Details</button>
    </div>
  </div>`;
}

/* ── Open detail modal ── */
function openModal(id) {
  const s = allScholarships.find(x => x.id === id);
  if (!s) return;

  const catClass = getCatClass(s.category);
  const dlClass  = getDeadlineClass(s.deadline);
  const dlIcon   = dlClass === 'deadline-soon' ? '⚠️' : '📅';

  document.getElementById('modal-content').innerHTML = `
    <div class="modal-header">
      <span class="sch-cat-badge ${catClass}">${escHtml(s.category || 'General')}</span>
      <h2>${escHtml(s.name)}</h2>
      <p class="provider">🏛️ ${escHtml(s.provider)}</p>
    </div>

    <div class="modal-amount">
      <span>${escHtml(s.amount)}</span>
      <p>Annual scholarship amount</p>
    </div>

    <div class="modal-deadline-box">
      <span>${dlIcon}</span>
      <div>
        <strong>Application Deadline: ${escHtml(s.deadline || 'Open')}</strong>
        <p>${dlClass === 'deadline-soon' ? 'Deadline approaching — apply soon!' : 'You have time, but apply early.'}</p>
      </div>
    </div>

    <div class="modal-section">
      <h4>Eligibility Criteria</h4>
      <p>${escHtml(s.eligibility)}</p>
    </div>

    <div class="modal-section">
      <h4>About This Scholarship</h4>
      <p>${escHtml(s.description)}</p>
    </div>

    <a href="${escHtml(s.apply_link || '#')}" target="_blank" class="modal-apply-btn">
      🚀 Apply on Official Portal →
    </a>`;

  document.getElementById('detail-modal').classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

/* ── Close modal ── */
function closeModal() {
  document.getElementById('detail-modal').classList.add('hidden');
  document.body.style.overflow = '';
}

// Close modal on overlay click
document.getElementById('detail-modal').addEventListener('click', function(e) {
  if (e.target === this) closeModal();
});

// Close modal on Escape key
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

/* ── Pill filter ── */
function setPill(el, cat) {
  document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
  el.classList.add('active');
  activePillCat = cat;
  applyFilters();
}

/* ── Eligibility checker ── */
function runEligibilityCheck() {
  const cat    = document.getElementById('chk-category').value;
  const income = document.getElementById('chk-income').value;
  const level  = document.getElementById('chk-level').value;

  // Set pill to matching category
  if (cat) {
    const pill = [...document.querySelectorAll('.pill')].find(p => p.dataset.cat === cat);
    if (pill) setPill(pill, cat);
    else { activePillCat = cat; applyFilters(); }
  } else {
    const allPill = document.querySelector('.pill[data-cat=""]');
    if (allPill) setPill(allPill, '');
  }

  // Scroll to listings
  document.querySelector('.main-content').scrollIntoView({ behavior: 'smooth' });
}

/* ── Clear all filters ── */
function clearFilters() {
  document.getElementById('search-input').value = '';
  document.getElementById('sort-select').value = 'deadline';
  document.getElementById('deadline-filter').value = '';
  document.querySelectorAll('#cat-filters input').forEach(cb => cb.checked = false);
  ['prov-govt','prov-pvt','prov-aicte'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.checked = false;
  });
  activePillCat = '';
  document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
  document.querySelector('.pill[data-cat=""]')?.classList.add('active');
  applyFilters();
}

/* ── Helpers ── */
function getCatClass(cat) {
  if (!cat) return 'cat-default';
  const c = cat.toLowerCase();
  if (c.includes('merit'))    return 'cat-Merit';
  if (c.includes('sc') || c.includes('st')) return 'cat-SCST';
  if (c.includes('obc'))      return 'cat-OBC';
  if (c.includes('ews'))      return 'cat-EWS';
  if (c.includes('girl'))     return 'cat-Girls';
  if (c.includes('sport'))    return 'cat-Sports';
  if (c.includes('minority')) return 'cat-Minority';
  return 'cat-default';
}

function getDeadlineClass(deadline) {
  if (!deadline) return 'deadline-normal';
  const d = parseDeadline(deadline);
  if (!d) return 'deadline-normal';
  const now = new Date();
  const diffDays = (d - now) / (1000 * 60 * 60 * 24);
  if (diffDays < 0)  return 'deadline-normal';
  if (diffDays < 30) return 'deadline-soon';
  if (diffDays < 90) return 'deadline-ok';
  return 'deadline-normal';
}

function parseDeadline(str) {
  if (!str) return null;
  // Handles "31 Oct 2025", "30 Nov 2025", "2025-10-31" etc.
  const d = new Date(str);
  return isNaN(d.getTime()) ? null : d;
}

function extractAmount(str) {
  if (!str) return 0;
  const nums = str.replace(/,/g, '').match(/\d+/g);
  if (!nums) return 0;
  return Math.max(...nums.map(Number));
}

function escHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/* ── Init ── */
document.addEventListener('DOMContentLoaded', loadScholarships);

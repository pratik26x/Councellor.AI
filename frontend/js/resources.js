/* ═══════════════════════════════════════════════
   resources.js  –  Counsellor.AI
   PYQs & Study Materials page logic
═══════════════════════════════════════════════ */

const API = 'http://127.0.0.1:5000/api/resources';

let allResources = [];   // full dataset from server
let activeTab    = '';   // current type tab filter

/* ─────────────────────────────────────────────
   INIT
───────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  loadResources();

  // Show/hide search clear button
  document.getElementById('global-search').addEventListener('input', function () {
    document.getElementById('search-clear').style.display = this.value ? 'block' : 'none';
  });
});

/* ─────────────────────────────────────────────
   FETCH
───────────────────────────────────────────── */
async function loadResources() {
  showSpinner();
  try {
    const res = await fetch(API);
    if (!res.ok) throw new Error('Server error');
    allResources = await res.json();
    updateStatBar();
    applyFilters();
  } catch {
    document.getElementById('resource-grid').innerHTML = `
      <div class="spinner">
        <p>⚠️ Could not load resources. Make sure the server is running on port 5000.</p>
        <button class="btn-clear-all" onclick="loadResources()">Retry</button>
      </div>`;
  }
}

/* ─────────────────────────────────────────────
   STAT BAR
───────────────────────────────────────────── */
function updateStatBar() {
  const count = t => allResources.filter(r => r.resource_type === t).length;
  document.getElementById('total-count').textContent  = allResources.length;
  document.getElementById('pyq-count').textContent    = count('PYQ');
  document.getElementById('notes-count').textContent  =
    allResources.filter(r => r.resource_type === 'Notes' || r.resource_type === 'Formula Sheet').length;
  document.getElementById('video-count').textContent  = count('Video');
  document.getElementById('mock-count').textContent   = count('Mock Test');
}

/* ─────────────────────────────────────────────
   FILTERS
───────────────────────────────────────────── */
function applyFilters() {
  const search  = (document.getElementById('global-search').value || '').toLowerCase();
  const examVal = document.querySelector('input[name="exam"]:checked')?.value || '';
  const yearVal = document.getElementById('year-filter').value;
  const sortVal = document.getElementById('sort-select').value;

  // Checked subjects
  const subjects = [...document.querySelectorAll('.checkbox-list input[type="checkbox"]')]
    .filter(cb => cb.value !== 'PYQ' && cb.value !== 'Notes' && cb.value !== 'Formula Sheet' && cb.value !== 'Video' && cb.value !== 'Mock Test' && cb.checked)
    .map(cb => cb.value);

  // Checked types (from sidebar checkboxes)
  const types = [...document.querySelectorAll('.checkbox-list input[type="checkbox"]')]
    .filter(cb => ['PYQ','Notes','Formula Sheet','Video','Mock Test'].includes(cb.value) && cb.checked)
    .map(cb => cb.value);

  let filtered = allResources.filter(r => {
    // Global search
    if (search) {
      const haystack = `${r.title} ${r.description} ${r.tags} ${r.exam} ${r.subject}`.toLowerCase();
      if (!haystack.includes(search)) return false;
    }
    // Tab type filter
    if (activeTab && r.resource_type !== activeTab) return false;
    // Sidebar type checkboxes (OR)
    if (types.length > 0 && !types.includes(r.resource_type)) return false;
    // Exam radio
    if (examVal && !r.exam.toLowerCase().includes(examVal.toLowerCase())) return false;
    // Subject checkboxes (OR)
    if (subjects.length > 0 && !subjects.some(s => r.subject.toLowerCase().includes(s.toLowerCase()))) return false;
    // Year
    if (yearVal && r.year && !r.year.includes(yearVal)) return false;
    return true;
  });

  // Sort
  filtered = sortResources(filtered, sortVal);

  renderGrid(filtered);
}

function sortResources(list, by) {
  return [...list].sort((a, b) => {
    if (by === 'popular') return b.downloads - a.downloads;
    if (by === 'newest')  return (b.year || '0').localeCompare(a.year || '0');
    if (by === 'az')      return a.title.localeCompare(b.title);
    return 0;
  });
}

/* ─────────────────────────────────────────────
   RENDER
───────────────────────────────────────────── */
function renderGrid(list) {
  const grid  = document.getElementById('resource-grid');
  const noRes = document.getElementById('no-results');
  document.getElementById('result-count').textContent =
    `${list.length} resource${list.length !== 1 ? 's' : ''} found`;

  if (list.length === 0) {
    grid.innerHTML = '';
    noRes.classList.remove('hidden');
    return;
  }
  noRes.classList.add('hidden');
  grid.innerHTML = list.map(buildCard).join('');
}

function buildCard(r) {
  const typeKey   = r.resource_type.replace(/\s+/g, '-');
  const typeIcon  = typeIcon_(r.resource_type);
  const dlLabel   = r.resource_type === 'Video' ? 'Watch Now' :
                    r.resource_type === 'Mock Test' ? 'Start Test' : 'Download';
  const dlCount   = r.downloads > 0
    ? `<span class="res-downloads">⬇️ ${r.downloads.toLocaleString()} downloads</span>` : '';

  return `
  <div class="res-card type-${typeKey}" onclick="openModal(${r.id})">
    <div class="res-card-top">
      <span class="type-badge badge-${typeKey}">${typeIcon} ${r.resource_type}</span>
      ${r.is_free ? '<span class="free-badge">FREE</span>' : ''}
    </div>
    <h3>${esc(r.title)}</h3>
    <div class="res-meta">
      <span class="res-meta-tag exam-tag">${esc(r.exam)}</span>
      <span class="res-meta-tag subj-tag">${esc(r.subject)}</span>
      ${r.year ? `<span class="res-meta-tag">${esc(r.year)}</span>` : ''}
    </div>
    <p class="res-desc">${esc(r.description)}</p>
    ${dlCount}
    <div class="res-card-footer">
      <a href="${esc(r.file_url || '#')}" target="_blank"
         class="btn-download"
         onclick="event.stopPropagation(); trackDownload(${r.id})">
        ${dlLabel} →
      </a>
      <button class="btn-view" onclick="event.stopPropagation(); openModal(${r.id})">Details</button>
    </div>
  </div>`;
}

/* ─────────────────────────────────────────────
   MODAL
───────────────────────────────────────────── */
function openModal(id) {
  const r = allResources.find(x => x.id === id);
  if (!r) return;

  const typeKey  = r.resource_type.replace(/\s+/g, '-');
  const typeIcon = typeIcon_(r.resource_type);
  const dlLabel  = r.resource_type === 'Video' ? '▶ Watch on YouTube' :
                   r.resource_type === 'Mock Test' ? '🎯 Start Mock Test' : '⬇️ Download Free';
  const tags = (r.tags || '').split(',').filter(Boolean);

  document.getElementById('modal-body').innerHTML = `
    <span class="type-badge badge-${typeKey} modal-type-badge">${typeIcon} ${r.resource_type}</span>
    <h2 class="modal-title">${esc(r.title)}</h2>
    <div class="modal-meta">
      <span class="res-meta-tag exam-tag">${esc(r.exam)}</span>
      <span class="res-meta-tag subj-tag">${esc(r.subject)}</span>
      ${r.year ? `<span class="res-meta-tag">📅 ${esc(r.year)}</span>` : ''}
      ${r.is_free ? '<span class="free-badge">FREE</span>' : ''}
    </div>
    <p class="modal-desc">${esc(r.description)}</p>
    ${tags.length ? `
    <div class="modal-tags">
      ${tags.map(t => `<span class="modal-tag">#${esc(t.trim())}</span>`).join('')}
    </div>` : ''}
    <a href="${esc(r.file_url || '#')}" target="_blank"
       class="modal-dl-btn"
       onclick="trackDownload(${r.id})">
      ${dlLabel}
    </a>
    ${r.downloads > 0 ? `<p class="modal-downloads">⬇️ Downloaded ${r.downloads.toLocaleString()} times</p>` : ''}`;

  document.getElementById('detail-modal').classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  document.getElementById('detail-modal').classList.add('hidden');
  document.body.style.overflow = '';
}

document.getElementById('detail-modal').addEventListener('click', function (e) {
  if (e.target === this) closeModal();
});
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

/* ─────────────────────────────────────────────
   TRACK DOWNLOAD
───────────────────────────────────────────── */
async function trackDownload(id) {
  try {
    await fetch(`${API}/${id}/download`, { method: 'POST' });
    // Update local count
    const r = allResources.find(x => x.id === id);
    if (r) r.downloads += 1;
  } catch { /* silent */ }
}

/* ─────────────────────────────────────────────
   TAB SWITCH
───────────────────────────────────────────── */
function setTab(el, type) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  activeTab = type;
  applyFilters();
}

/* ─────────────────────────────────────────────
   CLEAR
───────────────────────────────────────────── */
function clearSearch() {
  document.getElementById('global-search').value = '';
  document.getElementById('search-clear').style.display = 'none';
  applyFilters();
}

function clearAllFilters() {
  document.getElementById('global-search').value = '';
  document.getElementById('search-clear').style.display = 'none';
  document.getElementById('year-filter').value = '';
  document.getElementById('sort-select').value = 'popular';
  document.querySelector('input[name="exam"][value=""]').checked = true;
  document.querySelectorAll('.checkbox-list input[type="checkbox"]').forEach(cb => cb.checked = false);
  activeTab = '';
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelector('.tab[data-type=""]').classList.add('active');
  applyFilters();
}

/* ─────────────────────────────────────────────
   HELPERS
───────────────────────────────────────────── */
function showSpinner() {
  document.getElementById('resource-grid').innerHTML = `
    <div class="spinner">
      <div class="spinner-ring"></div>
      <p>Loading resources…</p>
    </div>`;
}

function typeIcon_(type) {
  const map = {
    'PYQ': '📝', 'Notes': '📓', 'Formula Sheet': '📋',
    'Video': '🎥', 'Mock Test': '🎯'
  };
  return map[type] || '📄';
}

function esc(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g,'&amp;').replace(/</g,'&lt;')
    .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

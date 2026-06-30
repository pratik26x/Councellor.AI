/* home.js — Counsellor.AI homepage logic */

const SCH_API = 'http://127.0.0.1:5000/api/scholarships';
let allScholarships = [];
let activeCat = '';

/* ══════════════════════════════════════════
   SCHOLARSHIPS
══════════════════════════════════════════ */
async function loadScholarships() {
  try {
    const res = await fetch(SCH_API);
    if (!res.ok) throw new Error();
    allScholarships = await res.json();
    renderScholarships(allScholarships);
  } catch {
    document.getElementById('sch-home-grid').innerHTML =
      `<div class="sch-home-loading">Could not load scholarships. Make sure the server is running.</div>`;
  }
}

function filterScholarships(btn, cat) {
  document.querySelectorAll('.sch-pill').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  activeCat = cat;
  const filtered = cat
    ? allScholarships.filter(s => s.category && s.category.toLowerCase().includes(cat.toLowerCase()))
    : allScholarships;
  renderScholarships(filtered);
}

function renderScholarships(list) {
  const grid  = document.getElementById('sch-home-grid');
  const count = document.getElementById('sch-home-count');

  // Show max 6 on homepage
  const display = list.slice(0, 6);
  count.textContent = `Showing ${display.length} of ${list.length} scholarships`;

  if (display.length === 0) {
    grid.innerHTML = `<div class="sch-home-loading">No scholarships found for this category.</div>`;
    return;
  }

  grid.innerHTML = display.map(s => buildSchCard(s)).join('');
}

function buildSchCard(s) {
  const catKey   = getCatKey(s.category);
  const dlClass  = getDeadlineClass(s.deadline);
  const dlLabel  = s.deadline || 'Open';

  return `
  <div class="sch-home-card ${catKey}" onclick="window.location='/pages/scholarships.html'">
    <div class="sch-home-top">
      <span class="sch-home-badge ${catKey}">${esc(s.category || 'General')}</span>
      <span class="sch-home-deadline ${dlClass}">&#128197; ${esc(dlLabel)}</span>
    </div>
    <h4>${esc(s.name)}</h4>
    <p class="sch-home-provider">&#127963; ${esc(s.provider)}</p>
    <div class="sch-home-amount">${esc(s.amount)}</div>
    <div class="sch-home-eligibility">&#9989; ${esc(s.eligibility)}</div>
    <div class="sch-home-footer">
      <a href="${esc(s.apply_link || '/pages/scholarships.html')}" target="_blank"
         class="sch-home-apply" onclick="event.stopPropagation()">
        Apply Now &rarr;
      </a>
    </div>
  </div>`;
}

function getCatKey(cat) {
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
  if (!deadline) return 'dl-normal';
  const d = new Date(deadline);
  if (isNaN(d)) return 'dl-normal';
  const days = (d - new Date()) / 86400000;
  if (days < 0)  return 'dl-normal';
  if (days < 30) return 'dl-soon';
  if (days < 90) return 'dl-ok';
  return 'dl-normal';
}

/* ══════════════════════════════════════════
   NEWSLETTER
══════════════════════════════════════════ */
function subscribeNewsletter(e) {
  e.preventDefault();
  const email = e.target.querySelector('input[type="email"]').value;
  if (email) {
    showToast('Thanks for subscribing!', 'success');
    e.target.reset();
  }
}

/* ══════════════════════════════════════════
   TOAST
══════════════════════════════════════════ */
function showToast(msg, type = 'success') {
  let toast = document.querySelector('.toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.className = 'toast';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.className = `toast ${type}`;
  setTimeout(() => toast.classList.add('show'), 10);
  setTimeout(() => toast.classList.remove('show'), 3500);
}

/* ══════════════════════════════════════════
   HAMBURGER & INIT
══════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', () => {
  // Sticky navbar shadow on scroll
  window.addEventListener('scroll', () => {
    const nav = document.getElementById('shared-navbar');
    if (nav) nav.style.boxShadow = window.scrollY > 10
      ? '0 4px 20px rgba(0,0,0,.18)' : '0 2px 16px rgba(0,0,0,.25)';
  });

  loadScholarships();
});

/* ══════════════════════════════════════════
   HELPERS
══════════════════════════════════════════ */
function esc(s) {
  return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

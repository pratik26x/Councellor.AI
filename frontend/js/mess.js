/* mess.js */
const API = 'http://127.0.0.1:5000/api/mess';
let allServices = [];

/* ── Load ── */
async function loadServices(params = {}) {
  showSpinner('mess-grid');
  try {
    const qs = new URLSearchParams(params).toString();
    const res = await fetch(`${API}${qs ? '?' + qs : ''}`);
    if (!res.ok) throw new Error();
    allServices = await res.json();
    sortAndRender();
  } catch {
    document.getElementById('mess-grid').innerHTML =
      `<div class="no-results"><span>&#9888;</span><p>Could not load services. Make sure the server is running.</p><button class="btn-reset" onclick="loadServices()">Retry</button></div>`;
  }
}

/* ── Search ── */
function searchMess() {
  const params = {};
  const city    = document.getElementById('f-city').value.trim();
  const type    = document.getElementById('f-type').value;
  const cuisine = document.getElementById('f-cuisine')?.value || '';
  const cost    = document.getElementById('f-cost').value;
  if (city)    params.city     = city;
  if (type)    params.type     = type;
  if (cost)    params.max_cost = cost;
  loadServices(params);
}

function resetFilters() {
  document.getElementById('f-city').value  = '';
  document.getElementById('f-type').value  = '';
  if (document.getElementById('f-cuisine')) document.getElementById('f-cuisine').value = '';
  document.getElementById('f-cost').value  = '';
  loadServices();
}

/* ── Sort & Render ── */
function sortAndRender() {
  const sort = document.getElementById('mess-sort').value;
  let sorted = [...allServices];
  if (sort === 'cost-asc')  sorted.sort((a,b) => a.monthly_cost - b.monthly_cost);
  if (sort === 'cost-desc') sorted.sort((a,b) => b.monthly_cost - a.monthly_cost);
  if (sort === 'az')        sorted.sort((a,b) => a.name.localeCompare(b.name));
  renderServices(sorted);
}

/* ── Render ── */
function renderServices(list) {
  const grid = document.getElementById('mess-grid');
  document.getElementById('mess-count').textContent =
    `${list.length} service${list.length !== 1 ? 's' : ''} found`;

  if (list.length === 0) {
    grid.innerHTML = `<div class="no-results"><span>&#128533;</span><p>No services match your search.</p><button class="btn-reset" onclick="resetFilters()">Clear Filters</button></div>`;
    return;
  }
  grid.innerHTML = list.map(buildCard).join('');
}

function buildCard(r) {
  const typeIcon = r.type === 'Mess' ? '&#127857;' : r.type === 'Tiffin' ? '&#127871;' : '&#9749;';
  const costDisplay = r.monthly_cost > 0
    ? `<div class="price-val">Rs.${r.monthly_cost.toLocaleString()}</div><div class="price-label">per month</div>`
    : `<div class="price-val" style="color:#6b7280;">Free / Pay per meal</div><div class="price-label">no subscription needed</div>`;

  return `
  <div class="listing-card" onclick="openDetail(${r.id})">
    <div class="card-header">
      <span class="card-type-badge badge-${r.type}">${typeIcon} ${r.type}</span>
    </div>
    <div class="card-title">${esc(r.name)}</div>
    <div class="card-location">&#128205; ${esc(r.area)}, ${esc(r.city)}</div>
    <div class="card-price">${costDisplay}</div>
    <div class="card-amenities">
      ${r.cuisine ? `<span class="amenity-tag">&#127869; ${esc(r.cuisine)}</span>` : ''}
      ${r.timing  ? `<span class="amenity-tag">&#128336; ${esc(r.timing)}</span>`  : ''}
    </div>
    <div class="card-desc">${esc(r.description)}</div>
    <div class="card-footer">
      <button class="btn-contact" onclick="event.stopPropagation(); callContact('${esc(r.contact)}')">&#128222; Contact</button>
      <button class="btn-details-sm" onclick="event.stopPropagation(); openDetail(${r.id})">Details</button>
    </div>
  </div>`;
}

/* ── Detail Modal ── */
function openDetail(id) {
  const r = allServices.find(x => x.id === id);
  if (!r) return;
  const typeIcon = r.type === 'Mess' ? '&#127857;' : r.type === 'Tiffin' ? '&#127871;' : '&#9749;';
  const costDisplay = r.monthly_cost > 0
    ? `<div class="big-price">Rs.${r.monthly_cost.toLocaleString()}</div><p>per month</p>`
    : `<div class="big-price" style="color:#6b7280;font-size:22px;">Free / Pay per meal</div>`;

  document.getElementById('detail-body').innerHTML = `
    <span class="card-type-badge badge-${r.type} detail-type-badge">${typeIcon} ${r.type}</span>
    <h2 class="detail-title">${esc(r.name)}</h2>
    <p class="detail-location">&#128205; ${esc(r.area)}, ${esc(r.city)}</p>
    <div class="detail-price-box">${costDisplay}</div>
    <div class="detail-section">
      <h4>Cuisine &amp; Timings</h4>
      <p>${r.cuisine ? '&#127869; ' + esc(r.cuisine) : 'Not specified'}</p>
      <p style="margin-top:6px">${r.timing ? '&#128336; ' + esc(r.timing) : ''}</p>
    </div>
    <div class="detail-section"><h4>About this Service</h4><p>${esc(r.description)}</p></div>
    <button class="detail-contact-btn" onclick="callContact('${esc(r.contact)}')">&#128222; Call / WhatsApp: ${esc(r.contact)}</button>`;

  document.getElementById('detail-modal').classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function closeDetailModal() {
  document.getElementById('detail-modal').classList.add('hidden');
  document.body.style.overflow = '';
}

/* ── Add Service Modal ── */
function openModal() {
  document.getElementById('add-modal').classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}
function closeModal() {
  document.getElementById('add-modal').classList.add('hidden');
  document.body.style.overflow = '';
}

async function submitListing(e) {
  e.preventDefault();
  const form = e.target;
  const data = {
    name:        form.name.value,
    type:        form.type.value,
    city:        form.city.value,
    area:        form.area.value,
    monthly_cost: parseInt(form.monthly_cost.value) || 0,
    contact:     form.contact.value,
    cuisine:     form.cuisine.value,
    timing:      form.timing.value,
    description: form.description.value,
  };
  try {
    const res = await fetch(API, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data) });
    if (!res.ok) throw new Error();
    alert('Service submitted successfully! It will be reviewed and published shortly.');
    form.reset();
    closeModal();
    loadServices();
  } catch {
    alert('Failed to submit. Please try again.');
  }
}

/* ── Helpers ── */
function callContact(num) {
  if (confirm(`Call ${num}?`)) window.open(`tel:${num}`);
}

function showSpinner(id) {
  document.getElementById(id).innerHTML =
    `<div class="spinner"><div class="spinner-ring"></div><p>Loading services...</p></div>`;
}

function esc(s) {
  if (!s) return '';
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

document.addEventListener('click', e => {
  if (e.target.id === 'detail-modal') closeDetailModal();
  if (e.target.id === 'add-modal')    closeModal();
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') { closeDetailModal(); closeModal(); }
});

document.addEventListener('DOMContentLoaded', loadServices);

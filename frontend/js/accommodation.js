/* accommodation.js */
const API = 'http://127.0.0.1:5000/api/accommodation';
let allListings = [];

/* ── Load ── */
async function loadListings(params = {}) {
  showSpinner('acc-grid');
  try {
    const qs = new URLSearchParams(params).toString();
    const res = await fetch(`${API}${qs ? '?' + qs : ''}`);
    if (!res.ok) throw new Error();
    allListings = await res.json();
    sortAndRender();
  } catch {
    document.getElementById('acc-grid').innerHTML =
      `<div class="no-results"><span>&#9888;</span><p>Could not load listings. Make sure the server is running.</p><button class="btn-reset" onclick="loadListings()">Retry</button></div>`;
  }
}

/* ── Search ── */
function searchAccommodation() {
  const params = {};
  const city   = document.getElementById('f-city').value.trim();
  const type   = document.getElementById('f-type').value;
  const gender = document.getElementById('f-gender').value;
  const rent   = document.getElementById('f-rent').value;
  if (city)   params.city     = city;
  if (type)   params.type     = type;
  if (gender) params.gender   = gender;
  if (rent)   params.max_rent = rent;
  loadListings(params);
}

function resetFilters() {
  document.getElementById('f-city').value   = '';
  document.getElementById('f-type').value   = '';
  document.getElementById('f-gender').value = '';
  document.getElementById('f-rent').value   = '';
  loadListings();
}

/* ── Sort & Render ── */
function sortAndRender() {
  const sort = document.getElementById('acc-sort').value;
  let sorted = [...allListings];
  if (sort === 'rent-asc')  sorted.sort((a,b) => a.rent - b.rent);
  if (sort === 'rent-desc') sorted.sort((a,b) => b.rent - a.rent);
  if (sort === 'az')        sorted.sort((a,b) => a.title.localeCompare(b.title));
  renderListings(sorted);
}

/* ── Render ── */
function renderListings(list) {
  const grid = document.getElementById('acc-grid');
  document.getElementById('acc-count').textContent =
    `${list.length} listing${list.length !== 1 ? 's' : ''} found`;

  if (list.length === 0) {
    grid.innerHTML = `<div class="no-results"><span>&#128533;</span><p>No listings match your search.</p><button class="btn-reset" onclick="resetFilters()">Clear Filters</button></div>`;
    return;
  }
  grid.innerHTML = list.map(buildCard).join('');
}

function buildCard(r) {
  const amenities = (r.amenities || '').split(',').filter(Boolean)
    .map(a => `<span class="amenity-tag">${esc(a.trim())}</span>`).join('');
  const genderIcon = r.gender === 'Boys' ? '&#128104;' : r.gender === 'Girls' ? '&#128105;' : '&#128101;';

  return `
  <div class="listing-card" onclick="openDetail(${r.id})">
    <div class="card-header">
      <span class="card-type-badge badge-${r.type}">${r.type}</span>
      <span class="gender-badge">${genderIcon} ${r.gender}</span>
    </div>
    <div class="card-title">${esc(r.title)}</div>
    <div class="card-location">&#128205; ${esc(r.area)}, ${esc(r.city)}</div>
    <div class="card-price">
      <div class="price-val">Rs.${r.rent.toLocaleString()}</div>
      <div class="price-label">per month</div>
    </div>
    ${amenities ? `<div class="card-amenities">${amenities}</div>` : ''}
    <div class="card-desc">${esc(r.description)}</div>
    <div class="card-footer">
      <button class="btn-contact" onclick="event.stopPropagation(); callContact('${esc(r.contact)}')">&#128222; Contact</button>
      <button class="btn-details-sm" onclick="event.stopPropagation(); openDetail(${r.id})">Details</button>
    </div>
  </div>`;
}

/* ── Detail Modal ── */
function openDetail(id) {
  const r = allListings.find(x => x.id === id);
  if (!r) return;
  const amenities = (r.amenities || '').split(',').filter(Boolean)
    .map(a => `<span class="amenity-tag">${esc(a.trim())}</span>`).join('');
  const genderIcon = r.gender === 'Boys' ? '&#128104;' : r.gender === 'Girls' ? '&#128105;' : '&#128101;';

  document.getElementById('detail-body').innerHTML = `
    <span class="card-type-badge badge-${r.type} detail-type-badge">${r.type}</span>
    <h2 class="detail-title">${esc(r.title)}</h2>
    <p class="detail-location">&#128205; ${esc(r.area)}, ${esc(r.city)} &nbsp;|&nbsp; ${genderIcon} ${esc(r.gender)}</p>
    <div class="detail-price-box">
      <div class="big-price">Rs.${r.rent.toLocaleString()}</div>
      <p>per month</p>
    </div>
    ${amenities ? `<div class="detail-section"><h4>Amenities</h4><div class="amenities-list">${amenities}</div></div>` : ''}
    <div class="detail-section"><h4>About this Listing</h4><p>${esc(r.description)}</p></div>
    <button class="detail-contact-btn" onclick="callContact('${esc(r.contact)}')">&#128222; Call / WhatsApp: ${esc(r.contact)}</button>`;

  document.getElementById('detail-modal').classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function closeDetailModal() {
  document.getElementById('detail-modal').classList.add('hidden');
  document.body.style.overflow = '';
}

/* ── Add Listing Modal ── */
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
    title:       form.title.value,
    type:        form.type.value,
    city:        form.city.value,
    area:        form.area.value,
    rent:        parseInt(form.rent.value) || 0,
    contact:     form.contact.value,
    gender:      form.gender.value,
    amenities:   form.amenities.value,
    description: form.description.value,
  };
  try {
    const res = await fetch(API, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data) });
    if (!res.ok) throw new Error();
    alert('Listing submitted successfully! It will be reviewed and published shortly.');
    form.reset();
    closeModal();
    loadListings();
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
    `<div class="spinner"><div class="spinner-ring"></div><p>Loading listings...</p></div>`;
}

function esc(s) {
  if (!s) return '';
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

/* ── Close modals on overlay click / Escape ── */
document.addEventListener('click', e => {
  if (e.target.id === 'detail-modal') closeDetailModal();
  if (e.target.id === 'add-modal')    closeModal();
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') { closeDetailModal(); closeModal(); }
});

/* ── Init ── */
document.addEventListener('DOMContentLoaded', loadListings);

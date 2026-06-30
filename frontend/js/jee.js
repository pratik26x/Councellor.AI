/* jee.js — JEE College Predictor */
const API = 'http://127.0.0.1:5000/api/predict/jee';

document.getElementById('prediction-form').addEventListener('submit', async function (e) {
  e.preventDefault();

  const rank     = parseInt(document.getElementById('Rank').value);
  const gender   = document.getElementById('gender').value;
  const category = document.getElementById('category').value;
  const branch   = this.querySelector('[name="branch"]').value.trim();
  const cities   = this.querySelector('[name="preferred_cities"]').value.trim();

  if (!rank || rank < 1) {
    showError('Please enter a valid JEE rank.');
    return;
  }
  if (!gender || !category) {
    showError('Please select Gender and Category.');
    return;
  }

  showLoading();

  try {
    const res = await fetch(API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        rank,
        gender,
        category,
        branch:           branch || '',
        preferred_cities: cities
      })
    });

    if (!res.ok) throw new Error(`Server error: ${res.status}`);
    const data = await res.json();
    renderResults(data, rank);
  } catch (err) {
    showError('Could not connect to the server. Make sure it is running on port 5000.');
    console.error(err);
  }
});

function renderResults(data, rank) {
  const tbody = document.querySelector('#results-table tbody');

  if (!data || data.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:30px;color:#888;">
      &#128533; No institutes found for rank ${rank.toLocaleString()}. Try a higher rank or change filters.
    </td></tr>`;
    return;
  }

  tbody.innerHTML = data.map((r) => {
    // Handle both old and new column name formats
    const institute = r['Institute'] || r['institute_short'] || '-';
    const program   = r['Academic Program Name'] || r['program_name'] || '-';
    const instType  = r['Institute Type'] || r['institute_type'] || '-';
    const seatType  = r['Seat Type'] || r['category'] || '-';
    const opening   = r['Opening Rank'] || r['opening_rank'] || '-';
    const closing   = r['Closing Rank'] || r['closing_rank'] || '-';

    return `<tr>
      <td><strong>${esc(institute)}</strong><br/><small style="color:#888">${esc(instType)}</small></td>
      <td>${esc(program)}</td>
      <td>${esc(seatType)}</td>
      <td>${esc(String(opening))}</td>
      <td><span class="cutoff-badge">${esc(String(closing))}</span></td>
    </tr>`;
  }).join('');

  document.getElementById('results-table').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function showLoading() {
  const tbody = document.querySelector('#results-table tbody');
  tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:30px;">
    <div style="display:inline-block;width:32px;height:32px;border:3px solid #eee;border-top-color:#FFBF23;border-radius:50%;animation:spin .8s linear infinite;"></div>
    <p style="margin-top:12px;color:#888;">Finding institutes for you...</p>
  </td></tr>`;
}

function showError(msg) {
  const tbody = document.querySelector('#results-table tbody');
  tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:30px;color:#888;">&#9888; ${msg}</td></tr>`;
}

function esc(s) {
  return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

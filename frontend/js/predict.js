/* predict.js — MHT-CET College Predictor */
const API = 'http://127.0.0.1:5000/api/predict/mhtcet';

document.getElementById('prediction-form').addEventListener('submit', async function (e) {
  e.preventDefault();

  const percentile = document.getElementById('percentile').value.trim();
  const category   = document.getElementById('category').value;
  const branch     = this.querySelector('[name="branch"]').value.trim();
  const cities     = this.querySelector('[name="preferred_cities"]').value.trim();

  if (!percentile || !category) {
    showError('Please fill in Percentile and Category.');
    return;
  }

  showLoading();

  try {
    const res = await fetch(API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        percentile:       parseFloat(percentile),
        category:         category,
        branch:           branch || null,
        preferred_cities: cities
      })
    });

    if (!res.ok) throw new Error(`Server error: ${res.status}`);
    const data = await res.json();
    renderResults(data);
  } catch (err) {
    showError('Could not connect to the server. Make sure it is running on port 5000.');
    console.error(err);
  }
});

function renderResults(data) {
  const div = document.getElementById('result');
  if (!data || data.length === 0) {
    div.innerHTML = `
      <div class="result-empty">
        <p>&#128533; No colleges found matching your criteria.</p>
        <p>Try lowering your percentile threshold or removing city/branch filters.</p>
      </div>`;
    return;
  }

  div.innerHTML = `
    <div class="result-header">
      <h3>&#127891; ${data.length} College${data.length > 1 ? 's' : ''} Found</h3>
    </div>
    <div class="result-table-wrap">
      <table class="result-table">
        <thead>
          <tr>
            <th>#</th>
            <th>College Name</th>
            <th>Branch</th>
            <th>City</th>
            <th>Cutoff Rank</th>
            <th>Cutoff Percentile</th>
          </tr>
        </thead>
        <tbody>
          ${data.map((row, i) => parseAndRenderRow(row, i + 1)).join('')}
        </tbody>
      </table>
    </div>`;
}

function parseAndRenderRow(raw, idx) {
  // Format: "College Name (Branch) - City, Cutoff Rank: X, CATEGORY Cutoff Percentile: Y"
  try {
    const nameMatch    = raw.match(/^(.+?)\s*\((.+?)\)\s*-\s*(.+?),\s*Cutoff Rank:\s*(.+?),\s*.+?Cutoff Percentile:\s*(.+)$/);
    if (nameMatch) {
      const [, college, branch, city, rank, percentile] = nameMatch;
      return `<tr>
        <td>${idx}</td>
        <td><strong>${esc(college.trim())}</strong></td>
        <td>${esc(branch.trim())}</td>
        <td>&#128205; ${esc(city.trim())}</td>
        <td>${esc(rank.trim())}</td>
        <td><span class="cutoff-badge">${esc(percentile.trim())}</span></td>
      </tr>`;
    }
  } catch (_) {}
  return `<tr><td>${idx}</td><td colspan="5">${esc(raw)}</td></tr>`;
}

function showLoading() {
  document.getElementById('result').innerHTML = `
    <div class="result-loading">
      <div class="spinner-ring"></div>
      <p>Finding colleges for you...</p>
    </div>`;
}

function showError(msg) {
  document.getElementById('result').innerHTML = `
    <div class="result-empty">
      <p>&#9888; ${msg}</p>
    </div>`;
}

function esc(s) {
  return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

/* bits.js — BITSAT College Predictor */
const API = 'http://127.0.0.1:5000/api/predict/bitsat';

document.getElementById('prediction-form').addEventListener('submit', async function (e) {
  e.preventDefault();

  const score  = parseInt(document.getElementById('score').value);
  const campus = document.getElementById('campus').value;

  if (!score || score < 0 || score > 390) {
    showError('Please enter a valid BITSAT score (0–390).');
    return;
  }

  showLoading();

  try {
    const res = await fetch(API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ score, campus })
    });

    if (!res.ok) throw new Error(`Server error: ${res.status}`);
    const data = await res.json();
    renderResults(data, score);
  } catch (err) {
    showError('Could not connect to the server. Make sure it is running on port 5000.');
    console.error(err);
  }
});

function renderResults(data, score) {
  const div = document.getElementById('result');
  if (!data || data.length === 0) {
    div.innerHTML = `
      <div class="result-empty">
        <p>&#128533; No programs found for score ${score}.</p>
        <p>Try a higher score or select "All Campuses".</p>
      </div>`;
    return;
  }

  div.innerHTML = `
    <div class="result-header">
      <h3>&#127891; ${data.length} Program${data.length > 1 ? 's' : ''} Found for Score ${score}</h3>
    </div>
    <div class="result-table-wrap">
      <table class="result-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Campus</th>
            <th>Program</th>
            <th>Cutoff Score</th>
            <th>Max Marks</th>
          </tr>
        </thead>
        <tbody>
          ${data.map((r, i) => `
            <tr>
              <td>${i + 1}</td>
              <td><strong>${esc(r.Campus)}</strong></td>
              <td>${esc(r.Program)}</td>
              <td><span class="cutoff-badge">${r['Cutoff Score']}</span></td>
              <td>${r['Maximum Marks'] || 390}</td>
            </tr>`).join('')}
        </tbody>
      </table>
    </div>`;
}

function showLoading() {
  document.getElementById('result').innerHTML = `
    <div class="result-loading">
      <div class="spinner-ring"></div>
      <p>Finding programs for you...</p>
    </div>`;
}

function showError(msg) {
  document.getElementById('result').innerHTML = `
    <div class="result-empty"><p>&#9888; ${msg}</p></div>`;
}

function esc(s) {
  return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

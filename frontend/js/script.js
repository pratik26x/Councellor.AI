// Fetch college data from JSON file
async function fetchCollegeData() {
    const response = await fetch('colleges.json'); // Ensure this path is correct
    const data = await response.json();
    return data;
}
// Fetch college data from JSON file
async function fetchCollegeData() {
    const response = await fetch('colleges.json'); // Make sure this path is correct
    const data = await response.json();
    return data;
}

function predictColleges(collegeData) {
    const rankInput = parseFloat(document.getElementById('rank').value);
    const percentileInput = parseFloat(document.getElementById('percentile').value);
    const categoryInput = document.getElementById('category').value;

    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = ''; // Clear previous results

    // Filter colleges based on user input
    const filteredColleges = collegeData.filter(college => {
        const cutoff = parseFloat(college[categoryInput]);
        return !isNaN(cutoff) && (cutoff <= percentileInput || cutoff <= rankInput);
    });

    if (filteredColleges.length > 0) {
        // Display matching colleges
        const resultList = document.createElement('ul');
        filteredColleges.forEach(college => {
            const listItem = document.createElement('li');
            listItem.textContent = `${college["College Name"]} (${college["Branch"]}) - Cutoff: ${college[categoryInput]}`;
            resultList.appendChild(listItem);
        });
        resultDiv.appendChild(resultList);
    } else {
        resultDiv.textContent = 'No colleges found matching your criteria.';
    }
}

// Event listener for the prediction button
document.getElementById('predict-button').addEventListener('click', async () => {
    const collegeData = await fetchCollegeData();
    predictColleges(collegeData);
});

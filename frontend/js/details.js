document.getElementById('student-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the default form submission

    // Collect form data
    const formData = new FormData(this);
    const formObject = {};
    formData.forEach((value, key) => {
        formObject[key] = value;
    });

    // Send data to Flask backend using fetch (AJAX)
    fetch('/submit', {
        method: 'POST',
        body: new URLSearchParams(formObject)
    })
    .then(response => {
        if (response.ok) {
            alert("Form submitted successfully!");
            window.location.href = '/';  // Redirect after successful form submission
        } else {
            alert("An error occurred while submitting the form.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Error while submitting the form.");
    });
});

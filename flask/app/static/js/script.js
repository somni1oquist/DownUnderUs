// When the page is loaded
$(window).on('load', () => {
  // Initialise all tooltips
  const $tooltips = $('[data-bs-toggle="tooltip"]')
  const tooltipList = [...$tooltips].map(tooltip => new bootstrap.Tooltip(tooltip))
});
/**
 * Handles sign-in by validating inputs and 
 * performing an AJAX request for server authentication.
 */
document.addEventListener('DOMContentLoaded', function() {
    // Click event for sign-in button
    document.getElementById('signInButton').addEventListener('click', function(e) {
        e.preventDefault(); 

        // Retrieves user input
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const errorMessageDiv = document.getElementById('error-message');

        errorMessageDiv.style.display = 'none';
        
        // Check if either field is empty
        if (!username || !password) {
            errorMessageDiv.innerText = 'Please enter username and password.';
            errorMessageDiv.style.display = 'block';
        } else {
            // AJAX request for sign-in
            fetch('/auth/signin', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: username, password: password}),
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    throw new Error(data.message);
                }
                window.location.href = data.redirect;
            })
            .catch(error => {
                // Handles fetch errors
                console.error('Error:', error);
                errorMessageDiv.innerText = error.message;
                errorMessageDiv.style.display = 'block';
            });
        }
    });
});

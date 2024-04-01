/**
 * Validates the sign-in form input fields.
 * Ensures both email and password are filled in before submitting the form.
 * @return {boolean} Returns true if both fields are filled, false otherwise.
 */

function validateForm() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  if (username === '' || password === '') {
    alert('Please fill in all fields.');
    return false; 
  }
  return true; 
}

$('#test').on('click', (e) => {
  if (!validateForm())
    e.preventDefault();
  else {
    // send ajax post here
  }
})

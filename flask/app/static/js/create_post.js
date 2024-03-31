// for create post feature
// This script is used to generate the drawdown list of topic
document.addEventListener('DOMContentLoaded', function() {
    //get topic list
    fetch('../../static/files/topic.txt')
        .then(response => response.text())
        .then(text => {
            const lines = text.split('\n');
            const menu = document.getElementById('topic-list');
            lines.forEach(line => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.classList.add('dropdown-item');
                a.textContent = line;
                // add event listerner to set the selected topic
                a.addEventListener('click', function(event) {
                    // prevent default action
                    event.preventDefault();
                    document.getElementById('topic').value = line;
                }); 
                li.appendChild(a);
                menu.appendChild(li);  
            });
        })
        .catch(error => console.error('Error fetching topic list', error));

    //get user name
    fetch('/post/get_user_name')
        .then(response => response.json())
        .then(data => {
            document.getElementById('author').textContent  = data.username;
        })
        .catch(error => console.error('Error fetching user name', error));
});


// This script is used to handle the form submission for creating a new post
document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('exampleModal').querySelector('form');
    form.onsubmit = function(event) {
        //prevent form submission
        event.preventDefault();

        // ajax post request
        var formData = new FormData(form);
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/post/create_post', true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        // handle response
        xhr.onload = function() {
            var response = JSON.parse(xhr.responseText);

            if (xhr.status === 200) {
                

                if (response.status ==='success') {
                    // close modal
                    alert(response.message);
                    document.querySelector('.btn-secondary[data-bs-dismiss="modal"]').click();
                    // clear form
                    form.reset();
                    // clear form errors
                    clearFormErrors();
                } 
            } else if (xhr.status === 400){
                if (response.errors) {
                    displayFormErrors(response.errors);
                } else {
                    alert('Validation failed but no errors provided');
                }
            } else{
                alert('Request failed');
            }

        };
        



        // handle request failure
        xhr.onerror = function() {
            alert('Request failed');
        };
        // send request
        xhr.send(formData);
    };

    // display form errors function
    function displayFormErrors(errors) {
        var errorDivs = document.querySelectorAll('.invalid-feedback');
        errorDivs.forEach(function(errorDiv) {
            errorDiv.style.display = 'none';
            errorDiv.innerHTML = '';
            });

        for (var key in errors) {
            if (errors.hasOwnProperty(key)) {
                var input = form.querySelector('input[name="' + key + '"], textarea[name="' + key + '"]');
                if (input) {
                    var errorDiv = input.nextElementSibling;
                    if (errorDiv && errorDiv.classList.contains('invalid-feedback')) {
                        errorDiv.style.display = 'block';
                        errorDiv.innerHTML = errors[key].join(', ');
                    } else {
                        console.error('No sibling with class "invalid-feedback" found for input', input);
                    }
                } else {
                    console.error('No input element found with name', key);
                }
            }

        }
    };
    
    function clearFormErrors() {
        var errorDivs = document.querySelectorAll('.invalid-feedback');
        errorDivs.forEach(function(errorDiv) {
            errorDiv.style.display = 'none'; 
            errorDiv.innerHTML = ''; 
        });
    }

});
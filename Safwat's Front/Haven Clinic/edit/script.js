document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded event fired');
    enableFormElements();
    document.getElementById('saveBtn').addEventListener('click', function() {
        updateProfile();
    });
    document.getElementById('phone').addEventListener('input', function() {
        validateInput(this, /^01\d{9}$/, 'Phone number must start with 01 and be followed by 9 digits');
    });
    document.getElementById('emergency_contact').addEventListener('input', function() {
        validateInput(this, /^01\d{9}$/, 'Emergency contact must start with 01 and be followed by 9 digits');
    });
    document.getElementById('profile_picture').addEventListener('change', function() {
        displayProfilePicture(this);
    });
});

function enableFormElements() {
    var form = document.getElementById('profileForm');
    var inputs = form.getElementsByTagName('input');
    var selects = form.getElementsByTagName('select');
    var profilePictureInput = document.getElementById('profile_picture');

    for (var i = 0; i < inputs.length; i++) {
        inputs[i].removeAttribute('disabled');
    }

    for (var i = 0; i < selects.length; i++) {
        selects[i].removeAttribute('disabled');
    }

    profilePictureInput.removeAttribute('disabled');
}

function updateProfile() {
    if (validateInputs()) {
        saveProfile();
    } else {
        alert('Please correct the errors in the form.');
    }
}

function validateInput(input, pattern, errorMessage) {
    var isValid = pattern.test(input.value);

    if (!isValid) {
        input.setCustomValidity(errorMessage);
        input.classList.add('error');
    } else {
        input.setCustomValidity('');
        input.classList.remove('error');
    }
}

function validateInputs() {
    var form = document.getElementById('profileForm');
    return form.checkValidity();
}

function saveProfile() {
    // Implement your logic to save the profile here
    console.log('Profile updated successfully!');
}

function displayProfilePicture(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            document.getElementById('profile_picture_preview').src = e.target.result;
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function validateEmail(input) {
    var email = input.value;
    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(email)) {
        input.setCustomValidity('Invalid email format');
        input.classList.add('error');
    } else {
        // Clear the prev message
        input.setCustomValidity('');
        input.classList.remove('error');
    }
}

document.getElementById('email').addEventListener('input', function() {
    validateEmail(this);
});

// Show error messages when two password input do not match
var inputPassword = $("#password").get(0);
var inputConfirmPassword = $("#confirm").get(0);
var btnSubmit = $("#submit").get(0);

function validatePassword() {
  if (inputPassword.value != inputConfirmPassword.value) {
    inputConfirmPassword.setCustomValidity("Passwords do not match!");
  } else {
    inputConfirmPassword.setCustomValidity("");
  }
}

inputConfirmPassword.onchange = validatePassword;
btnSubmit.onclick = validatePassword;

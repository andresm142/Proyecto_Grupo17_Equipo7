const body = document.body;
const form = document.getElementById("login-form");

body.classList.add("usuario");

function onSubmitForm(event) {
    alert("datos " + globalVariable.userType());
    event.preventDefault();
}

form.addEventListener('submit', onSubmitForm);
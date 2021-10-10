// DESPLIEGE DE LA OPCION DEL TIPO DE USUARIO
const selectedUsuario = document.querySelector(".selected-usuario");
const optionsContainerUsuario = document.querySelector(".options-container-usuario");
const optionsListUsuario = document.querySelectorAll(".option-user");

selectedUsuario.addEventListener("click", () => {
    optionsContainerUsuario.classList.toggle("active");
    console.log("funciona");
});

optionsListUsuario.forEach(o => {
    o.addEventListener("click", () => {
        selectedUsuario.innerHTML = o.querySelector("label").innerHTML;
        optionsContainerUsuario.classList.remove("active");
    });
});

// DESPLIEGE DE LA OPCION DEL TIPO DE USUARIO
const selectedUsuario = document.querySelector(".selected-usuario");
const optionsContainerUsuario = document.querySelector(".options-container-usuario");
const optionsListUsuario = document.querySelectorAll(".option-user");


selectedUsuario.addEventListener("click", () => {
    if(sessionStorage.getItem('userType')=="superAdmin"){
        optionsContainerUsuario.classList.toggle("active");
    }

});

optionsListUsuario.forEach(o => {
    o.addEventListener("click", () => {
        selectedUsuario.innerHTML = o.querySelector("label").innerHTML;
        optionsContainerUsuario.classList.remove("active");
        var nombre = document.querySelector(".selected-usuario").textContent;
        document.getElementById("inputSelected").value=nombre;
        
    });
});

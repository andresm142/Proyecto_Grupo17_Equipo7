// DESPLIEGE DE LA OPCION DE PROVEEDOR O PRODUCTO EN EL BUSCADOR
const selected = document.querySelector(".selected");
const optionsContainer = document.querySelector(".options-container");
const optionsList = document.querySelectorAll(".option");

selected.addEventListener("click", () => {
  optionsContainer.classList.toggle("active");
});

optionsList.forEach(o => {
    o.addEventListener("click", () => {
      selected.innerHTML = o.querySelector("label").innerHTML;
      optionsContainer.classList.remove("active");
    });
});


// DESPLIEGE DE LA OPCION DE TIPO DE USUARIO O PROVEEDOR
const selectedUser = document.querySelector(".selected-user");
const optionsContainerUser = document.querySelector(".options-container-user");
const optionsListUser = document.querySelectorAll(".option-user");

selectedUser.addEventListener("click", () => {
  optionsContainerUser.classList.toggle("active");
});

optionsListUser.forEach(o => {
    o.addEventListener("click", () => {
      selectedUser.innerHTML = o.querySelector("label").innerHTML;
      optionsContainerUser.classList.remove("active");
    });
});


// MOSTRAR / OCULTAR MENU DE NAVEGACIÓN
function mostrar() {
    document.getElementById("sidebar").style.width = "250px";
    document.getElementById("abrir-menu").style.marginLeft = "250px";
    document.getElementById("contenido").style.marginLeft = "250px";
    document.getElementById("abrir").style.display = "none";
    document.getElementById("cerrar").style.display = "inline";
}

function ocultar() {
    document.getElementById("sidebar").style.width = "0";
    document.getElementById("abrir-menu").style.marginLeft = "0";
    document.getElementById("contenido").style.marginLeft = "0px";
    document.getElementById("abrir").style.display = "inline";
    document.getElementById("cerrar").style.display = "none";

}
function cargar(event){
    $("#contenido").load(event);    
}
function home(){
    location.reload();
}


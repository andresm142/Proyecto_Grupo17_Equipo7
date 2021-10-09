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

function guardar(){                     //Temporal, solo para navegabilidad
    alert("Guardado")
}
function eliminar(){
    alert("Eliminado")
}
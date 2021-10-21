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
        var nombre = document.querySelector(".selected").textContent;
        document.getElementById("inputSelectedSearch").value=nombre;
    });
});

// CAMBIA EL COLOR SEGUN TIPO DE USUARIO

// const body = document.body;
document.body.classList.add(sessionStorage.getItem('userType'));
document.getElementById("id").value=sessionStorage.getItem('id')

// MOSTRAR / OCULTAR OPCIONES SEGUN TIPO DE USUARIO

if (sessionStorage.getItem('userType') === "usuario") {
    document.getElementById("usuarios").style.display = "none";
} else {
    document.getElementById("usuarios").style.display = "";
}
if (sessionStorage.getItem('userType') === "admin") {
    document.getElementById("listas").style.display = "none";
}

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
function cargar(event) {
    $("#contenido").load(event);
}
function home() {
    location.reload();
}

function guardar() {                     //Temporal, solo para navegabilidad
    alert("Guardado")
}
function eliminar() {
    alert("Eliminado")
}
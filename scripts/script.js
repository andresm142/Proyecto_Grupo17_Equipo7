function mostrar() {
    document.getElementById("sidebar").style.width = "200px";
    document.getElementById("abrir-menu").style.marginLeft = "200px";
    document.getElementById("contenido").style.marginLeft = "200px";
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
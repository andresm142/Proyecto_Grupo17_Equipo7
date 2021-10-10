
// DESPLIEGE DE LA OPCION DEL PROVEDOR
const selectedProveedor = document.querySelector(".selected-proveedor");
const optionsContainerProveedor = document.querySelector(".options-container-proveedor");
const optionsListProveedor = document.querySelectorAll(".option-proveedor");

selectedProveedor.addEventListener("click", () => {
    optionsContainerProveedor.classList.toggle("active");
});

optionsListProveedor.forEach(o => {
    o.addEventListener("click", () => {
        selectedProveedor.innerHTML = o.querySelector("label").innerHTML;
        optionsContainerProveedor.classList.remove("active");
    });
});
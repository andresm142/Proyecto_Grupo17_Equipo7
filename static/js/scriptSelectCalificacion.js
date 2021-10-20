// DESPLIEGE DE LA OPCION DE LA CALIFICACION
const selectedCalificacion = document.querySelector(".selected-calificacion");
const optionsContainerCalificacion = document.querySelector(".options-container-calificacion");
const optionsListCalificacion = document.querySelectorAll(".option-calificacion");

selectedCalificacion.addEventListener("click", () => {
    optionsContainerCalificacion.classList.toggle("active");
});

optionsListCalificacion.forEach(o => {
    o.addEventListener("click", () => {
        selectedCalificacion.innerHTML = o.querySelector("label").innerHTML;
        optionsContainerCalificacion.classList.remove("active");
        var nombre = document.querySelector(".selected-calificacion").textContent;
        document.getElementById("inputSelectedCalificacion").value=nombre;
    });
});
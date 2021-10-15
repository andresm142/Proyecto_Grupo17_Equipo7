const modal = document.querySelector(".modal"); //selecciona el modal
const btnCloseModal = document.querySelector(".close-modal"); //selecciona el botón para cerrar el modal
const btnOpenModal = document.querySelector(".show-modal"); //Selecciona el botón para mostrar la modal.
const overlay = document.querySelector(".overlay"); //selecciona la superposición

const toggleModal = function () {
    modal.classList.toggle("hidden");
    overlay.classList.toggle("hidden");
};

btnOpenModal.addEventListener("click", toggleModal);

btnCloseModal.addEventListener("click", toggleModal);

overlay.addEventListener("click", toggleModal);
let currentSlide = 0;
const slides = document.querySelectorAll(".slide");
const totalSlides = slides.length;
const prevBtn = document.querySelector(".prev-btn");
const nextBtn = document.querySelector(".next-btn");
let mostrador = document.getElementById("mostrador");
let seleccion = document.getElementById("seleccion");
let imgSeleccionada = document.getElementById("img");
let modeloSeleccionado = document.getElementById("modelo");
let descripSeleccionada = document.getElementById("descripcion");
let precioSeleccionado = document.getElementById("precio");

function cargar(item) {
  quitarBordes();
  mostrador.style.width = "60%";
  seleccion.style.width = "40%";
  seleccion.style.opacity = "1";
  item.style.border = "2px solid green";

  imgSeleccionada.src = item.getElementsByTagName("images")[0].src;

  modeloSeleccionado.innerHTML = item.getElementsByTagName("p")[0].innerHTML;

  descripSeleccionada.innerHTML = "Descripción del modelo ";

  precioSeleccionado.innerHTML = item.getElementsByTagName("span")[0].innerHTML;
}
function cerrar() {
  mostrador.style.width = "100%";
  seleccion.style.width = "0%";
  seleccion.style.opacity = "0";
  quitarBordes();
}
function quitarBordes() {
  var items = document.getElementsByClassName("item");
  for (i = 0; i < items.length; i++) {
    items[i].style.border = "none";
  }
}

function showSlide(n) {
  slides[currentSlide].classList.remove("active");
  currentSlide = (n + totalSlides) % totalSlides;
  slides[currentSlide].classList.add("active");
}

function prevSlide() {
  showSlide(currentSlide - 1);
}

function nextSlide() {
  showSlide(currentSlide + 1);
}

function autoSlide() {
  nextSlide();
}

let autoSlideInterval = setInterval(autoSlide, 5000);

prevBtn.addEventListener("click", () => {
  prevSlide();
  clearInterval(autoSlideInterval);
  autoSlideInterval = setInterval(autoSlide, 5000);
});

nextBtn.addEventListener("click", () => {
  nextSlide();
  clearInterval(autoSlideInterval);
  autoSlideInterval = setInterval(autoSlide, 5000);
});

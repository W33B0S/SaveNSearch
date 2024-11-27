function toggleDropdown() {
  const dropdown = document.getElementById('dropdownMenu');
  dropdown.classList.toggle('show');
}

window.onclick = function(event) {
  // Verifica que el clic no sea en el botón de filtro ni en el menú desplegable
  if (!event.target.matches('#filterButton') && !event.target.closest('.dropdown-menu')) {
      const dropdown = document.getElementById('dropdownMenu');
      if (dropdown.classList.contains('show')) {
          dropdown.classList.remove('show');
      }
  }
};

function filterProducts2(category) {
  const products = document.querySelectorAll('.product-item');
  const dropdown = document.getElementById('dropdownMenu');
  dropdown.classList.remove('show'); // Ocultar el dropdown al seleccionar

  products.forEach(product => {
      const productCategory = product.getAttribute('p-category');
      if (category === 'all' || productCategory === category) {
          product.style.display = 'block'; // Mostrar producto
      } else {
          product.style.display = 'none'; // Ocultar producto
      }
  });
}
function filterProducts() {
  const searchInput = document.querySelector(".container-fluid form input");
  const searchTerm = searchInput.value.toLowerCase();
  const productItems = document.querySelectorAll(".product-item");

  productItems.forEach((item) => {
    const productDescription = item
      .querySelector("p")
      .textContent.toLowerCase();

    if (
      productDescription.includes(searchTerm)
    ) {
      item.style.display = "flex";
    } else {
      item.style.display = "none";
    }
  });
}
2
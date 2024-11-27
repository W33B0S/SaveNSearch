function compareProducts() {
    const product1 = document.getElementById('product1').value;
    const product2 = document.getElementById('product2').value;

    fetch('/catalogos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `product1=${product1}&product2=${product2}`,
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById('comparison-results').innerHTML = data;
    });
}
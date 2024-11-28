import requests
from bs4 import BeautifulSoup
from passlib.hash import pbkdf2_sha256
from modelo.paginas import plazavea, franco

class CatalogosScraper:
    def __init__(self, mysql):
        self.mysql = mysql
        self.plazavea_urls = plazavea
        self.franco_urls = franco

    def scrape_plazavea(self, url, id_c):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []

        for producto in soup.find_all('div', class_="Showcase__content"):
            precio = producto.find('div', class_="Showcase__salePrice").string.strip()
            titulo = producto.find('a', class_="Showcase__name").string.strip()
            img_tag = producto.find('figure', class_="Showcase__photo")
            image_url = img_tag.find("img").get("src")
            producto_url = producto.find('a', class_="Showcase__name").get("href")
            products.append({
                'precio': precio,
                'titulo': titulo,
                'producto_url': producto_url,
                'image_url': image_url
            })
            
            hashed_prod = pbkdf2_sha256.hash(producto_url)

            self.save_to_database(titulo, precio, hashed_prod, 1, id_c)

        return products

    def scrape_franco(self, url, id_c):
        BASE_URL_FRANCO = "https://francosupermercado.com/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        products2 = []

        for producto in soup.find_all('div', class_="border_prods"):
            titulo2 = producto.find('h2', class_="name name2_padd").string.strip()
            precio2 = producto.find('span', class_="productSpecialPrice").string.strip()
            img_tag = producto.find('a', class_="prods_pic_bg")
            image_url2 = BASE_URL_FRANCO + img_tag.find("img").get("src")
            producto_url2 = producto.find("a").get("href")
            products2.append({
                'precio2': precio2,
                'titulo2': titulo2,
                'producto_url2': producto_url2,
                'image_url': image_url2
            })
            
            hashed_prod2 = pbkdf2_sha256.hash(producto_url2)

            self.save_to_database(titulo2, precio2, hashed_prod2, 2, id_c)

        return products

    def save_to_database(self, titulo, precio, hashed_prod, id_s, id_c):
        cursor = self.mysql.connection.cursor()
        cursor.execute('SELECT * FROM productos WHERE descripcion = %s', (titulo,))
        result = cursor.fetchone()
        
        if result is None:
            cursor.execute('INSERT INTO productos (id_c, id_url, id_s, descripcion, precio) VALUES (%s, %s, %s, %s, %s)', (id_c, hashed_prod, id_s, titulo, precio))
        else:
            id_p = result[0]
            cursor.execute('UPDATE productos SET descripcion = %s, precio = %s WHERE id_p = %s', (titulo, precio, id_p))
        
        self.mysql.connection.commit()
        cursor.close()

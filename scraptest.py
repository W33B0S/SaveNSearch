from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.metro.pe/abarrotes/arroz")
METRO_URL_BASE = "https://metro.pe"
products3 = []

namep3 = driver.find_elements(By.CLASS_NAME, 'vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-brandName.t-body')
#pricep3 = driver.find_elements(By.CLASS_NAME, 'copy10.primary.medium.jsx-3451706699.normal.line-height-22')
#urlp3 = driver.find_elements(By.CSS_SELECTOR, 'a[class="vtex-product-summary-2-x-clearLink.h-100.flex.flex-column"]')
#imgp3 = driver.find_elements(By.CSS_SELECTOR, 'img.jsx-1996933093')

for producto in zip(namep3):
    name_p,=producto
    titulo4 = name_p.text
    print(f"URL: {titulo4}")

driver.quit()

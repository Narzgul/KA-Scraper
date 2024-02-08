from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import sqlite3

options = Options()
options.add_argument('-headless')

driver = webdriver.Firefox(options=options)
driver.install_addon("uBlock0_1.55.0.firefox.signed.xpi")
driver.get("https://www.kleinanzeigen.de/s-51647/anzeige:angebote/preis:200:450/rx-6700-xt/k0l1885r100")
ad_list = driver.find_elements(by=By.XPATH, value="/html/body/div[1]/div[2]/div/div[4]/div[2]/div[4]/div[1]/ul/li")

connection = sqlite3.connect("scraper_objects_data")
cursor = connection.cursor()
for element in ad_list:
    print("----------------")
    try:

        id = element.find_element(by=By.CLASS_NAME, value="aditem").get_attribute(name="data-adid")
        price_full = element.find_element(by=By.CLASS_NAME, value="aditem-main--middle--price-shipping--price").text
        price = price_full.split()[0]
        print("Price: " + price)
        if price_full[-2:] == "VB":
            print("Ist VB!")

        title = element.find_element(by=By.CLASS_NAME, value="ellipsis").text
        print(
            "Description: " + element.find_element(by=By.CLASS_NAME, value="aditem-main--middle--description").text)
        location = element.find_element(by=By.CLASS_NAME, value="aditem-main--top--left").text
        try:
            element.find_element(by=By.CLASS_NAME, value="aditem-main--middle--price-shipping--shipping")
            shipping = True
        except NoSuchElementException:
            shipping = False
        print("Shipping: " + str(shipping))

        cursor.execute("""INSERT INTO products VALUES (id, title, price, null, location, product_shipping=shipping, null)""")

    except NoSuchElementException:
        print("Abtrenner")  # Element is just a gray seperator

driver.quit()

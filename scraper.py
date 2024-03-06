from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import sqlite3


def do_nothing():
    return


options = Options()
options.add_argument('-headless')

driver = webdriver.Firefox(options=options)
driver.install_addon("uBlock0_1.55.0.firefox.signed.xpi")

with open("products.txt") as products_file:
    for full_product in products_file:
        url = full_product.split(sep=',')[0]
        product = full_product.split(sep=',')[1].strip()
        driver.get(url)
        ad_list = driver.find_elements(by=By.XPATH, value="/html/body/div[1]/div[2]/div/div[4]/div[2]/div[4]/div[1]/ul/li")

        connection = sqlite3.connect("scraper_objects_data")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        new_ads = 0
        old_ads = 0
        for element in ad_list:
            # print("----------------")
            try:
                product_id = element.find_element(by=By.CLASS_NAME, value="aditem").get_attribute(name="data-adid")

                if cursor.execute("SELECT * FROM products WHERE product_id=?", (product_id,)).fetchall():
                    # print("Already scraped")
                    old_ads += 1
                    continue

                price_full = element.find_element(by=By.CLASS_NAME, value="aditem-main--middle--price-shipping--price").text
                if price_full != "" and price_full != "VB":
                    price = price_full.split()[0]
                    price = price.replace(".", "")
                    # print("Price: " + str(price))
                    vb = False
                    if price_full[-2:] == "VB":
                        # print("Ist VB!")
                        vb = True
                else:
                    if price_full == "VB":
                        vb = True
                    else:
                        vb = False
                    price = -1

                title = element.find_element(by=By.CLASS_NAME, value="ellipsis").text
                # print("Title: " + str(title))
                # print(
                #     "Description: " + element.find_element(by=By.CLASS_NAME, value="aditem-main--middle--description").text)
                location = element.find_element(by=By.CLASS_NAME, value="aditem-main--top--left").text
                try:
                    element.find_element(by=By.CLASS_NAME, value="aditem-main--middle--price-shipping--shipping")
                    shipping = True
                except NoSuchElementException:
                    shipping = False
                # print("Shipping: " + str(shipping))

                cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (product_id, title, price, vb, location, shipping, product))
                connection.commit()
                new_ads += 1

            except NoSuchElementException:
                do_nothing()  # Workaround
                # print("Abtrenner")  # Element is just a gray seperator
        print("Found " + str(new_ads) + " new ads and " + str(old_ads) + " old ads for " + product)

driver.quit()


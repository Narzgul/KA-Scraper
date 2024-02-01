from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument('-headless')

driver = webdriver.Firefox(options=options)
driver.install_addon("uBlock0_1.55.0.firefox.signed.xpi")
driver.get("https://www.kleinanzeigen.de/s-51647/anzeige:angebote/preis:200:450/rx-6700-xt/k0l1885r100")
ad_list = driver.find_elements(by=By.XPATH, value="/html/body/div[1]/div[2]/div/div[4]/div[2]/div[4]/div[1]/ul/li")
for element in ad_list:
    print("----------------")
    print(element.text)
    try:
        print(
            "Price: " + element.find_element(by=By.CLASS_NAME, value="aditem-main--middle--price-shipping--price").text)
        print(
            "Title: " + element.find_element(by=By.CLASS_NAME, value="ellipsis").text)
        print(
            "Description: " + element.find_element(by=By.CLASS_NAME, value="aditem-main--middle--description").text)
    except NoSuchElementException:
        print("Abtrenner")  # Element is just a gray seperator

driver.quit()

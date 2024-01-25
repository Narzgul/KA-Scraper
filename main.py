from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.install_addon("uBlock0_1.55.0.firefox.signed.xpi")
driver.get("https://www.kleinanzeigen.de/s-51647/preis:200:300/rx-6700-xt/k0l1885r100")
print(driver.find_element(by=By.XPATH, value="//*[@id=\"srchrslt-adtable\"]").text.strip())

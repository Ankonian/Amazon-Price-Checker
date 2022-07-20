from multiprocessing.connection import wait
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import selenium
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.amazon.com/")

time.sleep(3)
login_link = driver.find_element_by_id("nav-link-accountList")
login_link.click()

email = "sixreincarnation@gmail.com"
pw = ":72fZb6kaJDP^67"

time.sleep(3)
email_login = driver.find_element_by_id("ap_email")
email_login.send_keys(email)
email_login.send_keys(Keys.RETURN)

time.sleep(3)
pw_input = driver.find_element_by_id("ap_password")
pw_input.send_keys(pw)
pw_input.send_keys(Keys.RETURN)

item_search = driver.find_element_by_id("twotabsearchtextbox")
item_search.send_keys("iphone 13 case")
item_search.send_keys(Keys.RETURN)

all_items = driver.find_element_by_id("")


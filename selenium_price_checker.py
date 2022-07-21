from multiprocessing.connection import wait
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import selenium
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

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

productLinks = []
filteredLink = []
rawLinks = driver.find_elements_by_tag_name('a')
for rawLink in rawLinks:
    productLinks.append(rawLink.get_attribute('href'))

sub = "/gp/slredirect/picassoRedirect.html/"
for s in productLinks:
    if(s != None):
        if(sub in s):
            if(s not in filteredLink):
                filteredLink.append(s)
print(len(filteredLink))

first_item = filteredLink[0]
driver.get(first_item)

driver.find_element_by_id("add-to-cart-button").click()
time.sleep(3)
driver.find_element_by_id("sc-buy-box-ptc-button").click()
#time.sleep(3)
#driver.find_element_by_link_text("Deliver to this address").click()
time.sleep(3)
driver.find_element_by_name('ppw-widgetEvent:SetPaymentPlanSelectContinueEvent').click()
time.sleep(3)
price = driver.find_element_by_xpath('//*[@id="subtotals-marketplace-table"]/tbody/tr[5]/td[2]')
print(price.text)

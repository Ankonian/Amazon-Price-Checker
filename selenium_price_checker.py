from multiprocessing.connection import wait
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import openpyxl

#opening and reading the list of items
items = []
path = "C:/Users/LiLang/Documents/GitHub Repos/Amazon Price Checker/Amazon-Purchase-Automater/item_prices.xlsx"
item_price = openpyxl.load_workbook(path)
sheet1 = item_price.active
for x in range(2, 7):
    cell_obj = sheet1.cell(row=x, column=1)
    items.append(cell_obj.value)

#login infos
email = "sixreincarnation@gmail.com"
pw = ":72fZb6kaJDP^67"

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.amazon.com/")

#login
login_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "nav-link-accountList"))
    )
login_link.click()
email_login = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ap_email"))
    )
email_login.send_keys(email)
email_login.send_keys(Keys.RETURN)
pw_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ap_password"))
    )
pw_input.send_keys(pw)
pw_input.send_keys(Keys.RETURN)

#loop through each item
for search_item in items:
#search for the item
    new_price_cell = 2
    driver.get("https://www.amazon.com/")
    shopping_cart = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nav-cart-count"))
        )
    shopping_cart.click()
    try:
        delete_item = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="sc-item-Cdff2b476-f3ff-4541-9d72-e76fca8480f0"]/div[4]/div/div[1]/div/div/div[2]/div[1]/span[2]/span/input'))
            )
        delete_item.click()
    except:
        pass
    item_search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
    #item_search = driver.find_element_by_id("twotabsearchtextbox")
    item_search.send_keys(search_item)
    item_search.send_keys(Keys.RETURN)

    #grab all clickable links
    productLinks = []
    filteredLink = []
    rawLinks = driver.find_elements_by_tag_name('a')
    for rawLink in rawLinks:
        productLinks.append(rawLink.get_attribute('href'))

    #filter out links that isn't product listing
    sub = "/gp/slredirect/picassoRedirect.html/"
    for s in productLinks:
        if(s != None):
            if(sub in s):
                if(s not in filteredLink):
                    filteredLink.append(s)
    print(len(filteredLink))
    #grab the first item of the list
    first_item = filteredLink[0]
    driver.get(first_item)

    #click on add to cart
    add_to_cart = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "add-to-cart-button"))
        )
    add_to_cart.click()

    #click on proceed to checkout
    checkout_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sc-buy-box-ptc-button"))
        )
    checkout_button.click()

    #click on continue for payment
    #continue_button = WebDriverWait(driver, 10).until(
        #    EC.presence_of_element_located((By.NAME, 'ppw-widgetEvent:SetPaymentPlanSelectContinueEvent'))
        #)
    #continue_button.click()

    #grab to total price before tax
    price = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="subtotals-marketplace-table"]/tbody/tr[5]/td[2]'))
        )
    write_cell = sheet1.cell(row=new_price_cell, column=2)
    write_cell.value = price.text
    item_price.save("C:/Users/LiLang/Documents/GitHub Repos/Amazon Price Checker/Amazon-Purchase-Automater/item_prices.xlsx")

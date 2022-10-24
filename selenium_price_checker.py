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
import time
from tkinter import *



######################################
#             Main   GUI             #
# ####################################

keywords = []
productName = []
productPrice = []
productRating = []
numofProductRating = []
productLink = []
root = Tk()
root.geometry("750x250")

def saveKeywords():
    newKeyword = entryBox.get()
    keywords.append(newKeyword)
    entryBox.delete(0, END)

def searchKeywords():
    keywordsLabel = Label(root, text=keywords)
    keywordsLabel.pack()
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.amazon.com/")
    for keyword in keywords:
        amazonTextBox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
            )
        amazonTextBox.send_keys(keyword)
        amazonTextBox.send_keys(Keys.ENTER)
        items = WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]'))
            )
        for item in items:
            #grabbing item name
            try:
                itemName = item.find_element(By.XPATH, './/span[@class="a-size-medium a-color-base a-text-normal"]')
                productName.append(itemName.text)
            except:
                itemName = item.find_element(By.XPATH, './/span[@class="a-size-base-plus a-color-base a-text-normal"]')
                productName.append(itemName.text)

            #grabbing item price
            fullPrice = 0
            wholePrice = item.find_element(By.CLASS_NAME, 'a-price-whole')
            fractionPrice = item.find_element(By.CLASS_NAME, 'a-price-fraction')
            if(wholePrice != [] and fractionPrice != []):
                fullPrice = wholePrice.text + "." + fractionPrice.text
            else:
                fullPrice = 0
            productPrice.append(fullPrice)

            #grabbing item rating and number of ratings
            starRating = 0
            numofRating = 0
            ratingInfos = fractionPrice = item.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')
            if(ratingInfos != []):
                starRating = ratingInfos[0].get_attribute('aria-label')
                numOfRating = ratingInfos[1].get_attribute('aria-label')
            else:
                starRating = 0
                numofRating = 0
            productRating = starRating
            numofProductRating = numofRating

            #grabbing product link
            link = item.find_element(By.XPATH, './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]').get_attribute("href")
            productLink.append(link)
    print(productName)
    print(productPrice)
    print(productRating)
    print(numofProductRating)
    print(productLink)

introLabel = Label(root, text="Enter a keyword you wish to search on Amazon:")
introLabel.grid(row=0, column=0)
introLabel.pack()

entryBox = Entry(root, width = 50)
entryBox.pack()

saveKeywordButton = Button(root, text = "Save keyword", command=saveKeywords)
saveKeywordButton.pack()

searchKeywordsButton = Button(root, text = "Search", command=searchKeywords)
searchKeywordsButton.pack()

root.mainloop()


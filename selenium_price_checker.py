from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import tkinter as tk
from tkinter import ttk

# function to perform the search and compile the results
def search_amazon():
    # get the search term from the entry field
    search_term = search_entry.get()

    # set up options for Chrome webdriver
    options = Options()
    options.add_argument("--headless")  # run Chrome in headless mode (without a window)

    # install a new chromedriver if not present
    driver = webdriver.Chrome()

    # navigate to the Amazon home page
    driver.get("https://www.amazon.com/")

    # find the search bar and enter the search term
    search_bar = driver.find_element(By.ID, "twotabsearchtextbox")
    search_bar.send_keys(search_term)
    search_bar.send_keys(Keys.RETURN)

    # wait for the search results to load
    time.sleep(2)

    # find all the product listings on the page
    listings = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")

    # initialize an empty list to hold the search results
    results = []

   # loop through each listing and extract relevant information
    for listing in listings:
        # extract product title
        name = listing.find_element(By.TAG_NAME, 'h2').text.strip()
        title_element = listing.find_element(By.TAG_NAME, 'h2')
        link = title_element.find_element(By.TAG_NAME, 'a').get_attribute('href')

        # extract product price, if available
        try:
            price = listing.find_element(By.XPATH, ".//span[@class='a-price-whole']").text
            price_fraction = listing.find_element(By.XPATH, ".//span[@class='a-price-fraction']").text
            price = f"{price}.{price_fraction}"
        except:
            price = ""

        # extract product rating, if available
        try:
            rating = listing.find_element(By.XPATH, ".//span[contains(@class,'a-icon-alt')]") \
                            .get_attribute('innerHTML').strip()
        except:
            rating = ""
        
        # extract number of ratings, if available
        try:
            num_ratings = listing.find_element(By.XPATH, ".//span[@class='a-size-base']") \
                                .text.split()[0]
        except:
            num_ratings = ""

        # add the extracted information to the results list
        results.append({
            'Product Name': name,
            'Product Link': link,
            'Price': price,
            'Rating': rating,
            'Number of Rating': num_ratings
        })


    # create a pandas DataFrame from the results list
    df = pd.DataFrame(results)

    # save the DataFrame to an Excel file
    filename = f"{search_term}_results.xlsx"
    df.to_excel(filename, index=False)

    # update the status label to indicate where the results were saved
    status_label.config(text=f"Search results saved to {filename}")

    # close the webdriver
    driver.quit()

# create the main window
root = tk.Tk()
root.title("Amazon Search")

# create a label and entry field for the search term
search_label = ttk.Label(root, text="Enter a search term:")
search_label.pack(pady=5)
search_entry = ttk.Entry(root, width=40)
search_entry.pack(pady=5)

# create a button to perform the search
search_button = ttk.Button(root, text="Search", command=search_amazon)
search_button.pack(pady=5)

# create a label to display the status of the search
status_label = ttk.Label(root, text="")
status_label.pack(pady=5)

# start the main event loop
root.mainloop()

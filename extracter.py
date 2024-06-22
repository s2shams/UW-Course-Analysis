from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Start WebDriver
service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get("https://uwflow.com/explore")

# The courses keep loading as you scroll down, so we need to keep scrolling down until we hit the bottom of the page
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(2)

    # Check if height has changed
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break ## if height didn't change, we've hit the bottom of the page
    last_height = new_height

# Access each tab and push the data to the dataframe
course_tabs = driver.find_elements(By.XPATH, '//div[@role="rowgroup"]//div[@role="row"]')
for tab in course_tabs:
    course_code = tab.find_element(By.XPATH,".//div//a").text
    course_name = tab.find_element(By.XPATH,".//div[2]").text
    course_ratings = tab.find_element(By.XPATH,".//div[3]").text
    course_useful = tab.find_element(By.XPATH,".//div[4]").text
    course_easy = tab.find_element(By.XPATH,".//div[5]").text
    course_liked = tab.find_element(By.XPATH,".//div[6]").text
    print(course_code, course_name, course_ratings, course_useful, course_easy, course_liked)
    ## add code to push data to dataframe here, we have to initialize a dataframe first using pandas

driver.quit()

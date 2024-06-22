from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from Helper_functions import *
import pandas as pd
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Start WebDriver
service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get("https://uwflow.com/explore")
wait_for_element(driver, '(//div[@role="rowgroup"]//div[@role="row"])[1]')

# Scroll to bottom of page to load all the courses
# scroll_to_bottom(driver)

# Create an empty dataframe to store the data
df = pd.DataFrame(columns = ['Course_Code', 'Course_Name', 'Number_of_Ratings', 'Useful', 'Easy', 'Liked', 'Course_Reviews'])

# Access each tab and push the data to the dataframe
course_tabs = driver.find_elements(By.XPATH, '//div[@role="rowgroup"]//div[@role="row"]')
for tab in course_tabs:
    # Retrieve relevant information from the summary
    course_code = tab.find_element(By.XPATH,".//div//a").text
    course_name = tab.find_element(By.XPATH,".//div[2]").text
    course_ratings = tab.find_element(By.XPATH,".//div[3]").text
    course_useful = tab.find_element(By.XPATH,".//div[4]").text
    course_easy = tab.find_element(By.XPATH,".//div[5]").text
    course_liked = tab.find_element(By.XPATH,".//div[6]").text

    # Click into the course to obtain the recent comments
    course_link = tab.find_element(By.XPATH,".//div//a").get_attribute('href')
    driver.execute_script(f'window.open("{course_link}", "_blank");')
    driver.switch_to.window(driver.window_handles[1])
    wait_for_element(driver, "//div[@class='sc-pKMan dgjbLL']")

    reviews_raw = driver.find_elements(By.XPATH, "//div[@class='sc-pLwIe kqSAIH']")
    if not reviews_raw:
        reviews = ['No reviews']
    else:
        reviews = [str(review.text) + " REVIEW ENDS HERE" for review in reviews_raw]
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(.5)

    ## add code to push data to dataframe here, we have to initialize a dataframe first using pandas
    print(course_code, course_name, course_ratings, course_useful, course_easy, course_liked, reviews)
    append_data_to_df(df, {'Course_Code':course_code, 'Course_Name':course_name, 'Number_of_Ratings':course_ratings,
                           'Useful':course_useful, 'Easy':course_easy, 'Liked':course_liked, 'Course_Reviews': reviews})

driver.quit()

import os
from selenium import webdriver
import time

MAX_PG_NUM = 200
FLEXBOX_NUM = 2
ITEM_PER_FLEXBOX = 6

script_dir = os.path.dirname(__file__)
chromeDriverPath = script_dir + '/chromedriver'

driver = webdriver.Chrome(chromeDriverPath)


print(driver.title)
for pgNum in range(MAX_PG_NUM):
    driver.get("https://www.kickstarter.com/discover/advanced?sort=newest&page=" + str(pgNum + 1))
    for i in range(FLEXBOX_NUM):
        for j in range(ITEM_PER_FLEXBOX):
            print(driver.find_element_by_xpath(
                '//*[@id="projects_list"]/div[' + str(i + 1) + ']/div[' + str(j + 1) + ']/div/div/div/div[3]/div[1]/div[1]/a/h3').text)
    time.sleep(1)
driver.quit()
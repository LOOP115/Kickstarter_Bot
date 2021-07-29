import os
from selenium import webdriver
import time

MAX_PG_NUM = 10
FLEXBOX_NUM = 2
ITEM_PER_FLEXBOX = 6

script_dir = os.path.dirname(__file__)
CHROME_DRIVER_PATH = script_dir + '/chromedriver'


def kickstarter_bot():
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    newCampaigns = []
    print(driver.title)
    for pgNum in range(MAX_PG_NUM):
        driver.get("https://www.kickstarter.com/discover/advanced?sort=newest&page=" + str(pgNum + 1))
        for i in range(FLEXBOX_NUM):
            for j in range(ITEM_PER_FLEXBOX):
                singleCampaign = [
                    driver.find_element_by_xpath('//*[@id="projects_list"]/div[' + str(i + 1) + ']/div[' + str(
                        j + 1) + ']/div/div/div/div[3]/div[1]/div[1]/a/h3').text,
                    driver.find_element_by_xpath('//*[@id="projects_list"]/div[' + str(i + 1) + ']/div[' + str(
                        j + 1) + ']/div/div/div/div[3]/div[1]/div[1]/a/p').text]
                newCampaigns.append(singleCampaign)
        time.sleep(1)
        driver.delete_all_cookies()
    driver.quit()


def kicktraq_bot():
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    new_campaigns = []
    for pg_num in range(MAX_PG_NUM):
        driver.get('https://kicktraq.com/projects/?sort=new&page=' + str(pg_num + 1))
        for project in driver.find_elements_by_class_name('project-infobox'):
            campaign = [
                project.find_element_by_tag_name("h2").text,
                project.find_element_by_tag_name("div").text]
            new_campaigns.append(campaign)

kicktraq_bot()

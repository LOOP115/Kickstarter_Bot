import os
from selenium import webdriver
import time
import googleSheets

MAX_PG_NUM = 10
FLEXBOX_NUM = 2
ITEM_PER_FLEXBOX = 6

script_dir = os.path.dirname(__file__)
CHROME_DRIVER_PATH = script_dir + '/chromedriver'


def kickstarter_bot(service, prev):
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    breaked = False
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
                if singleCampaign in prev:
                    breaked = True
                    break
                else:
                    newCampaigns.append(singleCampaign)
            if breaked:
                break
        time.sleep(1)
        driver.delete_all_cookies()
        if breaked:
            break
    driver.quit()
    final = [['Name', 'Desc']] + newCampaigns + prev
    googleSheets.upload_to_sheets(final, service)


def kicktraq_bot(service, prev):
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    new_campaigns = []
    breaked = False
    for pg_num in range(MAX_PG_NUM):
        driver.get('https://kicktraq.com/projects/?sort=new&page=' + str(pg_num + 1))
        for project in driver.find_elements_by_class_name('project-infobox'):
            campaign = [
                project.find_element_by_tag_name("h2").text,
                project.find_element_by_tag_name("div").text]
            if campaign in prev:
                breaked = True
                break
            else:
                new_campaigns.append(campaign)
        if breaked:
            break
    driver.quit()
    final = [['Name', 'Desc']] + new_campaigns + prev
    googleSheets.upload_to_sheets(final, service)


sheet_service = googleSheets.auth()
prev = googleSheets.read_current_sheet(sheet_service)[1:]
try:
    kickstarter_bot(sheet_service, prev)
except TypeError as e:
    kicktraq_bot(sheet_service, prev)

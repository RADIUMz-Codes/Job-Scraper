from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs
import os
import time
import json
import pandas as pd

from Utils import getJobTitle, getJobDescription, getSkills



# Creating a webdriver instance
chrome_options = Options()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)
driver.delete_all_cookies()
driver.maximize_window()

# Opening linkedIn's login page
driver.get("https://www.linkedin.com/")

time.sleep(5)
load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# entering username
username = driver.find_element(By.ID, "session_key")
driver.implicitly_wait(3)

# Enter Your Email Address
username.send_keys(USERNAME)

# entering password
pword = driver.find_element(By.ID, "session_password")
driver.implicitly_wait(3)

# Enter Your Password
pword.send_keys(PASSWORD)
driver.implicitly_wait(3)

driver.find_element(By.XPATH, "//button[@type='submit']").click()

time.sleep(5)


# ----------------------- Looper for each company_page ----------------------- #
f = open('example.json')
data = json.load(f)
f.close()

# The DataFrame

jobData = []

for key,value in data.items():
    companyUrl =f"https://www.linkedin.com/jobs/search/?f_C={value}&origin=JOB_SEARCH_PAGE_JOB_FILTER" 
    
    driver.get(companyUrl)
    time.sleep(5)
    page = 1
    # ----------------------------- Extraction Logic ----------------------------- #
    jdIdList = []
    while True:
        print(key, "->", page)
        
        company_page = driver.page_source
        soup = bs(company_page, "html5lib")
        
        internalIdList = []
        
        jobList = soup.find('ul', attrs={'class':'scaffold-layout__list-container'})


        for job in jobList.find_all('li'):
            try:
                currId = job['data-occludable-job-id']
                internalIdList.append(currId)
            except:
                continue
                
        
        jdIdList.extend(internalIdList)
        
        page += 1
        try:
            nextButton = driver.find_element(By.XPATH, "//*[@aria-label='View next page']")
            nextButton.click()
            time.sleep(2)
        except:
            break
    
    print(key, " -> ", jdIdList, " count = ",len(jdIdList))
    
    # ----------------------- Spcraping info from each job ----------------------- #
    for job in jdIdList:
        jobUrl = f"https://www.linkedin.com/jobs/search/?currentJobId={job}"
        
        driver.get(jobUrl)
        time.sleep(2)
        
        jobPageSource = driver.page_source
        jobSoup = bs(jobPageSource, "html5lib")
        
        currJobTitle = getJobTitle(jobSoup)
        currJobDescription = getJobDescription(jobSoup)
        currJobSkills = getSkills(jobSoup)
        
        jobData.append({
            'Company' : key,
            'Job_Title': currJobTitle,
            'Job_Description': currJobDescription,
            'Skills' : currJobSkills,
            'Url' : jobUrl
        })
        
        
        # df = pd.DataFrame(columns=['Company', 'Job_Id', 'Job_Title', 'Job_Description','Skills','Url'])
        

df = pd.DataFrame(jobData)
df.to_csv('output.csv', index=False)

driver.get("https://www.linkedin.com/m/logout/")
time.sleep(3)
driver.quit()

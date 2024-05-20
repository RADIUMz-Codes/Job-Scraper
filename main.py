from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from dotenv import load_dotenv
from credentials import USERNAME, PASSWORD
from bs4 import BeautifulSoup as bs
import os
import time
import json
import pandas as pd

from Utils import getJobTitle, getJobDescription, getSkills, isJobAvailable, getCompanyName

def searchJobFromExistingClients():
# ----------------------- Looper for each company_page ----------------------- #
    f = open('example.json')
    data = json.load(f)
    f.close()

    # The DataFrame


    for key,value in data.items():
        jobData = []
        
        companyUrl =f"https://www.linkedin.com/jobs/search/?f_C={value}&&f_TPR=r604800&origin=JOB_SEARCH_PAGE_JOB_FILTER" 
        
        driver.get(companyUrl)
        time.sleep(5)
        page = 1
        # ----------------------------- Extraction Logic ----------------------------- #
        jdIdList = []
        while True:
            print(key, "->", page)
            page += 1
            company_page = driver.page_source
            soup = bs(company_page, "html5lib")
            
            if isJobAvailable(soup) == True:
                break


            
            internalIdList = []
            
            jobList = soup.find('ul', attrs={'class':'scaffold-layout__list-container'})


            for job in jobList.find_all('li'):
                try:
                    currId = job['data-occludable-job-id']
                    internalIdList.append(currId)
                except:
                    continue
                    
            
            jdIdList.extend(internalIdList)
            
            
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
            
        df = pd.DataFrame(jobData)
        path = f'{os.getcwd()}\\results\\{key}.csv' 
        df.to_csv(path, index=False)
        
def searchJobsUsingKeywords(keywords):
    jobData = []
    
    keywords = keywords.replace(" ", "%20")
    jobsUrl =f"https://www.linkedin.com/jobs/search/?f_TPR=r86400&keywords={keywords}&location=Bengaluru%2C%20Karnataka%2C%20India&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R" 
    
    driver.get(jobsUrl)
    time.sleep(5)
    page = 1
    jdIdList = []

    while True:
        page += 1
        jobsPage= driver.page_source
        soup = bs(jobsPage, "html5lib")
        
        if isJobAvailable(soup) == True:
            break


        
        internalIdList = []
        
        jobList = soup.find('ul', attrs={'class':'scaffold-layout__list-container'})


        for job in jobList.find_all('li'):
            try:
                currId = job['data-occludable-job-id']
                internalIdList.append(currId)
            except:
                continue
                
        
        jdIdList.extend(internalIdList)
        
        
        try:
            nextButton = driver.find_element(By.XPATH, "//*[@aria-label='View next page']")
            nextButton.click()
            time.sleep(2)
        except:
            break

    for job in jdIdList:
            jobUrl = f"https://www.linkedin.com/jobs/search/?currentJobId={job}"
            
            driver.get(jobUrl)
            time.sleep(2)
            
            jobPageSource = driver.page_source
            jobSoup = bs(jobPageSource, "html5lib")
            
            company = getCompanyName(jobSoup)
            currJobTitle = getJobTitle(jobSoup)
            currJobDescription = getJobDescription(jobSoup)
            currJobSkills = getSkills(jobSoup)
            
            jobData.append({
                'Company' : company,
                'Job_Title': currJobTitle,
                'Job_Description': currJobDescription,
                'Skills' : currJobSkills,
                'Url' : jobUrl
            })
            
    df = pd.DataFrame(jobData)
    df.to_csv('output.csv', index=False)



if __name__ == '__main__':
    # Creating a webdriver instance
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)
    driver.delete_all_cookies()
    driver.maximize_window()

    # Opening linkedIn's login page
    driver.get("https://www.linkedin.com/")

    time.sleep(5)
    # load_dotenv()
    # USERNAME = os.getenv("USERNAME")
    # PASSWORD = os.getenv("PASSWORD")
    # print(USERNAME, PASSWORD)
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

    # searchJobsUsingKeywords("SAP")
    searchJobFromExistingClients()

    driver.get("https://www.linkedin.com/m/logout/")
    time.sleep(3)
    driver.quit()

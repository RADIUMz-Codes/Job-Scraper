# Linkedin Job Scraper

This project helps you to scrape the job posting from a list of clients or by using keywords.

## Steps to Use this Bot


##### 1. Fork or Download this Repo.

##### 2. Install the requirements for this project.
&nbsp;&nbsp;&nbsp;Run this Command :

    pip install -r requirements.txt

##### 3. Add Credentials.
&nbsp;&nbsp;&nbsp; Create `credentials.py` in your home directory and add your Username and Password.

    USERNAME='example@gmail.com'
    PASSWORD='Password'


##### 4. Add Company List.
&nbsp;&nbsp;&nbsp; Create `company_code.json` in your home directory add the data in the following format.

    {
        "HSBC" : "1241",
        "Goldman Sachs" : "1382"
    }
&nbsp;&nbsp;&nbsp;Here the `key` is company name and `value` is the company code from LinkedIn URL.

&nbsp;&nbsp;&nbsp;Example: In this url [https://www.linkedin.com/jobs/search/?currentJobId=3953515669&f_C=2329&keywords=schneider%20electric&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true](https://www.linkedin.com/jobs/search/?currentJobId=3953515669&f_C=2329&keywords=schneider%20electric&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true) here the value `f_C` or `company code` is 2329 which will be added to the `company_code.json` file.


##### 5. Run Scraper.
&nbsp;&nbsp;&nbsp;Run this Command :

    python main.py


##### 6. Run Summary Generator.
&nbsp;&nbsp;&nbsp;Run this Command :

    python summaryGenerator.py

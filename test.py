import json
f = open('example.json')

data = json.load(f)
f.close()

for key,value in data.items():
    url =f"https://www.linkedin.com/jobs/search/?f_C={value}&origin=JOB_SEARCH_PAGE_JOB_FILTER" 
    print(key," -> ", url)
    

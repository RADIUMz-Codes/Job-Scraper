import os
import pandas as pd
import json

def generateSummary(file,data):

    results = os.path.join(os.getcwd(), 'results',file)
    df = pd.read_csv(results)
    

    totalJobs = df.shape[0]
    relevantJobCount = 0
    traSkills = []

    prev = 0
    for index, row in df.iterrows():
        inputString = row['Skills']+' , '+row['Job_Title']
        tokens = inputString.split(',')

        for token in tokens:
            token = token.strip()

            for key in data:
                for val in data[key]:
                    if val in token.lower() :
                        print(key)
                        traSkills.append(key)
                        break

        if len(traSkills) > prev:
            relevantJobCount += 1
            prev = len(traSkills)


    res = {
        'Company': file.replace('.csv',''),
        '#Total Openings': totalJobs,
        '#Relevent Openings': relevantJobCount,
        'TRA Skills': ', '.join(list(set(traSkills)))
    }

    print('#Total Jobs:', totalJobs)
    print(file.replace('.csv',''))
    print(list(set(traSkills)))
    print(relevantJobCount)
    print('------------------------------------')

    return res

    
if __name__ == '__main__':
    f = open('skillList.json', 'r')
    data = json.load(f)
    f.close()

    fileList = os.listdir(os.getcwd()+'/results')

    summary = []
    for file in fileList:
        res = generateSummary(file, data)
        summary.append(res)
    
    df = pd.DataFrame(summary)
    df.to_csv('summary.csv', index=False)




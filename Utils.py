def getCleanText(str):
    return " ".join(str.split())


def getJobTitle(soup):
    try:
        jdTitle = soup.find(
            "div", attrs={"class": "t-24 job-details-jobs-unified-top-card__job-title"}
        ).text
        return getCleanText(jdTitle)
    except:
        return " "


def getJobDescription(soup):
    try:
        jdText = soup.find(
            "div",
            attrs={
                "class": "jobs-box__html-content jobs-description-content__text t-14 t-normal jobs-description-content__text--stretch"
            },
        ).text
        return getCleanText(jdText)
    except:
        return " "

def getSkills(soup):
    try:
        skillsSection = soup.find(
            "div",
            attrs={
                "class": "job-details-how-you-match__skills-item-wrapper display-flex flex-row pt4"
            },
        ).text
        
        skills = skillsSection.split('profile', 1)[1]
        return getCleanText(skills)
    except:
        return " "

def isJobAvailable(soup):
    getBanner = soup.find('div', attrs={'class': 'jobs-search-no-results-banner__image'})
    if getBanner is None:
        return True
    else:
        return False

def getCompanyName(soup):
    try:
        divText = soup.find('div', attrs={'class':'job-details-jobs-unified-top-card__primary-description-without-tagline mb2'}).text
        company = divText.split('· Bengaluru', 1)[0]
        return getCleanText(company)
    except:
        return " "
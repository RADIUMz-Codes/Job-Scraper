def getCleanText(str):
    return " ".join(str.split())


def getJobTitle(soup):
    jdTitle = soup.find(
        "div", attrs={"class": "t-24 job-details-jobs-unified-top-card__job-title"}
    ).text
    return getCleanText(jdTitle)


def getJobDescription(soup):
    jdText = soup.find(
        "div",
        attrs={
            "class": "jobs-box__html-content jobs-description-content__text t-14 t-normal jobs-description-content__text--stretch"
        },
    ).text
    return getCleanText(jdText)


def getSkills(soup):
    skillsSection = soup.find(
        "div",
        attrs={
            "class": "job-details-how-you-match__skills-item-wrapper display-flex flex-row pt4"
        },
    ).text
    
    skills = skillsSection.split('profile', 1)[1]
    return getCleanText(skills)



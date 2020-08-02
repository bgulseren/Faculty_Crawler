
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re

import warnings
warnings.filterwarnings(action="once")


# all_urls=["https://schulich.ucalgary.ca/departments/electrical-and-computer-engineering/faculty",
# "https://schulich.ucalgary.ca/departments/chemical-and-petroleum-engineering/faculty",
# "https://schulich.ucalgary.ca/departments/civil-engineering/faculty",
# "https://schulich.ucalgary.ca/departments/mechanical-and-manufacturing-engineering/faculty",
# "https://schulich.ucalgary.ca/geomatics/faculty-members"]


all_urls=['html/ECE.html', 'html/CPE.html', 'html/CE.html', 'html/MME.html', 'html/GE.html']

df_professors = pd.DataFrame(columns = ["firstname", "lastname", "title", "faculty", "email", "homepage"])

# Your solution goes here
for url in all_urls:
    faculty = url
    file = open(url, 'r')
    # html = file.read()

    # html = requests.get(all_urls[0], verify=False).text
    soup = BeautifulSoup(file, 'lxml')

    file.close()

    # all profs are children of this special div, wrapped in a p
    for row in soup.find('div', class_="col-sm-12 two-col").find_all('p'):
        if row.contents == ['\xa0']:
            print('Empty <p> tag found, skipping...')
            continue 

        firstname = lastname = title = email = homepage = np.nan
        for span in row('span'):
            span.unwrap()
        for strong in row('strong'):
            strong.decompose()
        for br in row('br'):
            br.decompose()
        
        profLine = str(row).splitlines()[0]
        profLine = profLine.replace('<p>','')
        profLine = profLine.replace('Dr.','')
        profLine = profLine.replace(u'\xa0', u' ')
        profLine = profLine.strip()
        prof_info_list = profLine.split(', ')

        ### Extracting first name and last name ###
        prof_name_list = prof_info_list[0].split(' ')
        lastname = prof_name_list[-1]
        firstname = prof_name_list[0]

        # Add first names if professor has more than one name.
        if len(prof_name_list) > 2:
            i = 1
            while i < len(prof_name_list) - 1:
                firstname = firstname + ' ' + prof_name_list[i]
                i += 1

        ### Extracting title ###
        title = prof_info_list[1]
        
        ### Extracting homepage ###
        homepage = row.find(href=re.compile("/contacts"))
        if homepage is not None:
            homepage = homepage['href']

        ### Extracting email address ###
        email = row.find(href=re.compile("mailto"))
        if email is not None:
            email = email['href'].replace('mailto:','')

        # add a row
        df_professors = df_professors.append({'firstname': firstname,'lastname': lastname,'title': title,'faculty': faculty,'email': email,'homepage':homepage}, ignore_index=True)


print(df_professors)
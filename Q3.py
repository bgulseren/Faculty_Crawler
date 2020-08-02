
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
        profLine = profLine.replace(u'â€™', u'\'')
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
        homepage = row.find(href=re.compile("/schulich"))
        if homepage is not None:
            homepage = homepage['href']
        else:
            homepage = row.find(href=re.compile("/research"))
            if homepage is not None:
                homepage = homepage['href']

        ### Extracting email address ###
        email = row.find(href=re.compile("mailto"))
        if email is not None:
            email = email['href'].replace('mailto:','')

        # add a row
        df_professors = df_professors.append({'firstname': firstname, 'lastname': lastname, 'title': title, 'faculty': faculty, 'email': email, 'homepage': homepage}, ignore_index=True)


#print(df_professors)

phone_list = []
office_list = []

for homepage in df_professors['homepage']:
    print('Scraping...')
    phone_number = office_number = np.nan

    # html = requests.get('https://schulich.ucalgary.ca/contacts/steve-liang', verify=True).text

    if homepage is None:
        phone_list.append(phone_list)
        office_list.append(office_number)
        print('no homepage for this prof, skipping')
        continue

    html = requests.get(homepage, verify=True).text
    soup = BeautifulSoup(html, 'lxml')
    # all prof contact information are children of this special div,
    contact_info = soup.find('div', class_="col-md-8 contact-section")

    if contact_info is None:
        phone_list.append(phone_list)
        office_list.append(office_number)
        print('no contact info found for this prof, skipping')
        continue

    ### Extracting phone number ###
    phone_tag = contact_info.find(href=re.compile("tel:"))
    if phone_tag is not None:
        phone_number = phone_tag.string
    phone_list.append(phone_list)

    ### Extracting office number ###
    office_tag = contact_info.find(href=re.compile("https://www.ucalgary.ca/map/contactlist/"))
    if office_tag is not None:
        office_number = office_tag.string
    office_list.append(office_number)

    print('Phone_number: ' + str(phone_number) + ' Office_number: ' + str(office_number))

# df_professors['office'] = office_list
# df_professors['phone'] = phone_list

# print(df_professors)

# df_professors.to_csv(r'export_dataframe.csv', index = False, header=True)
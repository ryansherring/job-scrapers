import pandas as pd
import re

from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
from random import randint
from requests import get
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from time import time
start_time = time()

#google stuff for google sheets implementation
import gspread
from gspread_dataframe import set_with_dataframe
gc = gspread.oauth()

from warnings import warn

# replace variables here.
SEARCH_TERMS = 'junior developer'
LOCATION = 'USA'
JOB_COUNT = 25

regex = '|'
INCLUDE = ['javascript', 'python']
INCLUDE = str(regex.join(INCLUDE))
EXCLUDE = ['degree', 'years']
EXCLUDE = str(regex.join(EXCLUDE))

# automatically for last week
url = f"https://www.linkedin.com/jobs/search/?f_TPR=r604800&keywords={SEARCH_TERMS}&location={LOCATION}&sortBy=DD&f_TP=1%2C2&redirect=false&position=1&pageNum=0&f_E=1%2C2"

# this will open up new window with the url provided above
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options, executable_path='../chromedriver')
driver.maximize_window()
driver.get(url)
sleep(3)
action = ActionChains(driver)

# to show more jobs. Depends on number of jobs selected
i = 2
while i <= (JOB_COUNT/25): 
    driver.find_element_by_xpath('/html/body/main/div/section/button').click()
    i = i + 1
    sleep(5)

# parsing the visible webpage
pageSource = driver.page_source
lxml_soup = BeautifulSoup(pageSource, 'lxml')

# searching for all job containers
job_container = lxml_soup.find('ul', class_ = 'jobs-search__results-list')
print('You are scraping information about {} jobs.'.format(len(job_container)))

# setting up list for job information
job_id = []
post_title = []
company_name = []
post_date = []
job_location = []
job_desc = []
level = []

# for loop for job title, company, id, location and date posted
for job in job_container:
    
    # job title
    job_titles = job.find("span", class_="screen-reader-text").text
    post_title.append(job_titles)
    
    # linkedin job id
    job_ids = job.find('a', href=True)['href']
    job_ids = re.findall(r'(?!-)([0-9]*)(?=\?)',job_ids)[0]
    job_ids = f"https://www.linkedin.com/jobs/search/?currentJobId={job_ids}&redirect=false"
    job_id.append(job_ids)
    
    # company name
    company_names = job.select_one('img')['alt']
    company_name.append(company_names)
    
    # job location
    job_locations = job.find("span", class_="job-result-card__location").text
    job_location.append(job_locations)
    
    # posting date
    post_dates = job.select_one('time')['datetime']
    post_date.append(post_dates)

# for loop for job description and criterias
for x in range(1,len(job_id)+1):
    
    # clicking on different job containers to view information about the job
    job_xpath = '/html/body/main/div/section/ul/li[{}]/img'.format(x)
    driver.find_element_by_xpath(job_xpath).click()
    sleep(3)
    
    # job description
    jobdesc_xpath = '/html/body/main/section/div[2]/section[2]/div'
    job_descs = driver.find_element_by_xpath(jobdesc_xpath).text
    job_desc.append(job_descs)
    
    # job criteria container below the description
    job_criteria_container = lxml_soup.find('ul', class_ = 'job-criteria__list')
    all_job_criterias = job_criteria_container.find_all("span", class_='job-criteria__text job-criteria__text--criteria')
    
    x = x+1


# print(len(job_id))
# print(len(post_title))
# print(len(company_name))
# print(len(post_date))
# print(len(job_location))
# print(len(job_desc))


# creating a dataframe
exclude_job_data = pd.DataFrame({'Post': post_title,
'Job ID': job_id,
'Date': post_date,
'Company Name': company_name,
'Location': job_location,
'Description': job_desc,
})

# print('--- pre-processed data below ---')
include_job_data = pd.DataFrame({'Post': post_title,
'Job ID': job_id,
'Date': post_date,
'Company Name': company_name,
'Location': job_location,
'Description': job_desc,
})
# print(len(include_job_data.index))

# cleaning and filtering description column
exclude_job_data['Description'] = exclude_job_data['Description'].str.replace('\n',' ')
include_job_data['Description'] = include_job_data['Description'].str.replace('\n',' ')

print('--- exclude data below ---')
exclude_job_data = exclude_job_data[~exclude_job_data['Description'].str.contains(EXCLUDE, regex=True, case=False)]
print(len(exclude_job_data.index))
exlen = len(exclude_job_data.index)
print('--- include data below ---')

include_job_data = include_job_data[include_job_data['Description'].str.contains(INCLUDE, regex=True, case=False)]
print(len(include_job_data.index))
inlen = len(include_job_data.index)

if (inlen > 0 and exlen > 0):
    job_data = pd.merge(exclude_job_data, include_job_data)
    print('--- merged data below ---')
elif (inlen == 0 and exlen > 0):
    job_data = exclude_job_data
    print(f'using excluded filter only. cannot merge in:{inlen}, ex: {exlen}')
elif (inlen > 0 and exlen == 0):
    job_data = include_job_data
    print(f'using included filter only. cannot merge inc:{inlen}, exc: {exlen}')
else:
    job_data = 0
    print('data not available or no jobs within parameter combo')


if(len(job_data.index) > 0):
    print(job_data.info())
    job_data.to_csv('./jobs.csv', index=0)

print(f"search includes {INCLUDE} and excludes {EXCLUDE}")


# sheet = gc.open('jobs').sheet1
# set_with_dataframe(sheet, job_data)
# sheets_url = dsfghdfgjrtggrsarths
# driver.get(sheets_url)